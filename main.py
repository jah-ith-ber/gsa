import sys  
import asyncio  
import aiohttp
from bs4 import BeautifulSoup
import csv

# These two variables determine if we're on the final task or not.
our_count = 0
csv_len = 0

loop = asyncio.get_event_loop()  

connector = aiohttp.TCPConnector(limit=20,force_close=True,enable_cleanup_closed=True,limit_per_host=20)
client = aiohttp.ClientSession(loop=loop,connector=connector)

proxy_url = input('Enter proxy url: ')
proxy_port = input('Enter proxy port: ')

httpproxy = 'http://' + proxy_url + ':' + proxy_port

# Read the CSV file in.
csvList = open('./productLinks.csv')
productList = csv.reader(csvList, delimiter='|')

 # Setup to write to a new csv file
outputfile = open('./final.csv', 'w', newline='')
outputwriter = csv.writer(outputfile, delimiter=';')

semaphore = asyncio.BoundedSemaphore(20)

# Our async .get function
async def get_page(client, url):  
    try:
        async with client.get(url, proxy=httpproxy) as response:
            if response.status == 200:
                return await response.read()
    except:
        return False

# Our main async function
async def parse_gsa_webpage(product, sem):
    async with sem: 
        prodname = product[0]
        prodUrls = product[1].split('`')

        print('started ', prodname)

        # List to prepare our csv rows for a csv writerow.
        csv_obj = [[], [], []]

        if 'No results found' not in prodUrls[0]:
            # Loop through product links
            for link in prodUrls:
                # If we haven't visited this link
                    print('initial request made to:')
                    # Grab the page asyncronously
                    html_to_parse = await get_page(client, link)
                    if html_to_parse == False:
                        return
                    print(link)
                    # parse it
                    soup = BeautifulSoup(html_to_parse, 'lxml')
                else: #Otherwise skip it
                    continue

                # Find our elements to scrape from the page. Typically arent really any classes/id's so we have to navigate by attributes.
                pricingTable = soup.findAll(attrs={
                    'width': "100%",
                    'border': "0",
                    'cellpadding': "0",
                    'cellspacing': "0",
                    'class': 'greybox'
                })[0]

                nameTable = soup.findAll(attrs={
                    'width': "100%",
                    'border': "0",
                    'cellspacing': "0",
                    'cellpadding': "0",
                    'class': "black8pt"
                })

                moreSpecs = soup.findAll(attrs={
                    'width': "100%",
                    'border': "0",
                    'cellspacing': "0",
                    'cellpadding': "1",
                    'class': "black8pt"
                })
                
                specsTab = ''
                additionalDesc = ''

                # Yay.. an id for once.
                descTable = soup.findAll(id='TabbedPanels1')

                # if a description table exists, grab it.
                if len(descTable) > 0:
                    if len(descTable[0].select('.comment')) > 0:
                        additionalDesc = descTable[0].select('.comment')
                    tabPanelContent = descTable[0].select(".TabbedPanelsContent table")

                # If spec box exists
                try:
                    speclist = tabPanelContent[1].findAll('tr')
                except:
                    speclist = []

                # Loop through the spec list, arrange it into a readable format for the csv.
                try:
                    for spec in speclist:
                        specs = spec.findAll('td')
                        if len(specs) > 1:
                            for i, v in enumerate(specs):
                                # If we're at at a 'key' in the spec list
                                if i == 1:
                                    specsTab += v.get_text() + '. '
                                # If we're at at a 'value' in the spec list
                                else:
                                    specsTab += v.get_text() + ': '
                except:
                    pass

                # Product Attributes
                productName = nameTable[1].strong.string.replace(';', ' ')

                trs = pricingTable.findAll('tr')
                # Pricing table madness begins
                for i, row in enumerate(trs):

                    row_tds = row.select('td')
                    row_ths = row.select('th')

                    ourList = []
                    our2List = []

                    vendorList = []
                    vendorIndex = []
                    count = 0

                    
                    for e, v in enumerate(row_tds):
                        print(e, ' - td iteration')
                        if i == 0:
                            if len(ourList) > 0 and e > 1:
                                if v.get_text().strip() == ourList[-1]:
                                    break
                            if v.get_text().strip() == 'Price/Unit':
                                ourList.append('Price')
                                ourList.append('')
                                ourList.append('Unit')
                            elif v.get_text().strip() == 'Features':
                                ourList.append('Features')
                                ourList.append('')
                                break
                            else:
                                ourList.append(''.join(e for e in v.get_text().replace('\n', ' ').strip() if e.isalnum() or e == '.' or e == '$' )) 
                        elif v.img != None:
                            if v.img['alt'].strip() != '':
                                ourList.append(v.img['alt'].strip())
                        else:
                            if '&nbsp;' not in v.get_text().strip():
                                ourList.append(''.join(e for e in v.get_text().replace('\n', ' ').strip() if e.isalnum() or e == '.' or e == '$' )) 
                            # if we find links in this tr and it contains catalog (vendor link)
                            if len(v.select('font[size="2"] a')) > 0:
                                if 'catalog' in v.select('font[size="2"] a')[0].get('href'):
                                    newlink = 'https://www.gsaadvantage.gov' + v.select('font[size="2"] a')[
                                        0].get('href')
                    for e, v in enumerate(row_ths):
                        print(e, ' - theaders iteration')
                        if i == 0:
                            if v.get_text().strip() == 'Contractor':
                                count = e
                            our2List.append(''.join(e for e in v.get_text().replace('\n', ' ').strip() if e.isalnum() or e == '.' or e == '$' ))                                 
                            our2List.append('')

                    ourList[0] = prodname

                    if i == 0:
                        if type(additionalDesc) == list:
                            if type(additionalDesc[0]) != str:
                                csv_obj[0] = 'prodNum;productName;prodUrl;specsTab;additionalDesc'.split(';')
                                csv_obj[1].append(prodname)
                                csv_obj[1].append(productName)
                                csv_obj[1].append(link)
                                csv_obj[1].append(specsTab)
                                csv_obj[1].append(additionalDesc[0].get_text().strip())
                        else:
                            csv_obj[0] = 'prodNum;productName;prodUrl;specsTab'.split(';')                     
                            csv_obj[1].append(prodname)
                            csv_obj[1].append(productName)
                            csv_obj[1].append(link)
                            csv_obj[1].append(specsTab)


                    if len(ourList) > 0:
                        csv_obj[2].append(ourList + our2List)
                    else:
                        continue

                outputwriter.writerow(csv_obj[0])
                csv_obj[0] = []
                outputwriter.writerow(csv_obj[1])
                csv_obj[1] = []
                for i, item in enumerate(csv_obj[2]):
                    if item[2] != '':
                        outputwriter.writerow(item)
                csv_obj[2] = []
                print('writerow')

        global our_count
        global csv_len

        our_count += 1

        print('our_count = ', our_count)
        print('csv_len = ', csv_len)

        if our_count == csv_len:
            loop.stop()
            await client.close()
            print('All tasks completed.')

for i, item in enumerate(productList):
    csv_len += 1
    asyncio.ensure_future(parse_gsa_webpage(item, semaphore), loop = loop)
try:
    loop.run_forever()
finally:
    loop.close()
