Quick Start

Install the module dependencies with python via entering in your cmd/terminal
1. python3 pipinstaller.py

2. make sure productLinks.csv is in the same directory as main.py.

get a proxy ip/port
3. get a proxy ip adress/port such as 173.36.255.167 and 80 from https://free-proxy-list.net/

Run main.py from your terminal/cmd with the command
4. python main.py
  a. enter the ip when prompted (173.36.255.167) and hit enter
  b. enter the port (80) and hit enter


======


The final.csv is semicolon delimited


==========
Troubleshooting
 ==========

 Stuck or errored out? 
 
 a. If the last message was 'writerow' it may be completed.

 b. Close out the program with cmd/ctrl+c and check that final.csv was written to. if it did, see where it left off. Then you can edit the productLinks.csv to where it left off, re-name the final.csv from the last run, and you can start a new one.

 Program never makes an http request? 
 
 Likely a problem with the proxy provided. Try using a different proxy ip and port from a site like http://free-proxy-list.net.