"""
Gemini AI service for FounderOS
Handles all Gemini API calls with graceful fallback when API key is not set.
"""
import json
import re
from django.conf import settings


def get_gemini_model():
    """Returns a Gemini model instance or None if API key not configured."""
    if not settings.GEMINI_API_KEY:
        return None
    try:
        import google.generativeai as genai
        genai.configure(api_key=settings.GEMINI_API_KEY)
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception:
        return None


def generate_pitch_analysis(title: str, description: str, extracted_text: str) -> dict:
    """Analyze a startup pitch using Gemini AI."""
    model = get_gemini_model()

    if not model:
        return _fallback_pitch_analysis(title)

    prompt = f"""
You are an expert startup pitch analyst. Analyze the following startup pitch and provide structured feedback.

Startup Title: {title}
Description: {description}
Pitch Content: {extracted_text[:3000] if extracted_text else description}

Provide a JSON response with exactly this structure:
{{
  "clarity_score": <integer 0-100>,
  "engagement_score": <integer 0-100>,
  "overall_score": <integer 0-100>,
  "strengths": ["point 1", "point 2", "point 3"],
  "weaknesses": ["point 1", "point 2", "point 3"],
  "recommendations": ["action 1", "action 2", "action 3"],
  "summary": "2-3 sentence overall assessment",
  "investor_readiness": "Low/Medium/High"
}}

Return ONLY valid JSON, no markdown or extra text.
"""
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        # Clean markdown code blocks if present
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*', '', text)
        return json.loads(text)
    except Exception as e:
        return _fallback_pitch_analysis(title)


def generate_risk_analysis(startup_name: str, industry: str, stage: str, description: str) -> dict:
    """Analyze startup risk using Gemini AI."""
    model = get_gemini_model()

    if not model:
        return _fallback_risk_analysis(startup_name)

    prompt = f"""
You are a startup risk analyst. Evaluate the risk profile of this startup.

Startup: {startup_name}
Industry: {industry}
Stage: {stage}
Description: {description}

Provide a JSON response with exactly this structure:
{{
  "financial_risk": <integer 0-100, higher = riskier>,
  "market_risk": <integer 0-100>,
  "operational_risk": <integer 0-100>,
  "overall_score": <integer 0-100, overall risk>,
  "strengths": ["strength 1", "strength 2", "strength 3"],
  "weaknesses": ["weakness 1", "weakness 2"],
  "opportunities": ["opportunity 1", "opportunity 2", "opportunity 3"],
  "threats": ["threat 1", "threat 2", "threat 3"],
  "mitigation_suggestions": ["suggestion 1", "suggestion 2", "suggestion 3", "suggestion 4"],
  "summary": "2-3 sentence risk assessment"
}}

Return ONLY valid JSON.
"""
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*', '', text)
        return json.loads(text)
    except Exception:
        return _fallback_risk_analysis(startup_name)


def generate_scheme_matches(industry: str, stage: str, location: str, description: str) -> list:
    """Match government schemes using Gemini AI."""
    model = get_gemini_model()

    schemes_data = [
        {"name": "Startup India Seed Fund", "max_funding": "₹20 Lakhs", "ministry": "DPIIT"},
        {"name": "Mudra Yojana (Shishu)", "max_funding": "₹50,000", "ministry": "Ministry of Finance"},
        {"name": "Mudra Yojana (Kishore)", "max_funding": "₹5 Lakhs", "ministry": "Ministry of Finance"},
        {"name": "GENESIS Scheme", "max_funding": "₹5 Crores", "ministry": "MeitY"},
        {"name": "SIDBI Startup Mitra", "max_funding": "₹2 Crores", "ministry": "SIDBI"},
        {"name": "Atal Innovation Mission", "max_funding": "₹10 Lakhs", "ministry": "NITI Aayog"},
        {"name": "Stand Up India", "max_funding": "₹1 Crore", "ministry": "Ministry of Finance"},
        {"name": "PM Vishwakarma Scheme", "max_funding": "₹3 Lakhs", "ministry": "MoMSME"},
    ]

    if not model:
        return _fallback_scheme_matches(schemes_data, stage)

    schemes_json = json.dumps(schemes_data)
    prompt = f"""
You are a government scheme advisor. Match the best schemes for this startup.

Industry: {industry}
Stage: {stage}
Location: {location}
Description: {description}

Available schemes: {schemes_json}

Return a JSON array with the top 5 matches:
[
  {{
    "scheme_name": "exact name from list above",
    "eligibility_score": <integer 0-100>,
    "reasoning": "2-3 sentence explanation",
    "status": "eligible" or "partially" or "not_eligible"
  }}
]

Return ONLY valid JSON array.
"""
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*', '', text)
        return json.loads(text)
    except Exception:
        return _fallback_scheme_matches(schemes_data, stage)


def _fallback_pitch_analysis(title: str) -> dict:
    return {
        "clarity_score": 72,
        "engagement_score": 68,
        "overall_score": 70,
        "strengths": [
            "Clear problem statement identified",
            "Target market defined",
            "Solution approach outlined"
        ],
        "weaknesses": [
            "Revenue model needs more detail",
            "Competitive analysis could be stronger"
        ],
        "recommendations": [
            "Add specific market size data (TAM/SAM/SOM)",
            "Include traction metrics or pilot results",
            "Strengthen the unique value proposition"
        ],
        "summary": f"The pitch for '{title}' shows promise with a clear problem-solution fit. Adding concrete data and metrics would significantly improve investor readiness.",
        "investor_readiness": "Medium",
        "_note": "Demo mode — Add GEMINI_API_KEY to .env for AI-powered analysis"
    }


def _fallback_risk_analysis(startup_name: str) -> dict:
    return {
        "financial_risk": 65,
        "market_risk": 55,
        "operational_risk": 48,
        "overall_score": 56,
        "strengths": ["Early mover advantage", "Scalable business model", "Lean team structure"],
        "weaknesses": ["Limited initial capital", "Untested market hypothesis"],
        "opportunities": ["Growing digital adoption in Tier-2/3 cities", "Government startup support schemes", "Underserved market segment"],
        "threats": ["Established competitors", "Regulatory changes", "Market timing risk"],
        "mitigation_suggestions": [
            "Apply for Startup India Seed Fund to extend runway",
            "Run a 30-day paid pilot to validate willingness to pay",
            "Build strategic partnerships to reduce operational costs",
            "Maintain 6-month cash reserve at all times"
        ],
        "summary": f"'{startup_name}' presents a moderate risk profile typical for early-stage startups. Financial risk is the primary concern and should be addressed through early revenue generation or grant funding.",
        "_note": "Demo mode — Add GEMINI_API_KEY to .env for AI-powered analysis"
    }


def _fallback_scheme_matches(schemes_data: list, stage: str) -> list:
    matches = []
    for i, scheme in enumerate(schemes_data[:5]):
        score = max(45, 90 - i * 8)
        matches.append({
            "scheme_name": scheme["name"],
            "eligibility_score": score,
            "reasoning": f"Based on your startup profile and {stage} stage, you appear to meet the basic criteria. Review the scheme guidelines and prepare required documentation.",
            "status": "eligible" if score >= 70 else "partially"
        })
    return matches
