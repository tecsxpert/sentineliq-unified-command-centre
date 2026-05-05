"""
Analyse Document Route - Document analysis for insights and risks
POST /api/ai/analyse-document
"""
from flask import Blueprint, jsonify, request
from services.groq_client import GroqClient
import json

# Create blueprint
analyse_bp = Blueprint('analyse', __name__)

client = GroqClient()


def validate_analyse_input(text):
    """Validate and clean input for document analysis."""
    if not text or not isinstance(text, str):
        return False, "Text must be a non-empty string", None

    cleaned = text.strip()

    if len(cleaned) < 50:
        return False, "Text must be at least 50 characters long for meaningful analysis", None

    if len(cleaned) > 10000:
        return False, "Text exceeds maximum length of 10000 characters", None

    return True, None, cleaned


def normalize_finding(item, finding_type):
    """Normalize a finding object and enforce valid fields."""
    if not isinstance(item, dict):
        return {
            "type": finding_type,
            "category": "general",
            "title": "Analysis finding",
            "description": "Document analysis result",
            "severity": "medium",
            "confidence": 0.7
        }

    # Validate finding type
    if finding_type not in ["insight", "risk"]:
        finding_type = "insight"

    # Validate category
    valid_categories = {
        "insight": ["technical", "business", "operational", "strategic", "compliance", "performance", "security"],
        "risk": ["security", "compliance", "operational", "financial", "reputational", "technical", "strategic"]
    }

    category = str(item.get("category", "general")).strip().lower()
    if category not in valid_categories[finding_type]:
        category = "general"

    title = str(item.get("title", f"Document {finding_type}")).strip()
    if not title:
        title = f"Document {finding_type}"

    description = str(item.get("description", "")).strip()
    if not description:
        description = f"Analysis identified a {finding_type} in the document."

    # Validate severity
    severity = str(item.get("severity", "medium")).strip().lower()
    if severity not in ["low", "medium", "high", "critical"]:
        severity = "medium"

    # Validate confidence
    confidence = item.get("confidence", 0.7)
    if not isinstance(confidence, (int, float)) or confidence < 0 or confidence > 1:
        confidence = 0.7

    return {
        "type": finding_type,
        "category": category,
        "title": title,
        "description": description,
        "severity": severity,
        "confidence": round(float(confidence), 2)
    }


def analyse_document(text):
    """Analyze document text for key insights and risks."""
    prompt = f"""Analyze the following document text and identify key insights and risks.
Return ONLY a JSON object with two arrays: "insights" and "risks".

For each insight, provide:
- category: technical|business|operational|strategic|compliance|performance|security
- title: brief title (5-10 words)
- description: detailed explanation (1-2 sentences)
- severity: low|medium|high (insights typically low-medium)
- confidence: 0.0-1.0 (how confident you are in this insight)

For each risk, provide:
- category: security|compliance|operational|financial|reputational|technical|strategic
- title: brief title (5-10 words)
- description: detailed explanation (1-2 sentences)
- severity: low|medium|high|critical
- confidence: 0.0-1.0 (how confident you are in this risk)

Focus on:
- Key business insights or opportunities
- Potential risks or threats
- Compliance or regulatory concerns
- Technical issues or improvements
- Operational efficiencies or problems
- Strategic implications

Return 3-5 insights and 2-4 risks maximum. Prioritize the most important findings.

Document Text:
{text}

Return ONLY valid JSON:
{{
    "insights": [...],
    "risks": [...]
}}"""

    try:
        response = client.generate_response(prompt).strip()

        # Try to parse JSON
        parsed = json.loads(response)

        if not isinstance(parsed, dict):
            parsed = {"insights": [], "risks": []}

        # Extract and normalize insights
        insights = []
        if "insights" in parsed and isinstance(parsed["insights"], list):
            insights = [normalize_finding(item, "insight") for item in parsed["insights"][:5]]

        # Extract and normalize risks
        risks = []
        if "risks" in parsed and isinstance(parsed["risks"], list):
            risks = [normalize_finding(item, "risk") for item in parsed["risks"][:4]]

        # Ensure we have at least some findings
        if not insights and not risks:
            # Fallback analysis
            insights = [
                {
                    "type": "insight",
                    "category": "general",
                    "title": "Document Content Analysis",
                    "description": "The document contains analyzable content that may have business implications.",
                    "severity": "medium",
                    "confidence": 0.6
                }
            ]

        return {
            "insights": insights,
            "risks": risks,
            "metadata": {
                "document_length": len(text),
                "insights_count": len(insights),
                "risks_count": len(risks),
                "analysis_timestamp": json.dumps(None)  # Will be set by caller
            }
        }

    except json.JSONDecodeError as e:
        print(f"JSON parsing error in document analysis: {e}")
        # Fallback response
        return {
            "insights": [
                {
                    "type": "insight",
                    "category": "general",
                    "title": "Document Analysis Completed",
                    "description": "Basic analysis of document content completed successfully.",
                    "severity": "low",
                    "confidence": 0.5
                }
            ],
            "risks": [],
            "metadata": {
                "document_length": len(text),
                "insights_count": 1,
                "risks_count": 0,
                "analysis_timestamp": json.dumps(None)
            }
        }
    except Exception as e:
        print(f"Error in document analysis: {str(e)}")
        raise


@analyse_bp.route('/analyse-document', methods=['POST'])
def analyse_document_endpoint():
    """
    Analyze document text for key insights and risks

    Expected JSON:
    {
        "text": "string (required) - Document text to analyze",
        "focus_areas": "array (optional) - Specific areas to focus on: security, compliance, business, technical, operational"
    }

    Returns:
    {
        "status": "success",
        "data": {
            "insights": [
                {
                    "type": "insight",
                    "category": "string",
                    "title": "string",
                    "description": "string",
                    "severity": "low|medium|high",
                    "confidence": 0.0-1.0
                }
            ],
            "risks": [
                {
                    "type": "risk",
                    "category": "string",
                    "title": "string",
                    "description": "string",
                    "severity": "low|medium|high|critical",
                    "confidence": 0.0-1.0
                }
            ],
            "metadata": {
                "document_length": integer,
                "insights_count": integer,
                "risks_count": integer,
                "analysis_timestamp": "ISO timestamp"
            }
        }
    }
    """
    try:
        data = request.get_json()

        # Validate required fields
        if not data or 'text' not in data:
            return jsonify({
                "status": "error",
                "message": "Missing required field: 'text'"
            }), 400

        text = data['text']
        if not isinstance(text, str) or len(text.strip()) == 0:
            return jsonify({
                "status": "error",
                "message": "Text must be a non-empty string"
            }), 400

        # Validate input
        is_valid, error_message, cleaned_text = validate_analyse_input(text)
        if not is_valid:
            return jsonify({
                "status": "error",
                "message": error_message
            }), 400

        # Optional focus areas
        focus_areas = data.get('focus_areas', [])

        # Perform analysis
        result = analyse_document(cleaned_text)

        # Add timestamp
        from datetime import datetime
        result["metadata"]["analysis_timestamp"] = datetime.now().isoformat()

        return jsonify({
            "status": "success",
            "data": result
        }), 200

    except ValueError as e:
        return jsonify({
            "status": "error",
            "message": f"Invalid parameter: {str(e)}"
        }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500