#!/usr/local/bin/bash

set -uo pipefail 
month=$(date '+%B')
# day_year=$(date '+%d-%Y')
day=$(date '+%e' | gsed 's/^ //')
year=$(date '+%Y')
url_date=${month,,}-${day}-${year}

date_short=$(date '+%b%d')

urls_to_try=( https://www.thegamer.com/nyt-strands-answers-hints-${url_date}/ https://www.thegamer.com/nyt-strands-answers-and-hints-${url_date}/ https://www.thegamer.com/nyt-strands-answers-hints-month-${day}-${year}/ )


html=/Users/dianalin/mocking-spongebob/files/strands.html

if [[ ! -f "/Users/dianalin/mocking-spongebob/temp/strands_${date_short}" ]]; then
	for url in "${urls_to_try[@]}"; do 
		curl -o $html $url 2> /dev/null
		if [[ "$(grep -wc '404' $html)" -eq 0 ]]; then
			break
		fi
	done
fi

if [[ "$(grep -wc '404' $html)" -gt 0 ]]; then
	echo NULL
	exit 0 
else
	touch /Users/dianalin/mocking-spongebob/temp/strands_${date_short}
	rm -rf $(ls /Users/dianalin/mocking-spongebob/temp/strands_* | grep -v ${date_short}) 2> /dev/null
fi

theme=$(grep 'theme is' $html | awk -F "<strong>|</strong>" '{print $2}' | gsed "s/&rsquo;/'/" | gsed "s/&#39;/'/g")
echo "$theme"

theme_hint=$(grep 'The theme' $html | awk -F "<p>|</p>" '{print $2}' | gsed 's/^ \+//' | gsed 's|</\?[a-z]\+>||g') 
echo "$theme_hint"

for i in "first" "second" "third" "fourth" "fifth" "sixth" "spangram"; do 
	if [[ "$i" == "spangram" ]]; then
		word=$(grep "${i}" $html | tail -n1 | awk '{print $NF}' | gsed 's|</\?[a-z]\+>||g' | gsed 's/\.$//')
		hint=$(grep "${i}" $html | head -n1 | gsed 's|</\?[a-z]\+>||g' | awk -F "spangram" '{print $2}' | gsed 's/^ \+//' | gsed 's/\.$//' | gsed 's/^ \?\(is \)\?\(are \)\?//' | gsed 's/^ \?refers to \?//' | gsed "s/&#39;/'/g")
	else
		# hint=$(grep "${i} word" $html | head -n1 |  gsed 's|</\?[a-z]\+>||g' | awk -F " word" '{print $2}' | gsed 's/\.$//' | gsed 's/^ \?\(is \)\?\(are \)\?//' | gsed 's/^[ ,]\+//' | gsed "s/&#39;/'/g")
		hint=$(grep "${i} word" $html | head -n1 | awk -F "</strong>" '{print $2}' | gsed 's|</\?[a-z]\+>||g' | gsed 's/\.$//' | gsed 's/^ \?\(is \)\?\(are \)\?//' | gsed 's/^[ ,]\+//' | gsed "s/&#39;/'/g")
		word=$(grep "${i} word" $html | tail -n1 | gsed 's|</\?[a-z]\+>||g' | awk -F " is " '{print $2}' | gsed 's/\.$//') 
	fi
	if [[ -n "${word}" ]]; then
		echo "${word}: ${hint}"
	fi
done

