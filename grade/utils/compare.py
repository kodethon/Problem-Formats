import sys
import re
import os

if len(sys.argv) != 3:
    sys.exit("USAGE: python compare.py PATH1 PATH2")

if not os.path.exists(sys.argv[1]):
    sys.exit("%s does not exists." % sys.argv[1])

if not os.path.exists(sys.argv[2]):
    sys.exit("%s does not exists." % sys.argv[2])

rstrip = False
if os.path.exists('__RSTRIP__'):
    rstrip = True

astrip = False
if os.path.exists('__ASTRIP__'):
    astrip = True

with open(sys.argv[1]) as f:
    answer = f.read()
    with open(sys.argv[2]) as f:
        content = f.read()

        if rstrip:
            content = content.rstrip()
            answer = answer.rstrip()
        elif astrip:
            content = content.replace(" ", '')
            content = content.replace("\t", '')
            content = content.replace("\n", '')
            answer = answer.replace(" ", '')
            answer = answer.replace("\t", '')
            answer = answer.replace("\n", '')
        
        last = len(answer) - 1
        if len(answer)> 0 and answer[0] == '/' and answer[last] == '/':
            # Handle regex
            r = answer[1:last]
            regex = re.compile(r)
            result = regex.search(content)
            
            if result:
                if len(result.string) == len(content):
                    print('1')
        else:
            if len(content) == len(answer) and content == answer:
                print('1')
