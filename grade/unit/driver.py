import sys
import os

# ARG1 => driver template path
# ARG2 => link code
# ARG3 => run command

# e.g. /home/kodethon/driver.py "import solution" "python driver.py"

class CommandFactory():

    def get(self, filename):
        toks = filename.split('.')
        ext = toks[1]
        switcher = {
            'cpp': self.get_c_command,
            'js': self.get_javascript_command,
            'py': self.get_python_command,
            'rb': self.get_ruby_command,
            'php': self.get_php_command,
            'lisp': self.get_lisp_command,
            'prolog': self.get_prolog_command,
            'rs': self.get_rust_command,
            'java': self.get_java_command
        }
        func = switcher.get(ext, lambda: "Invalid file extension.")
        return func(filename)
  
    def get_ruby_command(self, filename):
        rb_interpreter = 'ruby'
        return ' '.join([rb_interpreter, filename])

    def get_prolog_command(self, filename):
        prolog_interpreter = 'gprolog'
        return ' '.join([prolog_interpreter, '--consult-file', path])
        
    def get_lisp_command(self,filename):
        lisp_interpreter = 'clisp'
        return ' '.join([lisp_interpreter, filename])

    def get_python_command(self, filename):
        py_interpreter = 'python'
        return ' '.join([py_interpreter, filename])

    def get_php_command(self,filename):
        php_interpreter = 'php'
        return ' '.join([php_interpreter, filename])

    def get_javascript_command(self, filename):
        js_interpreter = 'node'
        return ' '.join([js_interpreter, filename])

    def get_java_command(self, filename):
        java_interpreter = 'java' 
        toks = filename.split('.')
        filename_without_ext = toks[0]
        return ' '.join(['javac *.java', '&&', java_interpreter, filename_without_ext])

    def get_c_command(self, filename):
        header_file = 'all_headers.h'
        if not os.path.exists(header_file):
            self.build_c_header_file(header_file)
        self.check_if_c_submission(filename)

        return ' '.join(['make', '&&', './a.out'])

    def get_rust_command(self, filename):
        compiler = 'rustc'
        toks = filename.split('.')
        filename_without_ext = toks[0]
        return ' '.join([compiler, filename, '&&', "./%s" % filename_without_ext])

    def build_c_header_file(self, header_file):
        with open(header_file, 'w+') as f:
            f.write("#ifndef __ALL_HEADERS__\n")
            f.write("#define __ALL_HEADERS__\n")
            for filename in os.listdir('.'):  
                if not filename.endswith(".h"):
                    continue
                f.write('#include "' + filename + '"\n')
            f.write("#endif")
    
    def check_if_c_submission(self, source):
        for filename in os.listdir('.'):  
            if filename.endswith(".c"):
                toks = source.split('.')
                filename_without_ext = toks[0]
                os.rename(source, "%s.c" % filename_without_ext)
                break


driver_template_path = sys.argv[1]
with open(driver_template_path) as f:
    # Obtain template contents
    driver_contents = f.read()

    # Obtain case to replace
    case = sys.stdin.read()
    driver_contents = driver_contents.replace('{{case}}', case)
    
    '''
    # Obtain solution code into test file 
    solution = sys.argv[2]
    if not os.path.exists(solution):
        raise Exception("Please name submission '%s'" % solution)

    with open(solution) as f:
        solution_contents = f.read()
        driver_contents = driver_contents.replace('{{inline}}', solution_contents)
    '''
        
    # Create file for testing
    driver_name = sys.argv[2]
    with open(driver_name, 'w+') as f:
        f.write(driver_contents)
    run_command = CommandFactory().get(driver_name)
    os.system(run_command)
