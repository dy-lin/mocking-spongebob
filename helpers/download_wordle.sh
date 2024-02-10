#!/usr/local/bin/bash
set -euo pipefail

# grab the html
html=/Users/dianalin/mocking-spongebob/files/wordle.html
date_short=$(date '+%b%d')

url_date=$(date '+%B-%-d-%Y')
url=https://mashable.com/article/wordle-today-answer
if [[ ! -f "/Users/dianalin/mocking-spongebob/temp/wordle_${date_short}" ]]; then
	curl -o $html ${url}-${url_date,,} 2>/dev/null
	touch /Users/dianalin/mocking-spongebob/temp/wordle_${date_short} 
	rm -f $(ls /Users/dianalin/mocking-spongebob/temp/wordle_* | grep -v ${date_short}) 2> /dev/null
fi

# grab today's date in the format wanted
today=$(date '+%B-%-d-%Y')

# grab panagrams
hints=$(grep 'subtle hint'  $html | grep -o "<p>[A-z.<>/' ]\+</p>" | gsed 's|<[pem/]\+>||g')
soln=$(grep 'solution'  $html | tail -n1| grep -o '<strong>[A-Z.]\+</strong>' | gsed 's|</\?strong>||g' | tr -d '.' )

if [[ "$today" != "$url_date" ]]; then
	echo "NULL"
else
	echo "$hints"
	echo "$soln"
fi
