import sys
import glob
import py_compile
import subprocess
import os

def compile_all():
    print("1. Compiling Python files for syntax errors...")
    success = True
    # Search all python files in the app folder
    for filepath in glob.iglob('**/*.py', recursive=True):
        # SKIP venv files to avoid checking third-party packages
        normalized_path = filepath.replace(os.sep, '/')
        if '.venv/' in normalized_path or 'venv/' in normalized_path:
            continue
        try:
            py_compile.compile(filepath, doraise=True)
        except py_compile.PyCompileError as e:
            print(f"[ERROR] Syntax Error in {filepath}:\n{e}")
            success = False
    return success

def run_tests():
    print("\n2. Running test suite...")
    # Runs the unittest suite (tests is a folder right next to check_project.py)
    result = subprocess.run([
        sys.executable, "-m", "unittest", "discover", 
        "-s", "tests", "-p", "test_*.py"
    ])
    return result.returncode == 0

if __name__ == "__main__":
    compilation_passed = compile_all()
    
    if not compilation_passed:
        print("\n[ERROR] PRE-DEPLOYMENT CHECK FAILED: Syntax errors found.")
        sys.exit(1)
        
    print("[OK] Compilation passed successfully.")
    
    tests_passed = run_tests()
    
    if not tests_passed:
        print("\n[ERROR] PRE-DEPLOYMENT CHECK FAILED: Test suite failed.")
        sys.exit(1)
        
    print("\n[SUCCESS] ALL PRE-DEPLOYMENT CHECKS PASSED SUCCESSFULLY!")
    sys.exit(0)
