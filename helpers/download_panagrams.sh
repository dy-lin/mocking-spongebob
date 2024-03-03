#!/bin/bash
set -euo pipefail

# grab the html
html=/Users/dianalin/mocking-spongebob/files/panagrams.html
date_short=$(date '+%b%d')

if [[ ! -f "/Users/dianalin/mocking-spongebob/temp/bee_${date_short}" ]]; then
	curl -o $html https://www.sbsolver.com/answers 2>/dev/null
	touch /Users/dianalin/mocking-spongebob/temp/bee_${date_short} 
	rm -f $(ls /Users/dianalin/mocking-spongebob/temp/bee_* | grep -v ${date_short}) 2> /dev/null
fi

# grab today's date in the format wanted
today=$(date '+%B %-d, %Y')
bee_date=$(grep 'Spelling Bee for' $html | grep -o '>[A-z0-9, ]\+<' | tail -n1 | tr -d '>' | tr -d '<')

if [[ "$#" -eq 1 ]]; then
	if [[ "$1" == -* ]]; then
		end=$(echo "$1" | tr -d '-')
		soln=$(grep "sbsolver.com/h/" $html | grep -o "/[a-z]\+\"" | tr -d / | tr -d '"' | tr '[:lower:]' '[:upper:]' | grep "${end}$")
	else
		soln=$(grep "sbsolver.com/h/" $html | grep -o "/[a-z]\+\"" | tr -d / | tr -d '"' | tr '[:lower:]' '[:upper:]' | grep "^$1")
	fi
else
	soln=$(grep -m3 "<b>" $html | tail -n1 | grep -o '>[A-Z, ]\+<' | tr -d '>' | tr -d '<' | sed 's/, / /g' | sed 's/^\s\+//g' | sed 's/\s\+$//g')
fi

if [[ "$today" != "$bee_date" ]]; then
	echo "NULL"
else
	echo "$soln"
fi
