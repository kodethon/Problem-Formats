from os.path import dirname, basename, isfile, join
import glob

modules = glob.glob(join(dirname(__file__), "*.py"))
reserved = ['_main.py', '__init__.py', 'driver.py']
for filename in [basename(f) for f in modules if isfile(f) and not f in reserved]:
    execfile(filename)

{{case}}
