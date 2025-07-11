
from risk_calculator import AlzheimersRiskCalculator
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class DataValidationAgent:
    def validate(self, data):
        required_fields = [
            'age', 'gender', 'ethnicity', 'education', 'bmi', 'smoking', 
            'alcohol', 'physical_activity', 'diet', 'sleep', 'family_history',
            'cardiovascular', 'diabetes', 'depression', 'head_injury', 'hypertension'
        ]
        
        missing_fields = [field for field in required_fields if field not in data or data[field] == '']
        
        if missing_fields:
            return False, f"Missing required fields: {', '.join(missing_fields)}"
        
        # Validate ranges
        try:
            age = int(data['age'])
            if not (60 <= age <= 90):
                return False, "Age must be between 60 and 90 years"
            
            bmi = float(data['bmi'])
            if not (15 <= bmi <= 40):
                return False, "BMI must be between 15 and 40"
            
            alcohol = int(data['alcohol'])
            if not (0 <= alcohol <= 20):
                return False, "Weekly alcohol consumption must be between 0 and 20 units"
            
            physical_activity = int(data['physical_activity'])
            if not (0 <= physical_activity <= 10):
                return False, "Weekly physical activity must be between 0 and 10 hours"
            
            diet = int(data['diet'])
            if not (0 <= diet <= 10):
                return False, "Diet quality score must be between 0 and 10"
            
            sleep = int(data['sleep'])
            if not (4 <= sleep <= 10):
                return False, "Sleep quality score must be between 4 and 10"
                
        except ValueError:
            return False, "Invalid numeric values provided"
        
        return True, "All fields are valid"

class RiskCalculationAgent:
    def analyze(self, data):
        calculator = AlzheimersRiskCalculator(data)
        return calculator.calculate_total_risk()

class GeminiExplanationAgent:
    def __init__(self):
        self.openai_client = openai

    def explain_risk(self, patient_data, risk_result):
        try:
            prompt = f"""
            You are a medical expert specializing in Alzheimer's risk assessment. 
            Given the following patient data and calculated risk breakdown, explain the patient's risk level 
            and provide personalized recommendations in plain, empathetic language.

            Patient Data: {patient_data}
            Risk Assessment Result: {risk_result}

            Please provide:
            1. A brief summary of the main risk contributors
            2. 3-4 specific, actionable steps to reduce risk
            3. General cognitive health tips
            4. Encouraging words about prevention

            Keep the response under 300 words and use clear, non-technical language.
            """

            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a compassionate medical expert providing Alzheimer's risk assessment guidance."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"Based on your assessment, your risk level is {risk_result['risk_level']}. The main contributing factors include age and medical history. To reduce your risk, consider: 1) Regular physical exercise (150 minutes per week), 2) A Mediterranean-style diet rich in omega-3 fatty acids, 3) Quality sleep (7-9 hours nightly), 4) Mental stimulation through reading, puzzles, or learning new skills. Remember, many risk factors are modifiable, and taking proactive steps can significantly impact your cognitive health."
