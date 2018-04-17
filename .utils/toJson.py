import json
import sys
import os

def toDict():
    output = {}
    num_args = len(sys.argv)
    for i in xrange(1, num_args - 1):
        if i % 2 == 1 and num_args > i + 1:
            val = sys.argv[i + 1]

            try:
                output[str(sys.argv[i])] = val.encode('utf-8').strip()
            except UnicodeDecodeError:
                output[str(sys.argv[i])] = val.encode('ISO-8859-1').strip()

    return output

if __name__ == "__main__":
    reload(sys)  
    sys.setdefaultencoding('utf-8')
    
    # For each arg pair...
    num_args = len(sys.argv)
    for i in xrange(1, num_args - 1):
        if i % 2 == 1 and num_args > i + 1:
            contents = sys.argv[i + 1] 

            # If the arg is a path, read its contents
            if os.path.isabs(sys.argv[i + 1]) and os.path.exists(sys.argv[i + 1]):
                fp = open(sys.argv[i + 1], 'r')
                contents = fp.read()

            try:
                sys.argv[i + 1] = contents.encode('utf-8')
            except UnicodeDecodeError:
                reload(sys)
                sys.setdefaultencoding('ISO-8859-1')
                sys.argv[i + 1] = contents

    sys.stdout.write(json.dumps(toDict()))
