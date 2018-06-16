# Description:
# This test script will compare run the submission file with each input in the inputs folder
# and compare the output to the corresponding file in the output folder.

# Assumptions:
#   1. There is at least one file in the inputs folder 

python_bin=$(which python2.7)
if [ -z "$python_bin" ]; then
    python_bin=$(which python2)
    if [ -z "$python_bin" ]; then
        python_bin=python
    fi    
fi

# Move into correct folder
cd ..
if [ -z $1 ]; then
    problem=$(basename "$(pwd)")
else
    problem=$1
fi
cd submission

SUBMISSION_PATH=$(pwd)
AUTOGRADER_PATH=~/$problem/autograder
CASES_PATH=.cases
FEEDBACK_PATH=.feedback # path to store feedback
TMP_OUTPUT_PATH=.tmp_output # path to store tmp output
DIFF_PATH=.diff

cat /dev/null > $FEEDBACK_PATH # reset output file
touch $TMP_OUTPUT_PATH

# Set resource limits
BLOCK_SIZE=512
MEM_LIMIT=$(expr $(cat /sys/fs/cgroup/memory/memory.limit_in_bytes) / 4) 
NUM_CASES=$(ls "$AUTOGRADER_PATH/.answers" | wc | awk '{print $1}')

if [ "$NUM_CASES" -eq 0 ]; then
    $python_bin "$AUTOGRADER_PATH/.utils/toJson.py" \
        output 'Your submission was received but no test cases were found.' > results.json
    exit
fi

HARD_OUTPUT_LIMIT=25000000 # 25MB
SOFT_OUTPUT_LIMIT=$(expr 2000000 / $NUM_CASES)
if [ "$SOFT_OUTPUT_LIMIT" -gt 100000 ]; then 
    SOFT_OUTPUT_LIMIT=100000
fi
DIFF_LIMIT=$(expr 500000 / $NUM_CASES)

echo "Max virtual memory per test case: $MEM_LIMIT"
echo "Max diff size per test case: $DIFF_LIMIT\n"

# Run init command
init_command="{{init_command}}"
if [ -z "$init_command" ]; then
    echo "No init command detected....\n"
else
    echo "Running init command: $init_command\n"
    eval " $init_command"
fi

score=0 # Student's score
max=0 # Max score

# Begin testing
echo -n '[' > $CASES_PATH
files=$(ls "$AUTOGRADER_PATH/.answers" | sort -n) # Get all answer files from answer folder
for f in $files; do
    echo "~ Test case $f"

    # Keep track of number of inputs
    max=$((max + 1))  

    # Pass each input into the submission program and then diff the anwers
    argument=$(cat "$AUTOGRADER_PATH/.arguments/$f" 2> /dev/null)
    input=$(ls "$AUTOGRADER_PATH/.inputs/$f" 2> /dev/null)
    
    if [ -z "$input" ]; then
        command="{{run_command}} $argument < /dev/null > $TMP_OUTPUT_PATH 2>&1"
    else
        command="{{run_command}} $argument < \"$AUTOGRADER_PATH/.inputs/$f\" > $TMP_OUTPUT_PATH 2>&1"
    fi

    echo "Testing with: $command"
    full_command="ulimit -Sv $MEM_LIMIT; ulimit -f $(expr $HARD_OUTPUT_LIMIT / $BLOCK_SIZE); $command"
    timeout {{execution_time}}s sh -c "$full_command" 2> /dev/null
    test_exit_status=$?

    echo "Exit status: $test_exit_status"
    d='' # Set comparison variable to be empty
    if [ "$test_exit_status" -eq 124 ]; then
        >&2 echo "Test Case $f: Your program did not complete, some output may not be shown due to buffering."
    elif [ "$test_exit_status" -eq 139 ]; then
        # Check for exit status to see if memory limit was breached
        >&2 echo "Test Case $f: Your program used more than $(expr $MEM_LIMIT / 1024 / 1024)MB of virtual memory."
    elif [ "$test_exit_status" -eq 153 ]; then
       printf ' (truncated)' >> $TMP_OUTPUT_PATH
       >&2 echo "Test Case $f: Your program printed an unexpected amount of data, some output may be truncated."
    else
        # Compare if output is equal to the answer
        d=$($python_bin "$AUTOGRADER_PATH/.utils/compare.py" "$AUTOGRADER_PATH/.answers/$f" $TMP_OUTPUT_PATH)
    fi
        
    if [ -z "$d" ]; then
        printf "Incorrect"

        output_size=$(du -sb $TMP_OUTPUT_PATH | awk '{ print $1 }')
        answer_size=$(du -sb "$AUTOGRADER_PATH/.answers/$f" | awk '{ print $1 }')
        # If output is greater than output_size and greater than 2x the answer, trunc file
        if [ "$output_size" -gt "$SOFT_OUTPUT_LIMIT" ]; then 
            echo "\nSize of output is $output_size"
            if [ "$output_size" -gt "$(( $answer_size * 2 ))" ]; then
                echo "Truncating output to size $answer_size\n"

                truncate -s $(( $answer_size )) $TMP_OUTPUT_PATH
                printf ' (truncated)' >> $TMP_OUTPUT_PATH
            else
                echo "\n"
            fi
        else
            echo "\n"
        fi

        # Try to generate a diff, if it's too large, trunc it
        command="diff \"$AUTOGRADER_PATH/.answers/$f\" $TMP_OUTPUT_PATH > $DIFF_PATH"
        timeout 1s sh -c "ulimit -f $(expr $DIFF_LIMIT / $BLOCK_SIZE); $command" 2> /dev/null
       
        test_case_args="score 0 max_score 1 number $f"
        $python_bin "$AUTOGRADER_PATH/.utils/toJson.py" $test_case_args \
            output "$SUBMISSION_PATH/$TMP_OUTPUT_PATH" diff "$SUBMISSION_PATH/$DIFF_PATH" >> $CASES_PATH

        printf ',' >> $CASES_PATH
    else
        echo "Correct\n"
        score=$((score + 1))
        
        test_case_args="score 1 max_score 1 number $f"
        $python_bin "$AUTOGRADER_PATH/.utils/toJson.py" $test_case_args \
            output "$SUBMISSION_PATH/$TMP_OUTPUT_PATH" >> $CASES_PATH

        printf ',' >> $CASES_PATH
    fi 
done

echo "$score case(s) passed out of $max case(s)" >> $FEEDBACK_PATH
sed '$ s/.$//' $CASES_PATH > .cases_tmp
mv .cases_tmp $CASES_PATH
printf ']' >> $CASES_PATH

printf "\nTesting done... writing to results.json"
$python_bin "$AUTOGRADER_PATH/.utils/toJsonFromFile.py" output $FEEDBACK_PATH tests $CASES_PATH > results.json

# Clean-up
rm $CASES_PATH 2> /dev/null
rm $TMP_OUTPUT_PATH 2> /dev/null
rm $FEEDBACK_PATH 2> /dev/null
rm $DIFF_PATH 2> /dev/null
