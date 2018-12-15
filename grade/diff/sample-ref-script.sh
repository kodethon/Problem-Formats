# DEPRECATED

# Description:
# This test script will compare run the submission file with each input in the inputs folder
# and compare the output to the corresponding file in the output folder.

# Assumptions:
#   1. There is at least one file in the inputs folder 

cd ..
problem=$(basename "$(pwd)")
cd submission

autograder_path=~/$problem

# Copy reference 
cp -r "$autograder_path/.ref" .

cases_path=.cases
feedback_path=.feedback # path to store feedback
tmp_output_path=.tmp_output # path to store tmp output
ref_output_path=.ref_output # path to store ref output

score=0 # Student's score
max=0 # Max score

cat /dev/null > $feedback_path # reset output file

inputs_count=$(ls "$autograder_path/.inputs" | wc | awk '{print $1}')
args_count=$(ls "$autograder_path/.arguments" | wc | awk '{print $1}')

# Find which folder has more files
inputs=$(python -c "print 'inputs' if int($inputs_count) > int($args_count) else ''")

if [ -z "$inputs" ]; then
    files=$(ls "$autograder_path/.arguments")
else
    files=$(ls "$autograder_path/.inputs")
fi

for f in $files; do
    # Pass each input into the submission program and then diff the anwers
    argument=$(cat "$autograder_path/.arguments/$f" 2> /dev/null)
    input=$(ls "$autograder_path/.inputs/$f" 2> /dev/null)

    if [ -z "$input" ]; then
        o=$({{run_command}} $argument < /dev/null > $tmp_output_path 2>&1)
    else
        o=$({{run_command}} $argument < "$autograder_path/.inputs/$f" > $tmp_output_path 2>&1)
    fi

    if [ -z "$input" ]; then
        o=$({{run_ref_command}} $argument < /dev/null > ../$ref_output_path 2>&1)
    else
        o=$({{run_ref_command}} $argument < "$autograder_path/.inputs/$f" > ../$ref_output_path 2>&1)
    fi
    
    d=$(python "$autograder_path/.utils/compare.py" $tmp_output_path $ref_output_path)
    if [ -z "$d" ]; then
        echo "===== Failed test case $f =====" >> $feedback_path
        printf "Output:\n" >> $feedback_path
        cat $tmp_output_path >> $feedback_path
        printf "\n\n" >> $feedback_path

        comment=$(cat comments/$f 2> /dev/null)
        if [ "$comment" != "" ]; then
            printf "Comment: " >> $feedback_path
            cat comments/$f >> $feedback_path 2> /dev/null
            printf "\n\n" >> $feedback_path
        fi

        printf "0 1\n" >> $cases_path
    else
        score=$((score + 1))
        echo "===== Passed test case $f =====" >> $feedback_path
        printf "Output:\n" >> $feedback_path
        cat $tmp_output_path >> $feedback_path
        printf "\n\n" >> $feedback_path

        printf "1 1\n" >> $cases_path
    fi
    
    # Keep track of number of inputs
    max=$((max + 1))
done

echo "$score case(s) passed out of $max case(s)"  >> $feedback_path

# Use python to convert division return value to float
#grade=$(python -c "print float($score)/$max * 100")
python "$autograder_path/.utils/toJson.py" output "$(cat $feedback_path)" tests "$(cat $cases_path)"

