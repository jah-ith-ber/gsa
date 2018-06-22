import sys  
import asyncio  
import aiohttp
from bs4 import BeautifulSoup
import csv

# These two variables determine if we're on the final task or not.
our_count = 0
csv_len = 0

loop = asyncio.get_event_loop()  
client = aiohttp.ClientSession(loop=loop)

proxy_url = input('Enter proxy url: ')
proxy_port = input('Enter proxy port: ')

httpproxy = 'http://' + proxy_url + ':' + proxy_port

# Read the CSV file in.
csvList = open('./productLinks.csv')
productList = csv.reader(csvList, delimiter='|')

 # Setup to write to a new csv file
outputfile = open('./final.csv', 'w', newline='')
outputwriter = csv.writer(outputfile, delimiter=';')

# Do not follow links that we've already followed.
links = []

# Tried using 2 separate async functions - one for initial, one for vendor links
async def get_page(client, url):  
    async with client.get(url, proxy=httpproxy) as response:
        if response.status == 200:
            return await response.read()

async def get_vendor_page(client, url):  
    async with client.get(url, proxy=httpproxy) as r:
        if r.status == 200:
            return await r.read()

# Our main async function
async def parse_gsa_webpage(product):
    prodname = product[0]
    prodUrls = product[1].split('`')

    print('started ', prodname)

    # List to prepare our csv rows for a csv writerow.
    csv_obj = [[], [], []]

    if 'No results found' not in prodUrls[0]:
        # Loop through product links
        for link in prodUrls:
            # If we haven't visited this link
            if link not in links:
                # Grab the page asyncronously
                html_to_parse = await get_page(client, link)
                print('initial request made to:')            
                print(link)
                # Throw the link in links
                links.append(link)
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

                                #added as placeholder.
                                print('VENDOR LINK FOUND: ' + newlink)

                                ##########################
                                # This is our problem area.
                                ##########################

                                # # if newlink != None and link != newlink and newlink not in links:
                                #     links.append(newlink)
                                #     res2 = await get_vendor_page(client, newlink)

                                #     soup2 = BeautifulSoup(res2, 'lxml')

                                #     nameTable2 = soup2.findAll(attrs={
                                #         'width': "100%",
                                #         'border': "0",
                                #         'cellspacing': "0",
                                #         'cellpadding': "0",
                                #         'class': "black8pt"
                                #     })

                                #     moreSpecs2 = soup2.findAll(attrs={
                                #         'width': "100%",
                                #         'border': "0",
                                #         'cellspacing': "0",
                                #         'cellpadding': "1",
                                #         'class': "black8pt"
                                #     })

                                #     # Spects/Description tabs
                                #     specsTab2 = ''
                                #     additionalDesc2 = ''

                                #     descTable2 = soup2.findAll(
                                #         id='TabbedPanels1')

                                #     if len(descTable2) > 0:
                                #         tabPanelLabels2 = descTable2[0].ul.findAll(
                                #             'li')
                                #         if len(descTable2[0].select('.comment')) > 0:
                                #             additionalDesc2 = descTable2[0].select(
                                #                 '.comment')
                                #         tabPanelContent2 = descTable2[0].select(
                                #             ".TabbedPanelsContent table")
                                #         tabPanelContent3 = descTable2[0].select(
                                #             ".TabbedPanelsContentGroup td div")
                                #         our2List.append(newlink)
                                #         for div in tabPanelContent3:
                                #             our2List.append(
                                #                 div.get_text().strip())
                                #         if len(additionalDesc2) > 0:
                                #             our2List.append(
                                #                 additionalDesc2[0].get_text().strip())

                                #     if len(tabPanelContent2) > 1:
                                #         speclist2 = tabPanelContent2[1].findAll(
                                #         'tr')
                                #     else:
                                #         speclist2 = []

                                #     if len(speclist2) > 0:
                                #         for spec in speclist2:
                                #             specs = spec.findAll('td')
                                #             if len(specs) > 1:
                                #                 for i, v in enumerate(specs):
                                #                     if i == 1:
                                #                         specsTab2 += str(v.string) + \
                                #                             '. '
                                #                     else:
                                #                         specsTab2 += str(v.string) + \
                                #                             ': '
                                #         our2List.append(
                                #             specsTab2)

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

    if our_count == csv_len:
        loop.stop()
        await client.close()
        print('All tasks completed.')

for i, item in enumerate(productList):
    csv_len += 1
    asyncio.ensure_future(parse_gsa_webpage(item), loop = loop)
try:
    loop.run_forever()
finally:
    loop.close()