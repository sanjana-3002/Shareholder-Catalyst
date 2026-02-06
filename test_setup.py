#!/usr/bin/env python3
"""
Setup Test Script
Verifies that your environment is configured correctly
"""

import os
import sys

def check_env_file():
    """Check if .env file exists and has API key"""
    print("🔍 Checking .env file...")
    
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("\nFix:")
        print("  1. Copy the example: cp .env.example .env")
        print("  2. Edit .env and add your OpenAI API key")
        print("  3. Get key from: https://platform.openai.com/api-keys")
        return False
    
    with open('.env', 'r') as f:
        content = f.read()
    
    if 'OPENAI_API_KEY=' not in content:
        print("❌ OPENAI_API_KEY not found in .env")
        return False
    
    # Extract key
    for line in content.split('\n'):
        if line.startswith('OPENAI_API_KEY='):
            key = line.split('=', 1)[1].strip()
            if key in ['', 'sk-proj-your-openai-api-key-here', 'your-openai-api-key-here']:
                print("❌ API key not set (still has placeholder value)")
                print("\nFix:")
                print("  1. Open .env in text editor")
                print("  2. Replace placeholder with your actual key")
                print("  3. Key should start with 'sk-proj-' or 'sk-'")
                return False
            print(f"✅ .env file exists with API key: {key[:12]}...")
            return True
    
    print("❌ Could not parse OPENAI_API_KEY from .env")
    return False

def check_dependencies():
    """Check if required packages are installed"""
    print("\n🔍 Checking dependencies...")
    
    required = ['openai', 'yfinance', 'requests', 'dotenv']
    missing = []
    
    for package in required:
        try:
            if package == 'dotenv':
                __import__('dotenv')
            else:
                __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package}")
            missing.append(package if package != 'dotenv' else 'python-dotenv')
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print(f"\nFix: pip install {' '.join(missing)}")
        return False
    
    return True

def check_api_key():
    """Test if OpenAI API key works"""
    print("\n🔍 Testing OpenAI API key...")
    
    try:
        from dotenv import load_dotenv
        import openai
        
        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            print("❌ API key not loaded from .env")
            return False
        
        client = openai.OpenAI(api_key=api_key)
        
        # Test API call
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": "Say 'test'"}],
            max_tokens=5
        )
        
        print("✅ OpenAI API key is valid and working!")
        return True
        
    except Exception as e:
        error_str = str(e).lower()
        print(f"❌ API test failed: {str(e)[:100]}")
        
        if 'authentication' in error_str or 'api key' in error_str:
            print("\nFix: Check that your API key is correct")
        elif 'insufficient' in error_str or 'quota' in error_str:
            print("\nFix: Add credits to your OpenAI account")
            print("  Go to: https://platform.openai.com/settings/organization/billing")
        elif 'rate limit' in error_str:
            print("\nFix: Wait a minute and try again")
        
        return False

def check_project_structure():
    """Check if project files exist"""
    print("\n🔍 Checking project structure...")
    
    required_files = [
        'orchestrator.py',
        'requirements.txt',
        'agents/analyst_agent.py',
        'agents/governance_agent.py',
        'agents/thesis_generator.py',
        'tools/sec_fetcher.py',
        'tools/ade_extractor.py',
        'tools/market_data.py'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file}")
            all_exist = False
    
    if not all_exist:
        print("\n❌ Some project files are missing")
        print("Make sure you extracted the entire archive")
        return False
    
    return True

def main():
    print("\n" + "="*60)
    print("  SHAREHOLDER CATALYST - SETUP TEST".center(60))
    print("="*60 + "\n")
    
    results = []
    
    # Run checks
    results.append(("Project Structure", check_project_structure()))
    results.append(("Dependencies", check_dependencies()))
    results.append((".env File", check_env_file()))
    results.append(("OpenAI API Key", check_api_key()))
    
    # Summary
    print("\n" + "="*60)
    print("  RESULTS SUMMARY".center(60))
    print("="*60)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {name}: {status}")
    
    print("="*60 + "\n")
    
    if all(r[1] for r in results):
        print("🎉 ALL CHECKS PASSED!")
        print("\nYou're ready to run:")
        print("  python orchestrator.py AAPL")
        print("\nThis will generate a complete activist investment thesis!")
        return 0
    else:
        print("⚠️  SOME CHECKS FAILED")
        print("\nFix the issues above, then run this test again:")
        print("  python test_setup.py")
        return 1

if __name__ == "__main__":
    sys.exit(main())
