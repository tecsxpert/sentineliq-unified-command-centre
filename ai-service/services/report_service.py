"""
Report Generation Service
Produces structured JSON reports with AI-generated content
Uses RAG for context and Groq for intelligent synthesis
"""
import json
from datetime import datetime
from typing import Dict, List, Optional
from services.rag_service import get_rag_service
from services.groq_client import GroqClient
import os


class ReportService:
    """Service for generating structured reports"""
    
    def __init__(self, groq_api_key: Optional[str] = None):
        """
        Initialize Report Service
        
        Args:
            groq_api_key: Groq API key (defaults to env variable)
        """
        self.groq_api_key = groq_api_key or os.getenv('GROQ_API_KEY')
        self.groq_client = GroqClient(api_key=self.groq_api_key)
        self.rag_service = get_rag_service()
    
    def _retrieve_context(self, query: str, n_results: int = 5) -> str:
        """Retrieve relevant context from RAG pipeline"""
        try:
            results = self.rag_service.retrieve_documents(query, n_results)
            context_docs = results['results']['documents']
            return "\n\n".join(context_docs) if context_docs else ""
        except Exception as e:
            print(f"Warning: Could not retrieve context: {str(e)}")
            return ""
    
    def _generate_streaming_title(self, topic: str):
        """Generate report title using streaming Groq"""
        prompt = f"""Generate a professional and concise report title for the following topic. 
        Return ONLY the title, nothing else.
        
        Topic: {topic}"""

        try:
            for chunk in self.groq_client.generate_streaming_response(prompt):
                yield chunk
        except Exception as e:
            print(f"Error generating streaming title: {str(e)}")
            yield f"Report: {topic}"

    def _generate_streaming_overview(self, topic: str, context: str = ""):
        """Generate detailed overview using streaming Groq"""
        context_section = f"\nAvailable information:\n{context[:1500]}\n" if context else ""

        prompt = f"""Generate a detailed overview (3-4 paragraphs) for a report on: {topic}
{context_section}

The overview should:
1. Explain what this topic is about
2. Describe its importance and relevance
3. Outline the key aspects covered in this report

Return ONLY the overview text in clear paragraphs."""

        try:
            for chunk in self.groq_client.generate_streaming_response(prompt):
                yield chunk
        except Exception as e:
            print(f"Error generating streaming overview: {str(e)}")
            yield f"Comprehensive overview of {topic}"

    def _generate_streaming_executive_summary(self, topic: str, overview: str,
                                             context: str = ""):
        """Generate executive summary using streaming Groq"""
        context_section = f"\nContext from knowledge base:\n{context[:1000]}\n" if context else ""

        prompt = f"""Generate a professional executive summary (2-3 sentences) for a report on the following:

Topic: {topic}

Overview: {overview}
{context_section}

Create a concise executive summary that captures the key points and value proposition. 
Return ONLY the executive summary text, no labels or formatting."""

        try:
            for chunk in self.groq_client.generate_streaming_response(prompt):
                yield chunk
        except Exception as e:
            print(f"Error generating streaming executive summary: {str(e)}")
            yield overview[:200]
    
    def _generate_executive_summary(self, topic: str, overview: str, 
                                   context: str = "") -> str:
        """Generate executive summary using Groq"""
        context_section = f"\nContext from knowledge base:\n{context[:1000]}\n" if context else ""
        
        prompt = f"""Generate a professional executive summary (2-3 sentences) for a report on the following:

Topic: {topic}

Overview: {overview}
{context_section}

Create a concise executive summary that captures the key points and value proposition. 
Return ONLY the executive summary text, no labels or formatting."""
        
        try:
            summary = self.groq_client.chat(prompt).strip()
            return summary
        except Exception as e:
            print(f"Error generating executive summary: {str(e)}")
            return overview[:200]
    
    def _generate_overview(self, topic: str, context: str = "") -> str:
        """Generate detailed overview using Groq"""
        context_section = f"\nAvailable information:\n{context[:1500]}\n" if context else ""
        
        prompt = f"""Generate a detailed overview (3-4 paragraphs) for a report on: {topic}
{context_section}

The overview should:
1. Explain what this topic is about
2. Describe its importance and relevance
3. Outline the key aspects covered in this report

Return ONLY the overview text in clear paragraphs."""
        
        try:
            overview = self.groq_client.chat(prompt).strip()
            return overview
        except Exception as e:
            print(f"Error generating overview: {str(e)}")
            return f"Comprehensive overview of {topic}"
    
    def _generate_top_items(self, topic: str, context: str = "", 
                           count: int = 5) -> List[Dict]:
        """Generate top items/findings using Groq"""
        context_section = f"\nContext:\n{context[:1500]}\n" if context else ""
        
        prompt = f"""Generate the top {count} key items, findings, or recommendations about: {topic}
{context_section}

Return ONLY a JSON array with exactly {count} objects, each with:
- "item_number": number starting from 1
- "title": short title (5-10 words)
- "description": detailed description (1-2 sentences)
- "impact": one of "high", "medium", "low"
- "priority": number from 1 to {count} (1 being highest)

Return ONLY valid JSON array, no other text."""
        
        try:
            response = self.groq_client.chat(prompt).strip()
            
            # Try to parse JSON
            items = json.loads(response)
            if not isinstance(items, list):
                items = [items]
            
            # Validate and clean items
            validated_items = []
            for i, item in enumerate(items[:count]):
                if isinstance(item, dict):
                    validated_items.append({
                        "item_number": item.get("item_number", i+1),
                        "title": item.get("title", f"Item {i+1}"),
                        "description": item.get("description", ""),
                        "impact": item.get("impact", "medium"),
                        "priority": item.get("priority", i+1)
                    })
            
            return validated_items
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return [{
                "item_number": i+1,
                "title": f"Key Finding {i+1}",
                "description": f"Important aspect of {topic}",
                "impact": "high" if i == 0 else "medium",
                "priority": i+1
            } for i in range(count)]
        except Exception as e:
            print(f"Error generating top items: {str(e)}")
            return []
    
    def _generate_recommendations(self, topic: str, overview: str, 
                                 items: List[Dict], context: str = "") -> List[Dict]:
        """Generate recommendations using Groq"""
        context_section = f"\nContext:\n{context[:1000]}\n" if context else ""
        items_summary = "\n".join([f"- {item['title']}: {item['description']}" 
                                  for item in items[:3]])
        
        prompt = f"""Based on the following report details, generate 4-5 actionable recommendations:

Topic: {topic}
Overview: {overview[:200]}
Key Items:
{items_summary}
{context_section}

Return ONLY a JSON array with 4-5 objects, each with:
- "recommendation": the recommendation text (1-2 sentences)
- "action": specific action steps (2-3 bullet points as a single string with \\n)
- "timeline": "immediate", "short-term", or "long-term"
- "effort": "low", "medium", or "high"

Return ONLY valid JSON array, no other text."""
        
        try:
            response = self.groq_client.chat(prompt).strip()
            recommendations = json.loads(response)
            
            if not isinstance(recommendations, list):
                recommendations = [recommendations]
            
            # Validate recommendations
            validated_recs = []
            for rec in recommendations:
                if isinstance(rec, dict):
                    validated_recs.append({
                        "recommendation": rec.get("recommendation", ""),
                        "action": rec.get("action", ""),
                        "timeline": rec.get("timeline", "medium-term"),
                        "effort": rec.get("effort", "medium")
                    })
            
            return validated_recs
        except json.JSONDecodeError:
            # Fallback recommendations
            return [{
                "recommendation": f"Implement best practices for {topic}",
                "action": "1. Define goals\n2. Create action plan\n3. Execute and monitor",
                "timeline": "short-term",
                "effort": "medium"
            }]
        except Exception as e:
            print(f"Error generating recommendations: {str(e)}")
            return []
    
    def generate_report(self, topic: str, report_type: str = "general",
                       use_rag: bool = True, custom_context: str = "",
                       top_items_count: int = 5) -> Dict:
        """
        Generate a comprehensive report
        
        Args:
            topic: Report topic/title
            report_type: Type of report (general, technical, executive, etc.)
            use_rag: Whether to use RAG for context retrieval
            custom_context: Optional custom context to include
            top_items_count: Number of top items to generate
            
        Returns:
            Report JSON with structure: {
                title, executive_summary, overview, 
                top_items, recommendations, metadata
            }
        """
        try:
            print(f"Generating {report_type} report on: {topic}")
            
            # Step 1: Retrieve context
            context = ""
            if use_rag:
                context = self._retrieve_context(topic, n_results=5)
            
            if custom_context:
                context = f"{custom_context}\n\n{context}" if context else custom_context
            
            # Step 2: Generate title
            print("  > Generating title...")
            title = self._generate_title(topic)
            
            # Step 3: Generate overview
            print("  > Generating overview...")
            overview = self._generate_overview(topic, context)
            
            # Step 4: Generate executive summary
            print("  > Generating executive summary...")
            executive_summary = self._generate_executive_summary(topic, overview, context)
            
            # Step 5: Generate top items
            print(f"  > Generating top {top_items_count} items...")
            top_items = self._generate_top_items(topic, context, top_items_count)
            
            # Step 6: Generate recommendations
            print("  > Generating recommendations...")
            recommendations = self._generate_recommendations(topic, overview, top_items, context)
            
            # Compile report
            report = {
                "title": title,
                "executive_summary": executive_summary,
                "overview": overview,
                "top_items": top_items,
                "recommendations": recommendations,
                "metadata": {
                    "generated_at": datetime.now().isoformat(),
                    "report_type": report_type,
                    "topic": topic,
                    "items_count": len(top_items),
                    "recommendations_count": len(recommendations),
                    "context_used": "rag" if use_rag else "custom" if custom_context else "none"
                }
            }
            
    def generate_streaming_report(self, topic: str, report_type: str = "general",
                                 use_rag: bool = True, custom_context: str = "",
                                 top_items_count: int = 5):
        """
        Generate a report with streaming output
        Yields SSE events as different parts are generated
        """
        try:
            print(f"Generating streaming {report_type} report on: {topic}")

            # Step 1: Retrieve context
            context = ""
            if use_rag:
                context = self._retrieve_context(topic, n_results=5)

            if custom_context:
                context = f"{custom_context}\n\n{context}" if context else custom_context

            # Send start event
            yield f"event: start\ndata: {json.dumps({'status': 'started', 'topic': topic})}\n\n"

            # Step 2: Generate title
            print("  > Generating title...")
            yield f"event: progress\ndata: {json.dumps({'step': 'title', 'message': 'Generating report title...'})}\n\n"

            title = ""
            for chunk in self._generate_streaming_title(topic):
                title += chunk
                yield f"event: title\ndata: {json.dumps({'chunk': chunk})}\n\n"

            # Step 3: Generate overview
            print("  > Generating overview...")
            yield f"event: progress\ndata: {json.dumps({'step': 'overview', 'message': 'Generating detailed overview...'})}\n\n"

            overview = ""
            for chunk in self._generate_streaming_overview(topic, context):
                overview += chunk
                yield f"event: overview\ndata: {json.dumps({'chunk': chunk})}\n\n"

            # Step 4: Generate executive summary
            print("  > Generating executive summary...")
            yield f"event: progress\ndata: {json.dumps({'step': 'executive_summary', 'message': 'Creating executive summary...'})}\n\n"

            executive_summary = ""
            for chunk in self._generate_streaming_executive_summary(topic, overview, context):
                executive_summary += chunk
                yield f"event: executive_summary\ndata: {json.dumps({'chunk': chunk})}\n\n"

            # Step 5: Generate top items
            print(f"  > Generating top {top_items_count} items...")
            yield f"event: progress\ndata: {json.dumps({'step': 'top_items', 'message': f'Generating top {top_items_count} items...'})}\n\n"

            top_items = self._generate_top_items(topic, context, top_items_count)
            yield f"event: top_items\ndata: {json.dumps({'items': top_items})}\n\n"

            # Step 6: Generate recommendations
            print("  > Generating recommendations...")
            yield f"event: progress\ndata: {json.dumps({'step': 'recommendations', 'message': 'Creating actionable recommendations...'})}\n\n"

            recommendations = self._generate_recommendations(topic, overview, top_items, context)
            yield f"event: recommendations\ndata: {json.dumps({'recommendations': recommendations})}\n\n"

            # Send complete report
            report = {
                "title": title,
                "executive_summary": executive_summary,
                "overview": overview,
                "top_items": top_items,
                "recommendations": recommendations,
                "metadata": {
                    "generated_at": datetime.now().isoformat(),
                    "report_type": report_type,
                    "topic": topic,
                    "items_count": len(top_items),
                    "recommendations_count": len(recommendations),
                    "context_used": "rag" if use_rag else "custom" if custom_context else "none"
                }
            }

            yield f"event: complete\ndata: {json.dumps({'status': 'completed', 'report': report})}\n\n"

            print("✓ Streaming report generated successfully")

        except Exception as e:
            print(f"✗ Error generating streaming report: {str(e)}")
            yield f"event: error\ndata: {json.dumps({'status': 'error', 'message': str(e)})}\n\n"
    
    def generate_streaming_summarized_report(self, topic: str, context_docs: List[str]):
        """Generate streaming report from specific context documents"""
        context = "\n\n".join(context_docs)
        # For summarized reports, we can reuse the streaming logic with custom context
        for event in self.generate_streaming_report(topic, custom_context=context, use_rag=False):
            yield event
    
    def generate_comparative_report(self, items_to_compare: List[str]) -> Dict:
        """Generate comparative report for multiple items"""
        topic = f"Comparison of {' vs '.join(items_to_compare)}"
        context = "\n".join([f"Comparing: {item}" for item in items_to_compare])
        return self.generate_report(topic, report_type="comparative", custom_context=context)
    
    def get_report_template(self) -> Dict:
        """Get empty report template"""
        return {
            "title": "",
            "executive_summary": "",
            "overview": "",
            "top_items": [],
            "recommendations": [],
            "metadata": {
                "generated_at": None,
                "report_type": "",
                "topic": "",
                "items_count": 0,
                "recommendations_count": 0,
                "context_used": None
            }
        }


# Singleton instance
_report_service = None

def get_report_service(groq_api_key: Optional[str] = None) -> ReportService:
    """Get or create report service singleton"""
    global _report_service
    if _report_service is None:
        _report_service = ReportService(groq_api_key)
    return _report_service
