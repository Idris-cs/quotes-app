#!/usr/bin/env python
"""
Setup script for Quotes App
Provides interactive setup for database and configuration
"""

import os
import sys
import subprocess

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_success(text):
    """Print success message"""
    print(f"✅ {text}")

def print_info(text):
    """Print info message"""
    print(f"ℹ️  {text}")

def print_error(text):
    """Print error message"""
    print(f"❌ {text}")

def check_python():
    """Check Python version"""
    print_header("Checking Python Version")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print_success(f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_error(f"Python 3.8+ required, found {version.major}.{version.minor}")
        return False

def create_venv():
    """Create virtual environment"""
    print_header("Setting Up Virtual Environment")
    
    if os.path.exists("venv"):
        print_info("Virtual environment already exists")
        return True
    
    try:
        subprocess.check_call([sys.executable, "-m", "venv", "venv"])
        print_success("Virtual environment created")
        return True
    except subprocess.CalledProcessError:
        print_error("Failed to create virtual environment")
        return False

def install_packages():
    """Install required packages"""
    print_header("Installing Python Packages")
    
    # Get pip executable
    if os.name == 'nt':  # Windows
        pip_exe = os.path.join("venv", "Scripts", "pip.exe")
    else:  # macOS/Linux
        pip_exe = os.path.join("venv", "bin", "pip")
    
    try:
        subprocess.check_call([pip_exe, "install", "-r", "requirements.txt"])
        print_success("Packages installed successfully")
        return True
    except subprocess.CalledProcessError:
        print_error("Failed to install packages")
        return False

def setup_env():
    """Setup .env file"""
    print_header("Configuring Environment")
    
    if os.path.exists(".env"):
        print_info(".env file already exists")
        return True
    
    if os.path.exists(".env.example"):
        try:
            with open(".env.example", "r") as src:
                content = src.read()
            with open(".env", "w") as dst:
                dst.write(content)
            print_success(".env file created from .env.example")
            return True
        except Exception as e:
            print_error(f"Failed to create .env: {e}")
            return False
    
    return True

def test_db():
    """Test database connection (Postgres/Supabase)"""
    print_header("Testing Database Connection")

    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print_info("No DATABASE_URL provided; skipping remote DB test")
        return True

    try:
        import psycopg2
        print_success("psycopg2 is installed")

        # psycopg2 can accept a connection URI
        conn_url = db_url
        if conn_url.startswith('postgres://'):
            conn_url = conn_url.replace('postgres://', 'postgresql://', 1)

        try:
            conn = psycopg2.connect(conn_url)
            conn.close()
            print_success("Connected to database successfully")
            return True
        except Exception as e:
            print_info("Could not connect to the database with provided DATABASE_URL")
            print_info(f"Error: {e}")
            return True  # Not critical
    except ImportError:
        print_error("psycopg2 not installed")
        return False

def show_next_steps():
    """Show next steps"""
    print_header("Next Steps")
    
    print("""
1. Update Database Credentials (if needed):
   - Edit: config.py
   - Set: DATABASE_URL (Supabase/Postgres connection string)

2. Using Supabase (recommended for Vercel deployments):
   - Create a Supabase project at https://app.supabase.com
   - Copy the "Connection string" and set it as `DATABASE_URL` in your Vercel project environment variables

3. Activate Virtual Environment:
   Windows: venv\\Scripts\\activate
   macOS/Linux: source venv/bin/activate

4. Initialize Database:
   python init_db.py

5. Run Application:
   python run.py

6. Open in Browser:
   http://localhost:5000

""")

def main():
    """Main setup process"""
    print_header("Quotes App - Setup Wizard")
    
    steps = [
        ("Python Version", check_python),
        ("Virtual Environment", create_venv),
        ("Python Packages", install_packages),
        ("Environment Config", setup_env),
        ("Database Connection", test_db),
    ]
    
    passed = 0
    for step_name, step_func in steps:
        print_info(f"Running: {step_name}")
        if step_func():
            passed += 1
        else:
            print_error(f"Failed: {step_name}")
    
    print_header("Setup Summary")
    print(f"Completed: {passed}/{len(steps)} steps")
    
    if passed == len(steps):
        print_success("Setup completed successfully!")
        show_next_steps()
    else:
        print_error("Setup failed. Please fix issues and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()
