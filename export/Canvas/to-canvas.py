import sys
import csv
import os

if len(sys.argv) < 4:
    sys.exit("USAGE: python kodethon-to-canvas.py <KODETHON GRADES> <CANVAS GRADES CSV> <CANVAS ID TO EMAIL>")

kodethon_export = sys.argv[1]
relationship = sys.argv[2]
canvas_export = sys.argv[3]

assignment_name = ''
email_to_grade_table = {}
with open(kodethon_export) as f:
    header = f.readline()
    assignment_name = header.split(',')[1].strip()

    count = 0
    for line in f:
	columns = line.split(',')
	if len(columns) < 2:
	   print "Line %s in %s is bad..." % (count, kodethon_export)
	   continue
	email = columns[0].strip()
	grade = columns[1].strip()
        email_to_grade_table[email] = grade
        count += 1

id_to_email_table = {}
with open(relationship) as f:
    count = 0
    for line in f:
	columns = line.split(',')
	if len(columns) < 2:
	   print "Line %s in %s is bad..." % (count, relationship)
	   continue
	i = columns[0]
	email = columns[1]
        id_to_email_table[i] = email
        count += 1

res = []
with open(canvas_export) as f:
    header = f.readline()
    row = header.split(',')[0:4]
    row.append(assignment_name)
    res.append(','.join(row))
    next(f) # skip another one.
    csv_reader = csv.reader(f, delimiter=',')
    count = 0
    for columns in csv_reader:
	if len(columns) < 2:
	   print "Line %s in %s is bad..." % (count, canvas_export)
	   continue

	i = columns[1]
	if not i in id_to_email_table:
	    print "Missing %s in %s" % (i, relationship)
	    continue 

	email = id_to_email_table[i].strip()
	if not email in email_to_grade_table:
	    print "Missing %s in %s" % (email, kodethon_export)
	    continue
	grade = email_to_grade_table[email]
	row = columns[0:4]
	row[0] = '"%s"' % row[0]
	row.append(grade)
       	res.append(','.join(row) )
       	count += 1

print "\n".join(res)
