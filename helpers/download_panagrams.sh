#!/bin/bash
set -euo pipefail

# grab the html
# html=/Users/dianalin/mocking-spongebob/files/panagrams.html
# date_short=$(date '+%b%d')
# 
# if [[ ! -f "/Users/dianalin/mocking-spongebob/temp/bee_${date_short}" ]]; then
# 	curl -o $html https://www.sbsolver.com/answers 2>/dev/null
# 	touch /Users/dianalin/mocking-spongebob/temp/bee_${date_short} 
# 	rm -f $(ls /Users/dianalin/mocking-spongebob/temp/bee_* | grep -v ${date_short}) 2> /dev/null
# fi

# indicates a date! 
today=false
if [[ "$#" -gt 0 ]]; then 
	if [[ $1 =~ ^[0-9] ]]; then
		requested_date=$1
		shift
	else
		requested_date=$(date '+%Y-%m-%d')
		today=true
	fi
else
	requested_date=$(date '+%Y-%m-%d')
	today=true
fi

requested_date_long=$(date -j -f '%Y-%m-%d' ${requested_date} '+%B %-d, %Y')

date_short=$(date -j -f "%Y-%m-%d" ${requested_date} '+%b%d')

arr=( $(echo "${requested_date}" | awk -F "-" '{print $1, $2, $3}')  )
html=/Users/dianalin/mocking-spongebob/temp/bee_${arr[1]}${arr[0]}.html

if [[ ! -f "$html" ]]; then
	curl -o $html https://www.sbsolver.com/archive/${arr[0]}/${arr[1]} 2> /dev/null
fi

if [[ "$today" == false ]]; then
	url=$(grep "<button>${arr[2]}</button>" $html | awk -F "href=" '{print $2}' | awk '{print $1}' | tr -d '"')
else
	url=https://sbsolver.com/answers
fi
rm $html

html=/Users/dianalin/mocking-spongebob/files/bee_${date_short}.html

if [[ ! -f $html ]]; then
	curl -o $html $url 2> /dev/null
fi

bee_date=$(grep 'Spelling Bee for' $html | grep -o '>[A-z0-9, ]\+<' | tail -n1 | tr -d '>' | tr -d '<')

if [[ "$#" -eq 1 ]]; then
	if [[ "$1" == -* ]]; then
		end=$(echo "$1" | tr -d '-')
		soln=$(grep "sbsolver.com/h/" $html | grep -o "/[a-z]\+\"" | tr -d / | tr -d '"' | tr '[:lower:]' '[:upper:]' | grep "${end}$")
	else
		soln=$(grep "sbsolver.com/h/" $html | grep -o "/[a-z]\+\"" | tr -d / | tr -d '"' | tr '[:lower:]' '[:upper:]' | grep "^$1")
	fi
else
	soln=$(grep -m3 "<b>" $html | tail -n1 | grep -o '>[A-Z, ]\+<' | tr -d '>' | tr -d '<' | sed 's/, / /g' | sed 's/^\s\+//g' | sed 's/\s\+$//g' | tr ' ' $'\n' | sed '/^$/d')
fi


if [[ "$requested_date_long" != "$bee_date" ]]; then
	echo "NULL"
else
	echo "$soln"
fi
