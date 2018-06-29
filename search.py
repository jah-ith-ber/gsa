import bs4
import csv
import webbrowser
import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os


proxy_url = input('Enter proxy url: ')
proxy_port = input('Enter proxy port: ')
proxy = 'http://' + proxy_url + ':' + proxy_port

links = []
our_dict = {}

if os.name == 'nt':
    webdriverPath = os.getcwd() + '\dependencies\chromedriver.exe'
else:
    webdriverPath = os.getcwd() + '/dependencies/chromedriver'

print(webdriverPath)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=%s' % proxy)
driver = webdriver.Chrome(webdriverPath, chrome_options=chrome_options)

def check_tag_exists(name):
    try:
        driver.find_elements_by_tag_name(name)
    except NoSuchElementException:
        return False
    return True


def check_xpath_exists(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


# Grab the initial GSA site cookie so we can use the search.
driver.get('https://www.gsaadvantage.gov')


# Read from the lsit of product id's provided.
mftrNumCsv = open('./csv/tony-export.csv')
mftrNumReader = csv.reader(mftrNumCsv, delimiter=',')
mftrNums = list(mftrNumReader)

# Setup to write to a new csv file
outputfile = open('./csv/productLinks.csv', 'w', newline='')
outputwriter = csv.writer(outputfile)

# For each product row in the CSV
for product in mftrNums:
    
    # Perform an exact search for mfr #
    print(product)

    # Our list variables
    searchList = []
    linkList = []

    # Some strings we need for later.
    blue = '../..//preceding::tr/td/a[contains(@class, "arial")]'
    green = '../..//preceding::tr/td/span/a[contains(@class, "arial")]'

    # Product numbers
    if product[0] and product[0] != 'n/a':
        prodNum = product[0]
        if prodNum not in searchList:
            searchList.append(prodNum)

    if product[3] and product[0] != 'n/a':
        if '|' in product[3]:
            prod_split = product[3].split('|')
            for numm in prod_split:
                if numm not in searchList:
                    searchList.append(numm)
        else:
            if product[3] not in searchList:
                searchList.append(product[3])

    # Manufacturer numbers
    prodMan = product[1]
    prodManAbbr = product[2]
    prodManList = []

    if product[1] and product[0] != 'n/a':
        if '|' in product[1]:
            man_split = product[1].split('|')
            for man in man_split:
                if man not in prodManList:
                    prodManList.append(man)
        else:
            prodManList = None

    # Lets loop through each product number
    for search in searchList:
        print('search: ', search)
        if prodManList is not None:
            for man_token in prodManList:
                print('token: ', man_token)

                # Perform the search
                driver.get('https://www.gsaadvantage.gov/advantage/s/search.do?q=9,8:1' +
                        search +
                        '&q=10:1' + man_token + '&q=1:4ADV.OFF.*&s=3&c=25&searchType=1')

                # html = driver.page_source

                myHref = 'a[contains(@class, "arial")'

                # If the search returns no results
                if check_xpath_exists("//*[contains(text(),'We found no')]") != False:
                    # outputwriter.writerow([search + '|' + 'No results found'])
                    continue
                # If results are returned
                elif check_tag_exists('font') != False:

                    # Grab the table holding search results
                    searchResults = driver.find_element_by_xpath(
                        "//td[@align='left']")
                    myfont = driver.find_elements_by_tag_name('font')
                    resultList = searchResults.find_elements_by_xpath(
                        "//td[@align='left']/table[@width='100%']")

                    # Loop through each result
                    for i, v in enumerate(resultList):
                        try:
                            # If the product number is an exact match
                            if v.find_element_by_tag_name('font').text == search:
                                the_link = str(v.find_elements_by_tag_name('a')[0].get_attribute('href'))
                                if the_link not in links:
                                    # print(v.find_element_by_tag_name('font').text)
                                    try:
                                        # Tack it onto our linklist variable
                                        linkList.append(the_link)
                                        links.append(the_link)
                                    except:
                                        print(v.find_element_by_xpath(
                                            myHref).get_attribute('href'))
                        except:
                            pass

                    # if iterations = length, THEN print
                    # Join all links into a string
                    joined = '`'.join(linkList)

                    mystr = search + '|' + joined
                    nostr = search + '|' + 'No results found.'

                    # If links were found add them to the csv, otherwise say no results were found.
                    if len(linkList) > 0:
                        # if str(search) in our_dict:
                        #     print(our_dict[str(search)])
                        our_dict[str(search)] = mystr
                    else:
                        our_dict[str(search)] = nostr
        else:
            # Perform the search
            driver.get('https://www.gsaadvantage.gov/advantage/s/search.do?q=9,8:1' +
                    search +
                    '&q=10:1' + prodMan + '&q=1:4ADV.OFF.*&s=3&c=25&searchType=1')

            # html = driver.page_source

            myHref = 'a[contains(@class, "arial")'

            # If the search returns no results
            if check_xpath_exists("//*[contains(text(),'We found no')]") != False:
                # outputwriter.writerow([search + '|' + 'No results found'])
                continue
            # If results are returned
            elif check_tag_exists('font') != False:

                # Grab the table holding search results
                searchResults = driver.find_element_by_xpath(
                    "//td[@align='left']")
                myfont = driver.find_elements_by_tag_name('font')
                resultList = searchResults.find_elements_by_xpath(
                    "//td[@align='left']/table[@width='100%']")



                for i, v in enumerate(resultList):
                    try:
                        # If the product number is an exact match
                        if v.find_element_by_tag_name('font').text == search:
                            the_link = str(v.find_elements_by_tag_name('a')[0].get_attribute('href'))
                            if the_link not in links:
                                try:
                                    # Tack it onto our linklist variable
                                    linkList.append(the_link)
                                    links.append(the_link)
                                except:
                                    pass
                    except:
                        print('failed to find font tag')

                # Join all links into a string
                joined = '`'.join(linkList)

                mystr = search + '|' + joined
                nostr = search + '|' + 'No results found.'

                # If links were found add them to the csv, otherwise say no results were found.
                if len(linkList) > 0:
                    if str(search) in our_dict:
                        our_dict[str(search)] = mystr
                else:
                    our_dict[str(search)] = nostr

for k,v in our_dict.items():
    outputwriter.writerow([v])
    print(v)

print('complete')