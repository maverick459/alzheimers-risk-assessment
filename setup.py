
#!/usr/bin/env python3
"""
Setup script for Alzheimer's Risk Assessment App
"""
import os
import sys
import subprocess

def install_dependencies():
    """Install required Python packages"""
    print("Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "psycopg2-binary"], check=True)
        print("✓ psycopg2-binary installed")
        
        subprocess.run([sys.executable, "-m", "pip", "install", "flask"], check=True)
        print("✓ Flask installed")
        
        subprocess.run([sys.executable, "-m", "pip", "install", "openai"], check=True)
        print("✓ OpenAI installed")
        
        subprocess.run([sys.executable, "-m", "pip", "install", "python-dotenv"], check=True)
        print("✓ python-dotenv installed")
        
        subprocess.run([sys.executable, "-m", "pip", "install", "reportlab"], check=True)
        print("✓ ReportLab installed")
        
        print("\n✅ All dependencies installed successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False
    
    return True

def check_env_file():
    """Check if .env file exists and has required variables"""
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("Please create a .env file with the following variables:")
        print("- OPENAI_API_KEY")
        print("- DATABASE_URL") 
        print("- SECRET_KEY")
        return False
    
    # Check for required environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = ['OPENAI_API_KEY', 'DATABASE_URL', 'SECRET_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.environ.get(var) or 'your_' in os.environ.get(var, ''):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing or incomplete environment variables: {', '.join(missing_vars)}")
        print("Please update your .env file with actual values.")
        return False
    
    print("✅ Environment variables configured")
    return True

def run_app():
    """Run the Flask application"""
    print("Starting Flask application...")
    try:
        from app import app
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        print(f"❌ Error running app: {e}")
        return False

if __name__ == "__main__":
    print("🧠 Alzheimer's Risk Assessment App Setup")
    print("=" * 50)
    
    if len(sys.argv) > 1 and sys.argv[1] == "install":
        install_dependencies()
    elif len(sys.argv) > 1 and sys.argv[1] == "run":
        if check_env_file():
            run_app()
    else:
        print("Usage:")
        print("  python setup.py install  - Install dependencies")
        print("  python setup.py run      - Run the application")
        print("  python main.py           - Run directly (after setup)")
