#!/usr/local/bin/bash
set -euo pipefail

# grab the html
html=/Users/dianalin/mocking-spongebob/files/connections.html
date_short=$(date '+%b%d')

url_date=$(date '+%B-%-d-%Y')
url=https://mashable.com/article/nyt-connections-hint-answer-today
if [[ ! -f "/Users/dianalin/mocking-spongebob/temp/connections_${date_short}" ]]; then
	curl -o $html ${url}-${url_date,,} 2>/dev/null
	touch /Users/dianalin/mocking-spongebob/temp/connections_${date_short} 
	rm -f $(ls /Users/dianalin/mocking-spongebob/temp/connections_* | grep -v ${date_short}) 2> /dev/null
fi

# grab today's date in the format wanted
today=$(date '+%B-%-d-%Y')

# grab panagrams
hints=$(grep -w try $html| awk -F "try:" '{print $2}' | gsed 's|</\?[0-9a-z=" :-]\+>||g' | gsed 's/Yellow: /**Yellow:** ||/' | gsed 's/Green: /\n**Green:** ||/' | gsed 's/Blue: /\n**Blue:** ||/' | gsed 's/Purple: /\n**Purple:** ||/' | gsed '/^$/d' | gsed 's/$/||/' | gsed 's/^/- /')
categories=$(grep 'extra help' $html | awk -F "categories:" '{print $2}' | gsed 's|</\?[a-oq-z0-9]\+>||g' | awk -F "Looking for Wordle"  '{print $1}' |gsed 's|</p><p>|\n|g' | gsed '/^$/d' | gsed 's/: /:** ||/' | gsed 's/^/- **/' | gsed 's/$/||/')
soln=$(grep 'What is the answer to' $html | grep -o '</strong>:* *[A-Z, ]\+</p>' | gsed 's|</\?[a-z]\+>:\? \?||g' | gsed '1s/^/**Yellow:** ||/' | gsed '2s/^/**Green:** ||/' | gsed '3s/^/**Blue:** ||/' | gsed '4s/^/**Purple:** ||/' | gsed 's/, /||   ||/g' | gsed '/^$/d' | gsed 's/$/||/' | gsed 's/^/- /')
if [[ "$today" != "$url_date" ]]; then
	echo "NULL"
else
	echo "# Hints:"
	echo "$hints"
	echo
	echo "# Categories:"
	echo "$categories"
	echo
	echo "# Answers:"
	echo "$soln"
fi
