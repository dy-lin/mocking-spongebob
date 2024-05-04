#!/usr/local/bin/bash
set -euo pipefail

# grab the html
html=/Users/dianalin/mocking-spongebob/files/connections.html
date_short=$(date '+%b%d')

month=$(date '+%B')
day=$(date '+%e' | gsed 's/^ //')
year=$(date '+%Y')

# url_date=$(date '+%B-%-d-%Y')
url_date=${month,,}-${day}-${year}
base_url=https://mashable.com/article/nyt-connections-hint-answer-today

urls_to_try=( ${base_url}-${url_date} ${base_url}-${month,,}-${day} )
if [[ ! -f "/Users/dianalin/mocking-spongebob/temp/connections_${date_short}" ]]; then

	for url in "${urls_to_try[@]}"; do 
		curl -o $html ${url} 2>/dev/null

		if [[ "$(grep -wc '404' $html)" -eq 0 ]]; then
			break
		fi
	done
fi

if [[ "$(grep -wc '404' $html)" -gt 0 ]]; then
	echo NULL
	exit 0
else
	touch /Users/dianalin/mocking-spongebob/temp/connections_${date_short} 
	rm -f $(ls /Users/dianalin/mocking-spongebob/temp/connections_* | grep -v ${date_short}) 2> /dev/null
fi

# grab panagrams
hints=$(grep -m1 'Yellow:' $html | awk -F "<strong>|</strong>" 'BEGIN{OFS="\n"} {print $2, $4, $6, $8}' | gsed 's|</\?[0-9a-z=" :-]\+>||g' | gsed '1s/^/**Yellow:** ||/' | gsed '2s/^/**Green:** ||/' | gsed '3s/^/**Blue:** ||/' | gsed '4s/^/**Purple:** ||/' | gsed 's/, /||   ||/g' | gsed '/^$/d' | gsed 's/$/||/' | gsed 's/^/- /')
categories=$(grep 'extra help' $html | awk -F "categories:" '{print $2}' | gsed 's|</\?[a-oq-z0-9]\+>||g' | awk -F "Looking for Wordle"  '{print $1}' |gsed 's|</p><p>|\n|g' | gsed '/^$/d' | gsed 's/: /:** ||/' | gsed 's/^/- **/' | gsed 's/$/||/')
soln=$(grep 'What is the answer to' $html | grep -o '</strong>:* *[A-Z, ()]\+</p>' | gsed 's|</\?[a-z]\+>:\? \?||g' | gsed '1s/^/**Yellow:** ||/' | gsed '2s/^/**Green:** ||/' | gsed '3s/^/**Blue:** ||/' | gsed '4s/^/**Purple:** ||/' | gsed 's/, /||   ||/g' | gsed '/^$/d' | gsed 's/$/||/' | gsed 's/^/- /')
echo "# Hints:"
echo "$hints"
echo
echo "# Categories:"
echo "$categories"
echo
echo "# Answers:"
echo "$soln"
