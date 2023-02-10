# WpEnum
```
░██╗░░░░░░░██╗██████╗░███████╗███╗░░██╗██╗░░░██╗███╗░░░███╗
░██║░░██╗░░██║██╔══██╗██╔════╝████╗░██║██║░░░██║████╗░████║
░╚██╗████╗██╔╝██████╔╝█████╗░░██╔██╗██║██║░░░██║██╔████╔██║
░░████╔═████║░██╔═══╝░██╔══╝░░██║╚████║██║░░░██║██║╚██╔╝██║
░░╚██╔╝░╚██╔╝░██║░░░░░███████╗██║░╚███║╚██████╔╝██║░╚═╝░██║
░░░╚═╝░░░╚═╝░░╚═╝░░░░░╚══════╝╚═╝░░╚══╝░╚═════╝░╚═╝░░░░░╚═╝ v.1
```

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

# Todo
- [ ] Automate everything
