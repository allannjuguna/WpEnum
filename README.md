# WpEnum
```
░██╗░░░░░░░██╗██████╗░███████╗███╗░░██╗██╗░░░██╗███╗░░░███╗
░██║░░██╗░░██║██╔══██╗██╔════╝████╗░██║██║░░░██║████╗░████║
░╚██╗████╗██╔╝██████╔╝█████╗░░██╔██╗██║██║░░░██║██╔████╔██║
░░████╔═████║░██╔═══╝░██╔══╝░░██║╚████║██║░░░██║██║╚██╔╝██║
░░╚██╔╝░╚██╔╝░██║░░░░░███████╗██║░╚███║╚██████╔╝██║░╚═╝░██║
░░░╚═╝░░░╚═╝░░╚═╝░░░░░╚══════╝╚═╝░░╚══╝░╚═════╝░╚═╝░░░░░╚═╝ v.1
```

# Description
* This is a collection of tricks and techniques that can be used to enumerate wordpress users,plugins,vulnerabilities etc, that i have collected after playing various ctfs,hackthebox,tryhackme and vulnhub boxes.


# Usage
	
```
Usage:
	wpenum https://url

Examples:
   wpenum https://example.com/           -- if the wordpress site is running on the '/' path
   wpenum https://example.com/wordpress/ -- if the wordpress site is running on the '/wordpress' path

Description:
   Simple script that automatically generates links that can guide you on how to recon and enumerate wordpress installations
```


# Tasks
- [x] Checking information leaks
- [x] Enumerating users using wp-json and info leaks
- [x] Enumerating users using comments,pages and posts
- [x] Enumerating users using Nmap,Wpscan and Metasploit
- [x] Enumerating users using userid
- [x] Enumerating users using username
- [x] Bruteforce login with found users
- [x] Checking Plugins
- [x] Checking Directory listing of uploads folder


# Sample Output
```
wpenum https://localhost/wordpress

[+] -  Checking information leaks
[*] - http://localhost/wordpress/?static=1  => Check Information leak
[*] - http://localhost/wordpress/?static=1&order=asc  => Check Information leak
[*] - http://localhost/wordpress/wp-content/plugins/hello.php

[+] -  Enumerating users using wp-json and info leaks
[*] - http://localhost/wordpress/wp-json/wp/v2/users  // View all users
[*] -  curl "http://localhost/wordpress/index.php/wp-json/wp/v2/users/?per_page=100&page=1" | grep -iEo "\"name\":\"[ _a-z0-9A-Z]+\"" | grep -iv "Archives" | sort -u
[*] - http://localhost/wordpress/wp-json/wp/v2/users/1  // Fuzz the last value using burp of ffuf, some users may be hidden
[*] - http://localhost/wordpress/index.php/wp-json/wp/v2/users/?per_page=100&page=1 // Viewing all users
[*] - http://localhost/wordpress/?rest_route=/wp/v2/users  // Viewing all users
[*] - http://localhost/wordpress/?feed=rss //checking leaked username via rss feed

[+] -  Enumerating users using comments,pages and posts
[*] -  curl http://localhost/wordpress/wp-json/wp/v2/comments | grep -iEo "\"author_name\":\"[ _a-z0-9A-Z]+\"" | sort -u
[*] -  curl http://localhost/wordpress/wp-json/wp/v2/pages | grep -iEo "\/author\W\W[a-z]+" | sort -u
[*] -  curl http://localhost/wordpress/wp-json/wp/v2/posts | grep -iEo "\/author\W\W[a-z]+" | sort -u

[+] -  Enumerating users using Nmap,Wpscan and Metasploit
[*] - metasploit - auxiliary/scanner/http/wordpress_login_enum
[*] - nmap -sV --script http-wordpress-users --script-args limit=50 http://localhost/wordpress
[*] - wpscan --url http://localhost/wordpress/ --enumerate u

[+] -  Enumerating users using userid
[*] -  curl http://localhost/wordpress/wp-json/wp/v2/comments | grep -iEo "\"author\":[ 0-9]+" | sort -u // Fetches user ids from comments
[*] -  curl http://localhost/wordpress/wp-json/wp/v2/pages | grep -iEo "\"author\":[ 0-9]+" | sort -u // Fetches user ids from pages
[*] -  curl http://localhost/wordpress/wp-json/wp/v2/posts | grep -iEo "\"author\":[ 0-9]+" | sort -u // Fetches user ids from pages
[*] - http://localhost/wordpress/?author=1  // Fuzz  1 using ffuf/burp
[*] - ffuf -c -r -recursion -w ~/wordlists/1-100.txt  -u "http://localhost/wordpress/?author=FUZZ" -mc all -fc 404,403 -o users.out
[*] - http://localhost/wordpress/wp-json/wp/v2/users/1  // bruteforce the last value, some users may be hidden
[*] - ffuf -c -r -recursion -w ~/wordlists/1-100.txt  -u "http://localhost/wordpress/index.php/wp-json/wp/v2/users/FUZZ" -mc all -fc 404,403 -o users.out

[+] -  Enumerating users using username
[*] - http://localhost/wordpress/author/admin/  // Checking the username admin
[*] - ffuf -c -r -recursion -w users.txt  -u "http://localhost/wordpress/author/FUZZ" -mc all -fc 404

[+] -  Bruteforce login with found users
[*] - wpscan --url http://localhost/wordpress -U users.txt -P /usr/share/wordlists/rockyou.txt
[*] - metasploit - auxiliary/scanner/http/wordpress_login_enum

[+] -  Checking Plugins
[*] - curl http://localhost/wordpress/hello-world/ | grep -Eo "/plugins/[-._/\a-zA-Z0-9]+" | sort -u
[*] - wpscan --api-token YourWpscanTokenHere --url http://localhost/wordpress --enumerate ap
[*] - wpscan --api-token YourWpscanTokenHere --url http://localhost/wordpress --plugins-detection aggressive
[*] - view source of 'http://localhost/wordpress/author/admin/' or 'http://localhost/wordpress/?p=1' or one posts page and search for the word plugin. Search for vulns in searchsploit

[+] -  Checking Directory listing of uploads folder
[*] - http://localhost/wordpress/wp-content/uploads/
[*] - http://localhost/wordpress/wp-content/uploads/2023/02/  //fuzz 2023 and 02 using burp/fuff
[*] - ffuf -c -r -recursion -w ~/wordlists/years.txt  -u "http://localhost/wordpress/wp-content/uploads/FUZZ/02/" -mc all -fc 404,403

[+] -  Other areas to check
[*] - http://localhost/wordpress/author/admin/feed/

[+] -  Checking Vulnerabilities in plugins and core wordpress 
[*] - wpscan --api-token YourWpscanTokenHere --url http://localhost/wordpress --enumerate vp,vt -o wpscan.log
[*] - searchsploit wordpress_version

[+] -  If authenticated or have credentials 
[*] - Check whether the core version has vulnerabilities like WordPress 5.6-5.7 - Authenticated XXE: https://tryhackme.com/room/wordpresscve202129447
```


# Todo
- [ ] Automate everything
