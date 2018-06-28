This is an async re-write of the scrape.py module. This only performs the second-half (scrape), not the search itself. You can still run the search from the original.

# This is a command-line utility - first open cmd
In your windows search bar, type in 'cmd' and hit enter.

# Install the module dependencies with python via Entering in your cmd/terminal
python3 pipinstaller.py

##################
PEFORMING A SCRAPE
##################

# Get a proxy ip adress/port such as '111.11.111.111:80' from https://free-proxy-list.net/
You can click the Https header and it will sort either way
* Confirm the Https column value is 'Yes'
* Confirm the Anonymity column value is 'Anonymous'

# Run the program by entering
python3 main.py
* Enter the IP (111.11.111.111) when prompted by the program
* Enter the port (80 in this example)

# Wait for the program to complete, then check final.csv. See troubleshooting below for errors.

###############
Troubleshooting
###############

Q. How is the final.csv delimited?
The final.csv is semicolon delimited.

Q. The last message was 'writerow' and it's sitting there
It may be completed and hanging. 

If it's not budging, close out the program with ctrl+c and check that final.csv was written to.
If it gets a ways through, an option would be to  find where the scraper left off. You can look at the ending product numbers in final.csv. 
You can then rename final.csv to something else, and then remove the upper products that did run in productLinks.csv.
You can then just run it again and it'll start from where it left off. just remember to move final.csv, or rename it. it will be overwritten if you don't and you might lose what you just ran.

Q. Program never makes an http request after I run it (403 forbidden/proxyError)? 
Try again with a different proxy.