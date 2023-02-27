#! /usr/bin/python3
#  @author: zerofrost
#  @twitter: @xubzer0
#  @date: 2022-12-2
#  @description: This script generates links to enumerate wordpress info


import requests
import re
from sys import argv as arguments

# Colors
token="YourWpscanTokenHere"
verbose="Truex"
white="\033[0m"
bold='\033[01m'
red='\033[31m'
green='\033[32m'
success=f"{bold}{green}[+]{white} - "
blue="\033[94m"
progress=f"{bold}{blue}[*]{white} - "
fail=f"{bold}{red}[*]{white} - "
good=f"{bold}{green}"
bad=f"{bold}{red}"
end="\033[0m"

def banner():
	banner="""

░██╗░░░░░░░██╗██████╗░███████╗███╗░░██╗██╗░░░██╗███╗░░░███╗
░██║░░██╗░░██║██╔══██╗██╔════╝████╗░██║██║░░░██║████╗░████║
░╚██╗████╗██╔╝██████╔╝█████╗░░██╔██╗██║██║░░░██║██╔████╔██║
░░████╔═████║░██╔═══╝░██╔══╝░░██║╚████║██║░░░██║██║╚██╔╝██║
░░╚██╔╝░╚██╔╝░██║░░░░░███████╗██║░╚███║╚██████╔╝██║░╚═╝░██║
░░░╚═╝░░░╚═╝░░╚═╝░░░░░╚══════╝╚═╝░░╚══╝░╚═════╝░╚═╝░░░░░╚═╝ v.1

					https://twitter.com/xubzer0
	
	"""
	print(f"{banner}")


def help():
	options="""Usage:
	wpenum https://url

Examples:
   wpenum https://example.com/           -- if the wordpress site is running on the '/' path
   wpenum https://example.com/wordpress/ -- if the wordpress site is running on the '/wordpress' path

Description:
   Simple script that automatically generates links that can guide you on how to recon and enumerate wordpress installations

	"""
	print(options) 


def generatelinks(url):
	url=url.strip().replace("/index.php","").replace("index.php","")
	if '://' not in url:
		url=f"{prefix}{url}"
	if url[-1] == '/':
		url=f"{url[:-1]}"


	# CHECKING LEAKING OF SENSITIVE INFO
	print(f"\n{success} Checking information leaks")
	print(f"{progress}{url}/?static=1  => Information leak")
	print(f"{progress}{url}/?static=1&order=asc  => Information leak")
	print(f"{progress}{url}/wp-content/plugins/hello.php")


	# USING JSON AND LEAKS
	print(f"\n{success} Enumerating users using wp-json and info leaks")
	print(f"{progress}{url}/wp-json/wp/v2/users  // View all users")
	regex=r'grep -iEo "\"name\":\"[ _a-z0-9A-Z]+\"" | grep -iv "Archives" | sort -u'
	print(f'{progress} curl -sk \"{url}/index.php/wp-json/wp/v2/users/?per_page=100&page=1\" | {regex}')

	print(f"{progress}{url}/wp-json/wp/v2/users/1  // Fuzz the last value using burp of ffuf, some users may be hidden")
	print(f"{progress}{url}/index.php/wp-json/wp/v2/users/?per_page=100&page=1 // Viewing all users")
	print(f"{progress}{url}/?rest_route=/wp/v2/users  // Viewing all users")
	print(f"{progress}{url}/?feed=rss //checking leaked username via rss feed")


	# USING JSON AND LEAKS
	print(f"\n{success} Enumerating users using comments,pages and posts")
	regex=r'grep -iEo "\"author_name\":\"[ _a-z0-9A-Z]+\"" | sort -u'
	print(f'{progress} curl -sk {url}/wp-json/wp/v2/comments | {regex}')
	regex=r'grep -iEo "\/author\W\W[a-z]+" | sort -u'
	print(f'{progress} curl -sk {url}/wp-json/wp/v2/pages | {regex}')
	print(f'{progress} curl -sk {url}/wp-json/wp/v2/posts | {regex}')


	# USING NMAP AND METASPLOIT
	print(f"\n{success} Enumerating users using Nmap,Wpscan and Metasploit")
	print(f"{progress}metasploit - auxiliary/scanner/http/wordpress_login_enum")
	print(f"{progress}nmap -sV --script http-wordpress-users --script-args limit=50 {url}")
	print(f"{progress}wpscan --url {url}/ --enumerate u")

	# USING USERID AND BRUTEFORCING IDS
	print(f"\n{success} Enumerating users using userid")
	regex=r'grep -iEo "\"author\":[ 0-9]+" | sort -u'
	print(f'{progress} curl -sk {url}/wp-json/wp/v2/comments | {regex} // Fetches user ids from comments'  )
	print(f'{progress} curl -sk {url}/wp-json/wp/v2/pages | {regex} // Fetches user ids from pages'  )
	print(f'{progress} curl -sk {url}/wp-json/wp/v2/posts | {regex} // Fetches user ids from pages'  )
	print(f"{progress}{url}/?author=1  // Fuzz  1 using ffuf/burp") 
	print(f"{progress}ffuf -c -r -recursion -w ~/wordlists/1-100.txt  -u \"{url}/?author=FUZZ\" -mc all -fc 404,403 -o users.out")
	print(f"{progress}{url}/wp-json/wp/v2/users/1  // bruteforce the last value, some users may be hidden")
	print(f"{progress}ffuf -c -r -recursion -w ~/wordlists/1-100.txt  -u \"{url}/index.php/wp-json/wp/v2/users/FUZZ\" -mc all -fc 404,403 -o users.out")
	# print(f"\t{progress}wpscan --api-token 0TXJyMIhsarjk9F3u0tit3ulOnyfjo8dMWGnU2W6liM --url {url}/ --enumerate u")
	

	# USING USERNAME AND BRUTEFORCING NAME
	print(f"\n{success} Enumerating users using username")
	print(f"{progress}{url}/author/admin/  // Checking the username admin")
	print(f"{progress}ffuf -c -r -recursion -w users.txt  -u \"{url}/author/FUZZ\" -mc all -fc 404")

	# BRUTEFORCING LOGIN FORMS
	print(f"\n{success} Bruteforce login with found users")
	print(f"{progress}wpscan --url {url} -U users.txt -P /usr/share/wordlists/rockyou.txt")
	print(f"{progress}metasploit - auxiliary/scanner/http/wordpress_login_enum")

	# CHECKING PLUGINS
	print(f"\n{success} Checking Plugins")
	print(f"{progress}wpscan --api-token {token} --url {url} --enumerate ap")
	print(f"{progress}wpscan --api-token {token} --url {url} --plugins-detection aggressive")
	print(f"{progress}view source of '{url}/author/admin/' or '{url}/?p=1' or one posts page and search for the word plugin. Search for vulns in searchsploit")

	# Check Directory listing
	print(f"\n{success} Checking Directory listing of uploads folder")
	print(f"{progress}{url}/wp-content/uploads/")
	print(f"{progress}{url}/wp-content/uploads/2023/02/  //fuzz 2023 and 02 using burp/fuff"  )
	print(f"{progress}ffuf -c -r -recursion -w ~/wordlists/years.txt  -u \"{url}/wp-content/uploads/FUZZ/02/\" -mc all -fc 404,403")


if len(arguments) < 2 :
	banner()
	help()
	exit(-1)
else:
	banner()
	generatelinks(arguments[1])

	



