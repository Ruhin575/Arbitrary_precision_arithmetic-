import subprocess
import sys
import json

#function to call ant compile for compiling java files 
def compile_code():
    subprocess.run("ant compile", check=True, shell=True)

#function to call ant run for executing java classes
def run_arith(args):
    cmd = ["java", "-cp", "build", "MyInfArith"] + args
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        if "ArithmeticException" in e.stderr or "by zero" in e.stderr:
            return "Division by zero error"
        return f"[Java Error] {e.stderr.strip()}" if e.stderr else "Runtime error"

#function to run the test cases by calling the run function and comparing with expected results 
def run_tests():
    with open("testcases.json") as f:
        cases = json.load(f)
    for i, case in enumerate(cases):
        args = [case["type"], case["op"], case["a"], case["b"]]
        expected = case["expected"]
        actual = run_arith(args)
        result = "PASS" if actual == expected else "FAIL"
        print(f"[{result}] Test {i+1}")
        print(f"  Expected: {expected}")
        print(f"  Actual  : {actual}\n")

if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] in ("test", "--test"):
        compile_code()
        run_tests()
    else:
        compile_code()
        print(run_arith(sys.argv[1:]))
