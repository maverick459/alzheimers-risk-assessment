
#!/usr/bin/env python3
"""
Alzheimer's Risk Assessment App
Main entry point with dependency checking
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = [
        'flask',
        'openai', 
        'psycopg2',
        'reportlab',
        'numpy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"""
❌ Missing required packages: {', '.join(missing_packages)}

To install missing packages, run:
pip install {' '.join(missing_packages)}

Or use the setup script:
python setup.py install
        """)
        return False
    
    return True

def check_environment():
    """Check if required environment variables are set"""
    required_vars = ['OPENAI_API_KEY', 'DATABASE_URL', 'SECRET_KEY']
    missing_vars = []
    
    for var in required_vars:
        value = os.environ.get(var)
        if not value or 'your_' in value or value == f'{var.lower()}_here':
            missing_vars.append(var)
    
    if missing_vars:
        print(f"""
❌ Missing or incomplete environment variables: {', '.join(missing_vars)}
        """)
        return False
    
    return True

def main():
    """Main application entry point"""
    print("🧠 Starting Alzheimer's Risk Assessment App...")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check environment variables
    if not check_environment():
        sys.exit(1)
    
    # Import and run the Flask app
    try:
        from api.app import app
        print("✅ All checks passed! Starting Flask server...")
        print("🌐 Access the app at: http://localhost:5000")
        print("🔄 Press Ctrl+C to stop the server")
        print("-" * 50)
        
        app.run(host='0.0.0.0', port=5000, debug=True)
        
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
