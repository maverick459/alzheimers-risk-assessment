
from flask import Flask, render_template, request, session, redirect, url_for, jsonify, make_response
import os
import json
import uuid
from datetime import datetime
from risk_calculator import AlzheimersRiskCalculator
from crew_agents import DataValidationAgent, RiskCalculationAgent, GeminiExplanationAgent
from database import Database
import openai
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import io
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

# Configure session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False

# Initialize OpenAI
openai.api_key = os.environ.get('OPENAI_API_KEY')

# Initialize Database
try:
    db = Database()
    db.create_tables()
    print("Database connected and tables created successfully!")
except Exception as e:
    print(f"Database connection failed: {e}")
    db = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/assessment')
def assessment():
    # Generate or get session ID
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    
    # Try to load existing assessment data from database
    assessment_data = {}
    if db:
        try:
            stored_data = db.get_assessment(session['session_id'])
            if stored_data and stored_data['assessment_data']:
                assessment_data = stored_data['assessment_data']
        except Exception as e:
            print(f"Error loading assessment data: {e}")
    
    # Fallback to session data if database fails
    if not assessment_data and 'assessment_data' in session:
        assessment_data = session['assessment_data']
    elif not assessment_data:
        assessment_data = {}
    
    return render_template('assessment.html', data=assessment_data)

@app.route('/save_step', methods=['POST'])
def save_step():
    try:
        step_data = request.get_json()
        
        # Ensure session ID exists
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())
        
        # Update session data
        if 'assessment_data' not in session:
            session['assessment_data'] = {}
        session['assessment_data'].update(step_data)
        session.modified = True
        
        # Save to database
        if db:
            try:
                db.save_assessment(session['session_id'], session['assessment_data'])
            except Exception as e:
                print(f"Error saving to database: {e}")
        
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/calculate_risk', methods=['POST'])
def calculate_risk():
    try:
        # Get final assessment data
        final_data = request.get_json()
        
        # Ensure session ID exists
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())
        
        if 'assessment_data' not in session:
            session['assessment_data'] = {}
        
        session['assessment_data'].update(final_data)
        session.modified = True
        
        # Validate data
        validator = DataValidationAgent()
        is_valid, message = validator.validate(session['assessment_data'])
        
        if not is_valid:
            return jsonify({'error': message}), 400
        
        # Calculate risk
        risk_agent = RiskCalculationAgent()
        risk_result = risk_agent.analyze(session['assessment_data'])
        
        # Generate AI explanation
        explanation_agent = GeminiExplanationAgent()
        ai_explanation = explanation_agent.explain_risk(session['assessment_data'], risk_result)
        
        # Store results in session
        session['risk_result'] = risk_result
        session['ai_explanation'] = ai_explanation
        session.modified = True
        
        # Save to database
        if db:
            try:
                db.save_assessment(
                    session['session_id'], 
                    session['assessment_data'], 
                    risk_result, 
                    ai_explanation
                )
            except Exception as e:
                print(f"Error saving risk result to database: {e}")
        
        return jsonify({
            'risk_result': risk_result,
            'ai_explanation': ai_explanation
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/results')
def results():
    # Try to load data from database first
    risk_result = None
    ai_explanation = None
    assessment_data = None
    
    if 'session_id' in session and db:
        try:
            stored_data = db.get_assessment(session['session_id'])
            if stored_data:
                risk_result = stored_data.get('risk_result')
                ai_explanation = stored_data.get('ai_explanation')
                assessment_data = stored_data.get('assessment_data')
        except Exception as e:
            print(f"Error loading results from database: {e}")
    
    # Fallback to session data if database fails or no data found
    if not risk_result and 'risk_result' in session:
        risk_result = session.get('risk_result', {})
        ai_explanation = session.get('ai_explanation', 'No explanation available.')
        assessment_data = session.get('assessment_data', {})
    
    # Redirect if no data found
    if not risk_result or 'total_score' not in risk_result:
        return redirect(url_for('assessment'))
    
    return render_template('results.html', 
                         risk_result=risk_result,
                         ai_explanation=ai_explanation,
                         assessment_data=assessment_data)

@app.route('/export_summary')
def export_summary():
    if 'risk_result' not in session:
        return redirect(url_for('assessment'))
    
    # Create text summary
    summary = f"""
ALZHEIMER'S RISK ASSESSMENT SUMMARY
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

OVERALL RISK SCORE: {session['risk_result']['total_score']}/100
RISK LEVEL: {session['risk_result']['risk_level']}

RISK FACTOR BREAKDOWN:
"""
    
    for factor, score in session['risk_result']['factor_breakdown'].items():
        summary += f"- {factor.replace('_', ' ').title()}: {score:.1f} points\n"
    
    summary += f"\nAI RECOMMENDATIONS:\n{session['ai_explanation']}"
    
    response = make_response(summary)
    response.headers["Content-Disposition"] = "attachment; filename=alzheimer_risk_assessment.txt"
    response.headers["Content-Type"] = "text/plain"
    
    return response

@app.route('/admin/assessments')
def admin_assessments():
    """Admin route to view all assessments (for development/debugging purposes)"""
    if not db:
        return jsonify({'error': 'Database not available'}), 500
    
    try:
        assessments = db.get_all_assessments(limit=50)
        return render_template('admin_assessments.html', assessments=assessments)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/export_pdf')
def export_pdf():
    if 'risk_result' not in session:
        return redirect(url_for('assessment'))
    
    # Create PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title = Paragraph("Alzheimer's Risk Assessment Report", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))
    
    # Date
    date_text = f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    story.append(Paragraph(date_text, styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Risk Score
    score_text = f"<b>Overall Risk Score:</b> {session['risk_result']['total_score']}/100"
    story.append(Paragraph(score_text, styles['Normal']))
    
    level_text = f"<b>Risk Level:</b> {session['risk_result']['risk_level']}"
    story.append(Paragraph(level_text, styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Risk Factor Breakdown
    story.append(Paragraph("<b>Risk Factor Breakdown:</b>", styles['Heading2']))
    for factor, score in session['risk_result']['factor_breakdown'].items():
        factor_text = f"• {factor.replace('_', ' ').title()}: {score:.1f} points"
        story.append(Paragraph(factor_text, styles['Normal']))
    
    story.append(Spacer(1, 12))
    
    # AI Recommendations
    story.append(Paragraph("<b>AI Recommendations:</b>", styles['Heading2']))
    story.append(Paragraph(session['ai_explanation'], styles['Normal']))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    
    response = make_response(buffer.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=alzheimer_risk_assessment.pdf"
    response.headers["Content-Type"] = "application/pdf"
    
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
