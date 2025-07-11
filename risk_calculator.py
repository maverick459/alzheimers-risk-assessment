
import numpy as np

class AlzheimersRiskCalculator:
    def __init__(self, patient_data):
        self.data = patient_data
        self.weights = {
            'age': 0.25,
            'medical_history': 0.30,
            'lifestyle': 0.20,
            'education': 0.12,
            'gender': 0.08,
            'ethnicity': 0.05
        }
        self.risk_factors = {}

    def score_age(self):
        age = int(self.data.get('age', 60))
        if age < 65:
            score = 0.1 * (age - 60)
        else:
            score = 0.5 + 0.05 * (age - 65)
        
        score = np.clip(score, 0, 1)
        self.risk_factors['age'] = score * 100 * self.weights['age']
        return self.risk_factors['age']

    def score_medical_history(self):
        # Family history (40% of medical weight)
        family_history = 1 if self.data.get('family_history') == 'yes' else 0
        
        # Chronic conditions (60% of medical weight)
        conditions = ['cardiovascular', 'diabetes', 'depression', 'head_injury', 'hypertension']
        condition_count = sum(1 for condition in conditions if self.data.get(condition) == 'yes')
        condition_score = min(condition_count / len(conditions), 1)
        
        medical_score = (family_history * 0.4 + condition_score * 0.6)
        self.risk_factors['medical_history'] = medical_score * 100 * self.weights['medical_history']
        return self.risk_factors['medical_history']

    def score_lifestyle(self):
        # BMI scoring (20% of lifestyle weight)
        bmi = float(self.data.get('bmi', 25))
        if bmi < 18.5 or bmi > 30:
            bmi_score = 0.8
        elif bmi > 25:
            bmi_score = 0.4
        else:
            bmi_score = 0.1
        
        # Smoking (25% of lifestyle weight)
        smoking_score = 0.9 if self.data.get('smoking') == 'yes' else 0.1
        
        # Alcohol (15% of lifestyle weight)
        alcohol = int(self.data.get('alcohol', 0))
        alcohol_score = min(alcohol / 20, 1) if alcohol > 7 else 0.1
        
        # Physical activity (20% of lifestyle weight)
        activity = int(self.data.get('physical_activity', 0))
        activity_score = max(0.1, 1 - (activity / 10))
        
        # Diet quality (10% of lifestyle weight)
        diet = int(self.data.get('diet', 5))
        diet_score = max(0.1, 1 - (diet / 10))
        
        # Sleep quality (10% of lifestyle weight)
        sleep = int(self.data.get('sleep', 7))
        sleep_score = max(0.1, 1 - ((sleep - 4) / 6))
        
        lifestyle_score = (bmi_score * 0.2 + smoking_score * 0.25 + alcohol_score * 0.15 + 
                          activity_score * 0.2 + diet_score * 0.1 + sleep_score * 0.1)
        
        self.risk_factors['lifestyle'] = lifestyle_score * 100 * self.weights['lifestyle']
        return self.risk_factors['lifestyle']

    def score_education(self):
        education_levels = {'none': 1.0, 'high_school': 0.6, 'bachelors': 0.3, 'higher': 0.1}
        education = self.data.get('education', 'high_school')
        education_score = education_levels.get(education, 0.6)
        
        self.risk_factors['education'] = education_score * 100 * self.weights['education']
        return self.risk_factors['education']

    def score_gender(self):
        # Women have slightly higher risk
        gender_score = 0.6 if self.data.get('gender') == 'female' else 0.4
        self.risk_factors['gender'] = gender_score * 100 * self.weights['gender']
        return self.risk_factors['gender']

    def score_ethnicity(self):
        ethnicity_risks = {
            'caucasian': 0.5,
            'african_american': 0.7,
            'asian': 0.3,
            'other': 0.5
        }
        ethnicity = self.data.get('ethnicity', 'other')
        ethnicity_score = ethnicity_risks.get(ethnicity, 0.5)
        
        self.risk_factors['ethnicity'] = ethnicity_score * 100 * self.weights['ethnicity']
        return self.risk_factors['ethnicity']

    def calculate_total_risk(self):
        self.score_age()
        self.score_medical_history()
        self.score_lifestyle()
        self.score_education()
        self.score_gender()
        self.score_ethnicity()
        
        total_score = sum(self.risk_factors.values())
        
        if total_score < 30:
            risk_level = 'Low'
        elif total_score < 60:
            risk_level = 'Moderate'
        else:
            risk_level = 'High'
        
        return {
            'total_score': round(total_score, 1),
            'risk_level': risk_level,
            'factor_breakdown': {k: round(v, 1) for k, v in self.risk_factors.items()}
        }
