import sys
import os

# ARG1 => driver template path
# ARG2 => link code
# ARG3 => run command

# e.g. /home/kodethon/driver.py "import solution" "python driver.py"

driver_template_path = sys.argv[1]
with open(driver_template_path) as f:
    # Obtain template contents
    driver_contents = f.read()

    # Obtain case to replace
    case = sys.stdin.read()
    driver_contents = driver_contents.replace('{{case}}', case)
        
    # Obtain solution code into test file 
    solution = sys.argv[2]
    if not os.path.exists(solution):
        raise Exception("Please name submission '%s'" % solution)

    with open(solution) as f:
        solution_contents = f.read()
        driver_contents = driver_contents.replace('{{inline}}', solution_contents)
        
    # Create file for testing
    driver_name = os.path.basename(driver_template_path)
    with open(driver_name, 'r+') as f:
        f.write(driver_contents)

    os.system(sys.argv[3])
