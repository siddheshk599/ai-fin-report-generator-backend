import os, json, logging
from typing import Dict
from google import genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "demo_key")
client = genai.Client(api_key = GEMINI_API_KEY)

async def generate_financial_report(data) -> Dict:
    """Generate a comprehensive financial report using AI"""
    
    # Prepare the prompt for AI
    prompt = f"""
    You are a senior financial analyst creating an executive-level financial report. 
    Generate a comprehensive financial report based on the following company data:
    
    Company: {data.company_name}
    Revenue: ₹{data.revenue:,.2f}
    Profit: ₹{data.profit:,.2f}
    Growth Percentage: {data.growth_percentage}%
    Sector Trends: {data.sector_trends}
    Key Metrics: {data.key_metrics}
    Identified Risks: {data.risks}
    Recommendations: {data.recommendations}
    
    Create a professional financial report with the following sections:
    1. Executive Summary (2-3 paragraphs)
    2. Key Trends Analysis (detailed analysis)
    3. Risk Assessment (comprehensive risk analysis)
    4. Strategic Recommendations (actionable recommendations)
    5. Top 3 Critical Risks (list format)
    6. Top 3 Priority Recommendations (list format)
    
    Respond with a JSON object containing these sections as strings.
    Make the content professional, data-driven, and suitable for C-level executives.
    """
    
    try:
        # Check if we have a valid API key
        if GEMINI_API_KEY == "demo_key":
            logging.warning("Using demo mode - no Gemini API key provided")
            return generate_demo_report(data)
        
        response = client.models.generate_content(
            model = "gemini-2.5-flash",
            contents = prompt
        )
        
        # Parse the AI response
        response_content = response.text
        ai_content = json.loads(response_content) if response_content else {}
        
        # Ensure all required fields are present
        required_fields = [
            "executive_summary", "key_trends", "risks", "recommendations",
            "top_risks", "top_recommendations"
        ]
        
        for field in required_fields:
            if field not in ai_content:
                ai_content[field] = f"Analysis for {field.replace('_', ' ').title()} not available."
        
        # Ensure top_risks and top_recommendations are lists
        if isinstance(ai_content.get("top_risks"), str):
            ai_content["top_risks"] = [ai_content["top_risks"]]
        if isinstance(ai_content.get("top_recommendations"), str):
            ai_content["top_recommendations"] = [ai_content["top_recommendations"]]
        
        return ai_content
        
    except Exception as e:
        logging.error(f"Error generating AI report: {str(e)}")
        # Fallback to demo report if AI fails
        return generate_demo_report(data)

def generate_demo_report(data) -> Dict:
    """Generate a demo report when AI is not available"""
    
    profit_margin = (data.profit / data.revenue * 100) if data.revenue > 0 else 0
    
    return {
        "executive_summary": f"""
        {data.company_name} demonstrates solid financial performance with revenue of ₹{data.revenue:,.2f} 
        and profit of ₹{data.profit:,.2f}, resulting in a profit margin of {profit_margin:.1f}%. 
        The company shows {data.growth_percentage}% growth, indicating positive market momentum. 
        
        Key sector trends and strategic positioning require attention to maintain competitive advantage. 
        Management should focus on optimizing operational efficiency while addressing identified risks 
        to ensure sustainable growth trajectory.
        """.strip(),
        
        "key_trends": f"""
        Current market analysis reveals {data.growth_percentage}% growth rate, which positions 
        {data.company_name} favorably within the sector. Sector trends indicate: {data.sector_trends}
        
        Key performance metrics show: {data.key_metrics}
        
        The financial fundamentals demonstrate stability with current profit margins at {profit_margin:.1f}%. 
        Revenue diversification and market expansion opportunities should be evaluated to strengthen 
        the company's competitive position.
        """.strip(),
        
        "risks": f"""
        Primary risk factors identified include: {data.risks}
        
        Financial risk assessment indicates potential vulnerabilities in market volatility exposure. 
        Operational risks related to supply chain dependencies and competitive pressures require 
        proactive management strategies.
        
        Regulatory changes and economic uncertainties pose additional challenges that could impact 
        future performance if not adequately addressed through strategic planning.
        """.strip(),
        
        "recommendations": f"""
        Strategic recommendations for {data.company_name}: {data.recommendations}
        
        1. Implement enhanced financial controls and monitoring systems
        2. Diversify revenue streams to reduce market concentration risk
        3. Invest in technology infrastructure to improve operational efficiency
        4. Develop comprehensive risk management framework
        5. Strengthen market position through strategic partnerships
        
        These initiatives should be prioritized based on resource availability and strategic impact.
        """.strip(),
        
        "top_risks": [
            "Market volatility and economic uncertainty",
            "Competitive pressure and market share erosion",
            "Operational inefficiencies and cost escalation"
        ],
        
        "top_recommendations": [
            "Diversify revenue streams and market presence",
            "Implement advanced analytics for decision making",
            "Strengthen operational risk management processes"
        ]
    }
