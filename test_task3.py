import subprocess

# List of test cases with moves and user inputs
test_cases = [
    ("python task3.py rock paper scissors", ["0"]),
    ("python task3.py rock paper scissors", ["?"]),
    ("python task3.py rock paper scissors", ["1"]),
    ("python task3.py rock paper scissors", ["5"]),
    ("python task3.py rock paper", ["1"]),
    ("python task3.py rock paper paper scissors", ["2"]),
    ("python task3.py rock paper scissors lizard spock", ["3"]),
    ("python task3.py rock paper scissors lizard spock dragon wizard", ["4"]),
    ("python task3.py alpha beta gamma", ["1"]),
    ("python task3.py 1 2 3 4 5", ["2"]),
]


def run_test(command, inputs):
    process = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        text=True,
    )
    try:
        stdout, stderr = process.communicate(input="\n".join(inputs) + "\n", timeout=15)
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()

    return stdout, stderr


for i, (command, inputs) in enumerate(test_cases, start=1):
    print(f"Running test case {i}: {command}")
    print("Inputs:")
    for input_line in inputs:
        print(f"  {input_line}")
    stdout, stderr = run_test(command, inputs)

    if stdout:
        print("Output:")
        print(stdout)
    if stderr:
        print("Errors:")
        print(stderr)
    print("-" * 80)
