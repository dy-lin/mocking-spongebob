#!/usr/local/bin/bash

set -euo pipefail 
month=$(date '+%B')
day_year=$(date '+%d-%Y')
url_date=${month,,}-${day_year}

date_short=$(date '+%b%d')

url=https://www.thegamer.com/nyt-strands-answers-hints-${url_date}/
html=/Users/dianalin/mocking-spongebob/files/strands.html
if [[ ! -f "/Users/dianalin/mocking-spongebob/temp/strands_${date_short}" ]]; then
	curl -o $html $url 2> /dev/null
	touch /Users/dianalin/mocking-spongebob/temp/strands_${date_short}
	rm -rf $(ls /Users/dianalin/mocking-spongebob/temp/strands_* | grep -v ${date_short}) 2> /dev/null
fi

theme=$(grep 'theme is' $html | awk -F "<strong>|</strong>" '{print $2}' | gsed "s/&rsquo;/'/")
echo "$theme"

for i in "first" "second" "third" "fourth" "fifth" "sixth" "seventh"; do 
	if [[ "$i" == "seventh" ]]; then
		word=$(grep "${i} word" $html | tail -n1 | awk '{print $NF}' | gsed 's|</\?[a-z]\+>||g' | gsed 's/\.$//')
		hint=$(grep "${i} word" $html | head -n1 | gsed 's|</\?[a-z]\+>||g' | awk -F " is " '{print $2}' | gsed 's/^ \+//' | gsed 's/\.$//')
	else
		hint=$(grep "${i} word" $html | head -n1 |  gsed 's|</\?[a-z]\+>||g' | awk -F " word " '{print $2}' | gsed 's/\.$//' | gsed 's/^ \?is \?//')
		word=$(grep "${i} word" $html | tail -n1 | gsed 's|</\?[a-z]\+>||g' | awk -F " is " '{print $2}' | gsed 's/\.$//') 
	fi
	echo "${word}: ${hint}"
done

