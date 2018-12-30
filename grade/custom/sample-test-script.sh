# Below is an outline of how to write a custom script

submission_path=../submission

# Step 1.
# The current directoy is 'autograder', 
# some test files may need to be linked into the submission folder
ln -sf TEST_FILES $submission_path

# Step 2.
# Move into the submission folder
cd $submission_path

# Step 3.
# Let's assume the submission is called 'submission.py'
# and we have a script to convert output to Kodethon's expected output called 'adapter.py'
#   a. Run the submission
#   b. Format the output to something Kodethon expects, see https://docs.kodethon.com/problems/custom.html
#   c. Write results to results.json
python submission.py | python adapter.py > results.json
