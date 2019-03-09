echo 'Removing...'
find * -newer .timestamp ! -name results.json -maxdepth 0 | xargs echo
find * -newer .timestamp ! -name results.json -maxdepth 0 | xargs rm -rf
