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
        
    # Create driver file for testing
    driver_name = os.path.basename(driver_template_path)
    with open(driver_name, 'r+') as f:

        # Obtain case to replace
        case = sys.stdin.readlines()
        driver_contents.replace('{{case}}', case)
            
        # Obtain code to link driver to solution file
        link = sys.argv[2]
        driver_contents.replace('{{link}}', link)

        f.write(driver_contents)

    os.system(sys.argv[3])
