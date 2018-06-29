This is a re-structure of the original crawler. Tkinter has been removed to reduce memory overhead issues. Asynchronous requests have been implemented with various cacheing, timeouts, a semaphore, and limits so as to keep the client safe and GSA's servers from dying (sorry).

# Initial setup - Install the module dependencies with python via Entering in your cmd/terminal
- python3 pipinstaller.py

# PEFORMING A SEARCH
### Get a proxy ip address and port such as **111.11.111.111:80** from https://free-proxy-list.net/
- A US based proxy is ideal
- You can click the Https table header and it will sort either way
- Confirm the Https column value is 'Yes'
- Confirm the Anonymity column value is 'Anonymous'

### Run the search.py by entering
- python3 search.py
- Enter the IP (111.11.111.111) when prompted by the program
- Enter the port (80 in this example)

### Wait for the program to complete, then check productLinks.csv.


# PEFORMING A SCRAPE
Once productLinks.csv exists in the csv folder, you can run scrape.py

### Get a proxy ip address and port (or use the same one) from https://free-proxy-list.net/
- A US based proxy is ideal
- You can click the Https table header and it will sort either way
- Confirm the Https column value is 'Yes'
- Confirm the Anonymity column value is 'Anonymous'

### Run the scrape by entering
- python3 scrape.py
- Enter the IP (111.11.111.111) when prompted by the program
- Enter the port (80 in this example)

### Wait for the program to complete, then check final.csv. See troubleshooting below for errors.

#### Troubleshooting

##### Q. How is the final.csv delimited?
- The final.csv is semicolon delimited.

##### Q. The last message was 'writerow' and it's sitting there
- Unfortunately it sounds like the program is hanging. 
- If it's not budging, close out the program with ctrl+c (don't click the X button) and check that final.csv was written to.
- If it gets a ways through, an option would be to find where the scraper left off. You can look at the ending product numbers in final.csv. 
- You can then rename final.csv to something else, and then remove the upper products that did run in productLinks.csv.
- You can then just run it again and it'll start from where it left off. Just remember to rename final.csv. It will be overwritten if you don't and you might lose what you just ran!

##### Q. Program never makes an http request after I run it (403 forbidden/proxyError)? 
- Try again with a different proxy.