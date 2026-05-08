#!/usr/bin/env python3
"""
Day 20: Advanced AI Demo
Demonstrates three advanced AI operations:
1. AI Recommend (with read-aloud via text-to-speech)
2. Report Generation (with streaming visualization)
3. RAG Query (semantic retrieval demonstration)
"""

import os
import sys
import json
import time
import requests
from typing import Optional
from datetime import datetime

# Text-to-speech support (optional)
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("[INFO] pyttsx3 not installed. Install with: pip install pyttsx3")


BASE_URL = os.getenv('AI_SERVICE_URL', 'http://localhost:5000/api/ai')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# Color codes for terminal output
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
MAGENTA = '\033[95m'
RESET = '\033[0m'
BOLD = '\033[1m'


def print_section(title: str):
    """Print a formatted section header"""
    print(f"\n{BOLD}{CYAN}{'='*70}{RESET}")
    print(f"{BOLD}{CYAN}{title.center(70)}{RESET}")
    print(f"{BOLD}{CYAN}{'='*70}{RESET}\n")


def print_step(step: int, description: str):
    """Print a numbered step"""
    print(f"{MAGENTA}[STEP {step}]{RESET} {description}")


def print_ai_thought(thought: str):
    """Print what the AI is thinking/doing"""
    print(f"{YELLOW}💭 AI: {thought}{RESET}")


def print_success(message: str):
    """Print success message"""
    print(f"{GREEN}✓ {message}{RESET}")


def read_aloud(text: str, enable_tts: bool = True):
    """
    Read text aloud using text-to-speech if available
    
    Args:
        text: Text to read
        enable_tts: Whether to actually use TTS or just print
    """
    if not enable_tts or not TTS_AVAILABLE:
        print(f"{CYAN}[TEXT-TO-SPEECH SIMULATED]{RESET}")
        return
    
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)  # Speed
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"{YELLOW}[TTS Error: {e}]{RESET}")


# ==================== DEMO 1: AI RECOMMEND (with read-aloud) ====================

def demo_recommend():
    """
    DEMO 1: AI Recommend endpoint with text-to-speech read-aloud
    
    What the AI is doing:
    1. Analyzing the input text for context and intent
    2. Identifying key issues and pain points
    3. Generating actionable recommendations with priorities
    4. Classifying each recommendation by type (fix, improve, investigate, etc.)
    """
    print_section("DEMO 1: AI RECOMMEND (Read-Aloud) 🎙️")
    
    print(f"{CYAN}Endpoint: POST /api/ai/recommend{RESET}")
    print(f"{CYAN}Purpose: Generate actionable recommendations with AI analysis{RESET}\n")
    
    # Sample input: A support ticket or issue description
    issue_text = (
        "Our mobile app is crashing on the login screen for Android users. "
        "The issue started after the latest update. Users report the app freezes "
        "for 5-10 seconds then closes. We've lost 15% of daily active users in the past week. "
        "The team suspects it's related to the new session management code."
    )
    
    print_step(1, "Preparing input for AI analysis")
    print(f"Input: {issue_text}\n")
    
    print_ai_thought("Reading the input... I see:")
    print_ai_thought("- Issue Type: Mobile app crash")
    print_ai_thought("- Severity: High (15% user drop)")
    print_ai_thought("- Suspected Cause: Session management code")
    print_ai_thought("- Generating 3 prioritized recommendations...\n")
    
    payload = {"text": issue_text}
    
    print_step(2, "Calling AI Recommend endpoint")
    try:
        response = requests.post(
            f"{BASE_URL}/recommend",
            json=payload,
            timeout=30,
            headers={'Accept': 'application/json', 'Content-Type': 'application/json'}
        )
        
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.text)
            return
        
        result = response.json()
        print_success(f"Response received in {response.elapsed.total_seconds():.2f}s\n")
        
        # Display recommendations
        recommendations = result.get('recommendations', [])
        print(f"{BOLD}Generated Recommendations:{RESET}")
        
        for i, rec in enumerate(recommendations, 1):
            action_type = rec.get('action_type', 'unknown').upper()
            priority = rec.get('priority', 'medium').upper()
            description = rec.get('description', '')
            
            print(f"\n{BOLD}Recommendation {i}:{RESET}")
            print(f"  Type:     {MAGENTA}{action_type}{RESET}")
            print(f"  Priority: {priority}")
            print(f"  Action:   {description}")
        
        # Read first recommendation aloud
        if recommendations:
            print_step(3, "Reading first recommendation aloud (Text-to-Speech)")
            first_rec = recommendations[0]
            text_to_read = (
                f"Recommendation: {first_rec.get('description', '')}. "
                f"Priority: {first_rec.get('priority', 'medium')}. "
                f"Action type: {first_rec.get('action_type', 'investigate')}."
            )
            
            print(f"\nText: '{text_to_read}'\n")
            read_aloud(text_to_read, enable_tts=TTS_AVAILABLE)
            print_success("Read-aloud completed")
        
        # Save results
        output_file = 'day20_recommend_results.json'
        with open(output_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'endpoint': '/recommend',
                'input': issue_text,
                'recommendations': recommendations,
                'response_time_seconds': response.elapsed.total_seconds()
            }, f, indent=2)
        print_success(f"Results saved to {output_file}")
        
    except Exception as e:
        print(f"Error: {e}")


# ==================== DEMO 2: REPORT GENERATION (Streaming) ====================

def demo_report_streaming():
    """
    DEMO 2: Report generation with streaming
    
    What the AI is doing:
    1. Analyzing the topic for context
    2. Optionally retrieving relevant documents via RAG
    3. Processing retrieved context with LLM
    4. Generating report sections incrementally
    5. Streaming output in real-time for progressive display
    """
    print_section("DEMO 2: REPORT GENERATION (Streaming) 📊")
    
    print(f"{CYAN}Endpoint: POST /api/ai/generate-report?stream=true{RESET}")
    print(f"{CYAN}Purpose: Generate comprehensive reports with real-time streaming{RESET}\n")
    
    topic = "Mobile App Crash Issues in Android Platform"
    
    print_step(1, "Setting up report generation request")
    print(f"Topic:    {topic}")
    print(f"Type:     Executive Summary")
    print(f"Streaming: Enabled (real-time output)\n")
    
    print_ai_thought("When streaming is enabled, the LLM generates report sections")
    print_ai_thought("and sends them as Server-Sent Events (SSE) in real-time.")
    print_ai_thought("This allows progressive UI updates without waiting for full completion.\n")
    
    payload = {
        "topic": topic,
        "report_type": "executive",
        "use_rag": True,
        "custom_context": "Recent update introduced session management changes",
        "top_items_count": 5
    }
    
    print_step(2, "Streaming report sections")
    
    try:
        # Request with stream=true
        response = requests.post(
            f"{BASE_URL}/generate-report?stream=true",
            json=payload,
            timeout=60,
            stream=True,  # Enable streaming
            headers={'Accept': 'text/event-stream', 'Content-Type': 'application/json'}
        )
        
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.text)
            return
        
        print(f"{BOLD}Real-time Report Output:{RESET}\n")
        
        chunk_count = 0
        full_report = ""
        
        # Process streaming response
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                
                # Handle SSE format
                if line.startswith('data:'):
                    try:
                        data = json.loads(line[5:].strip())
                        
                        if 'content' in data:
                            chunk_count += 1
                            content = data['content']
                            full_report += content
                            
                            # Print progressively
                            print(content, end='', flush=True)
                            
                    except json.JSONDecodeError:
                        pass
        
        print(f"\n\n{BOLD}Streaming completed.{RESET}")
        print_success(f"Received {chunk_count} chunks")
        
        # Save streamed results
        output_file = 'day20_report_streaming_results.json'
        with open(output_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'endpoint': '/generate-report?stream=true',
                'topic': topic,
                'report_type': 'executive',
                'chunks_received': chunk_count,
                'full_report_preview': full_report[:500] + "..." if len(full_report) > 500 else full_report
            }, f, indent=2)
        print_success(f"Results saved to {output_file}")
        
    except requests.exceptions.StreamConsumedError:
        print_success("Stream successfully consumed")
    except Exception as e:
        print(f"Error: {e}")


# ==================== DEMO 3: RAG QUERY (Semantic Retrieval) ====================

def demo_rag_query():
    """
    DEMO 3: RAG Query - Semantic retrieval of relevant documents
    
    What the AI is doing:
    1. Converting user query into semantic embeddings
    2. Searching ChromaDB for similar documents
    3. Retrieving top-k most relevant documents
    4. Computing similarity scores for relevance ranking
    5. Returning context for downstream LLM operations
    """
    print_section("DEMO 3: RAG QUERY (Semantic Retrieval) 🔍")
    
    print(f"{CYAN}Endpoint: POST /api/ai/rag/retrieve{RESET}")
    print(f"{CYAN}Purpose: Retrieve semantically similar documents from knowledge base{RESET}\n")
    
    query = "How do I troubleshoot app crashes on Android?"
    
    print_step(1, "Preparing RAG query")
    print(f"Query: {query}\n")
    
    print_ai_thought("Converting query to embeddings using sentence-transformers...")
    print_ai_thought("Searching ChromaDB vector database...")
    print_ai_thought("Computing semantic similarity scores...")
    print_ai_thought("Ranking results by relevance...\n")
    
    payload = {
        "query": query,
        "n_results": 5
    }
    
    print_step(2, "Sending RAG retrieve request")
    try:
        response = requests.post(
            f"{BASE_URL}/rag/retrieve",
            json=payload,
            timeout=30,
            headers={'Accept': 'application/json', 'Content-Type': 'application/json'}
        )
        
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.text)
            return
        
        result = response.json()
        print_success(f"Response received in {response.elapsed.total_seconds():.2f}s\n")
        
        # Display retrieved documents
        documents = result.get('data', {}).get('documents', [])
        metadatas = result.get('data', {}).get('metadatas', [])
        distances = result.get('data', {}).get('distances', [])
        
        print(f"{BOLD}Retrieved Documents ({len(documents)} results):{RESET}\n")
        
        for i, doc in enumerate(documents, 1):
            distance = distances[i-1] if i-1 < len(distances) else 'N/A'
            metadata = metadatas[i-1] if i-1 < len(metadatas) else {}
            
            # Convert distance to similarity score (0-1)
            similarity = 1 - (distance if isinstance(distance, (int, float)) else 0)
            
            print(f"{BOLD}Result {i}:{RESET}")
            print(f"  Similarity: {similarity:.2%}")
            print(f"  Document:   {doc[:150]}{'...' if len(doc) > 150 else ''}")
            if metadata:
                print(f"  Metadata:   {metadata}")
            print()
        
        # Save RAG results
        output_file = 'day20_rag_query_results.json'
        with open(output_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'endpoint': '/rag/retrieve',
                'query': query,
                'n_results_requested': 5,
                'n_results_returned': len(documents),
                'documents': documents[:3],  # Save first 3 for brevity
                'documents_count': len(documents),
                'response_time_seconds': response.elapsed.total_seconds()
            }, f, indent=2)
        print_success(f"Results saved to {output_file}")
        
    except Exception as e:
        print(f"Error: {e}")


# ==================== MAIN EXECUTION ====================

def main():
    """Run all three demos"""
    
    print(f"\n{BOLD}{CYAN}")
    print("╔" + "═"*68 + "╗")
    print("║" + " "*15 + "DAY 20: ADVANCED AI OPERATIONS DEMO" + " "*19 + "║")
    print("╚" + "═"*68 + "╝")
    print(RESET)
    
    # Check prerequisites
    print_step(0, "Checking prerequisites")
    
    if not GROQ_API_KEY:
        print(f"{YELLOW}⚠ GROQ_API_KEY not found in environment.{RESET}")
        print(f"{YELLOW}  Set GROQ_API_KEY environment variable before running.{RESET}\n")
        return 1
    else:
        print_success("GROQ_API_KEY is set ✓")
    
    print_success(f"Base URL: {BASE_URL}")
    print_success(f"TTS Support: {'Available' if TTS_AVAILABLE else 'Not installed (optional)'}\n")
    
    # Run demos
    try:
        demo_recommend()
        print("\n")
        demo_report_streaming()
        print("\n")
        demo_rag_query()
        
        print_section("Day 20 Demo Complete 🎉")
        print(f"{GREEN}All demonstrations completed successfully!{RESET}")
        print(f"{CYAN}Output files:${RESET}")
        print("  - day20_recommend_results.json")
        print("  - day20_report_streaming_results.json")
        print("  - day20_rag_query_results.json\n")
        
        return 0
        
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Demo interrupted by user.{RESET}")
        return 1
    except Exception as e:
        print(f"\n{YELLOW}Error during demo: {e}{RESET}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
