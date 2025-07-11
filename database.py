
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.database_url = os.environ.get('DATABASE_URL')
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable not set")
    
    @contextmanager
    def get_connection(self):
        conn = None
        try:
            conn = psycopg2.connect(self.database_url)
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()
    
    def create_tables(self):
        """Create necessary tables if they don't exist"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Create assessments table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS assessments (
                    id SERIAL PRIMARY KEY,
                    session_id VARCHAR(255) UNIQUE NOT NULL,
                    assessment_data JSONB NOT NULL,
                    risk_result JSONB,
                    ai_explanation TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create index on session_id for faster lookups
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_assessments_session_id 
                ON assessments(session_id)
            ''')
            
            conn.commit()
    
    def save_assessment(self, session_id, assessment_data, risk_result=None, ai_explanation=None):
        """Save or update assessment data"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO assessments (session_id, assessment_data, risk_result, ai_explanation)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (session_id) 
                DO UPDATE SET 
                    assessment_data = EXCLUDED.assessment_data,
                    risk_result = EXCLUDED.risk_result,
                    ai_explanation = EXCLUDED.ai_explanation,
                    updated_at = CURRENT_TIMESTAMP
            ''', (session_id, json.dumps(assessment_data), 
                  json.dumps(risk_result) if risk_result else None,
                  ai_explanation))
            
            conn.commit()
    
    def get_assessment(self, session_id):
        """Retrieve assessment data by session ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute('''
                SELECT assessment_data, risk_result, ai_explanation, created_at, updated_at
                FROM assessments 
                WHERE session_id = %s
            ''', (session_id,))
            
            result = cursor.fetchone()
            if result:
                return {
                    'assessment_data': result['assessment_data'],
                    'risk_result': result['risk_result'],
                    'ai_explanation': result['ai_explanation'],
                    'created_at': result['created_at'],
                    'updated_at': result['updated_at']
                }
            return None
    
    def update_risk_result(self, session_id, risk_result, ai_explanation):
        """Update risk result and AI explanation for existing assessment"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE assessments 
                SET risk_result = %s, ai_explanation = %s, updated_at = CURRENT_TIMESTAMP
                WHERE session_id = %s
            ''', (json.dumps(risk_result), ai_explanation, session_id))
            
            conn.commit()
    
    def get_all_assessments(self, limit=100):
        """Retrieve all assessments for admin purposes"""
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute('''
                SELECT id, session_id, assessment_data, risk_result, ai_explanation, 
                       created_at, updated_at
                FROM assessments 
                ORDER BY created_at DESC 
                LIMIT %s
            ''', (limit,))
            
            return cursor.fetchall()
