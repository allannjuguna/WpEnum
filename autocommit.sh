#! /bin/bash
#  @author: zerofrost🦊
#  @date: 2022-5-22
#  @description: Automatic commits


white="\033[0m"
red="\033[91m"
green="\033[92m"
bold="\033[01m"
yellow="\033[93m"
blue="\033[94m"
success="${bold}${green}[+]${white} - "
alert="${bold}${yellow}[!]${white} - "
progress="${bold}${blue}[*]${white} - "
fail="${bold}${red}[*]${white} - "
end="${white}"

echo -e "$progress Pulling recent changes"
git pull && echo -e "$success All changes pulled" || echo -e "$fail Could not pull changes. Ignoring ... "
git config advice.addIgnoredFile false
commit_messages=(
	"New Update" 
	"Fixed typo" 
	"Restructured Code" 
	"Minor changes"
	"New feature"
	"Updated Readme.md"
	"Minimized clutter in code"
	"Added files via upload"
	)

total=${#commit_messages[@]}
index=$(( ( RANDOM % $total ) + 0 ))
result=$(($total - $index))

if [[ $result < 0 ]];then
	echo "[-] Try again"
	exit
else

	arguments=${#}
	if [ $arguments -lt 1 ] # Checking the number of args
	then
	    echo -e "${fail} Enter commit message"
	    exit
	fi

	INPUT="${1}"
	if [ "$INPUT" = "-f" ]
	then
		message=${commit_messages[index]}
	else
		message=${1}
	fi
	echo -e "${success} Committing with message: $message $end"
	echo

	git add * && sleep 1 && git commit -m "${message}"
	git add * || sleep 1 && git commit -m "${message}"
	echo 
	git push && echo -e "$success Committed successfully $end" || echo -e "$fail An error occurred while committing $end"
fi

