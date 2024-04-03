#!/usr/local/bin/bash

set -euo pipefail 
month=$(date '+%B')
# day_year=$(date '+%d-%Y')
day=$(date '+%e' | gsed 's/^ //')
year=$(date '+%Y')
url_date=${month,,}-${day}-${year}

date_short=$(date '+%b%d')
url=https://www.thegamer.com/nyt-strands-answers-hints-${url_date}/
html=/Users/dianalin/mocking-spongebob/files/strands.html
if [[ ! -f "/Users/dianalin/mocking-spongebob/temp/strands_${date_short}" ]]; then
	curl -o $html $url 2> /dev/null

	if [[ "$(grep -wc '404' $html)" -gt 0 ]]; then
		url=https://www.thegamer.com/nyt-strands-answers-and-hints-${url_date}/
		curl -o $html $url 2> /dev/null
		if [[ "$(grep -wc '404' $html)" -gt 0 ]]; then
			echo NULL
			exit 0 
		fi
	fi
	touch /Users/dianalin/mocking-spongebob/temp/strands_${date_short}
	rm -rf $(ls /Users/dianalin/mocking-spongebob/temp/strands_* | grep -v ${date_short}) 2> /dev/null
fi

theme=$(grep 'theme is' $html | awk -F "<strong>|</strong>" '{print $2}' | gsed "s/&rsquo;/'/")
echo "$theme"

theme_hint=$(grep 'The theme' $html | awk -F "<p>|</p>" '{print $2}' | gsed 's/^ \+//' | gsed 's|</\?[a-z]\+>||g') 
echo "$theme_hint"

for i in "first" "second" "third" "fourth" "fifth" "sixth" "spangram"; do 
	if [[ "$i" == "spangram" ]]; then
		word=$(grep "${i}" $html | tail -n1 | awk '{print $NF}' | gsed 's|</\?[a-z]\+>||g' | gsed 's/\.$//')
		hint=$(grep "${i}" $html | head -n1 | gsed 's|</\?[a-z]\+>||g' | awk -F "spangram" '{print $2}' | gsed 's/^ \+//' | gsed 's/\.$//' | gsed 's/^ \?is \?//' | gsed 's/^ \?refers to \?//')
	else
		hint=$(grep "${i} word" $html | head -n1 |  gsed 's|</\?[a-z]\+>||g' | awk -F " word " '{print $2}' | gsed 's/\.$//' | gsed 's/^ \?is \?//')
		word=$(grep "${i} word" $html | tail -n1 | gsed 's|</\?[a-z]\+>||g' | awk -F " is " '{print $2}' | gsed 's/\.$//') 
	fi
	echo "${word}: ${hint}"
done

