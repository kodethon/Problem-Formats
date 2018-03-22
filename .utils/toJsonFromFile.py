import json
import sys

reload(sys)  
sys.setdefaultencoding('utf8')

output = {}
for i in xrange(1, len(sys.argv) - 1):
    if i % 2 == 1:
        if len(sys.argv) > i + 1:
            fp = contents = open(sys.argv[i + 1], 'r')
            contents = fp.read()
            output[str(sys.argv[i])] = contents.encode('utf-8').strip()
            fp.close()

sys.stdout.write(json.dumps(output))
