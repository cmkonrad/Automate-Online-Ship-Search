##############################################################################

##### Part one: find 'magic numbers' that find webpage for each ship #########

##############################################################################


# Download ChromeDriver from: https://sites.google.com/a/chromium.org/chromedriver/downloads
# Extract the chomedriver.exe file in the same directory as your python script

#Import Selenium Webdriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


#open Chrome
driver = webdriver.Chrome("C:/Users/CMKONRAD/.spyder/chromedriver.exe")

## Potential work around to get rid of pop-up where you have to click "ok"
# replace:
#driver = webdriver.Chrome()
## with the following:
#options = webdriver.chrome.options.Options()
#options.add_experimental_option("useAutomationExtension",False)
#driver = webdriver.Chrome(options=options)


# Resize the window to the desired screen width/height
driver.set_window_size(1300, 800)


magicNums = []       # numbers for URL
foundMMSIs = [] 
matchlessMMSIs = [] 
shiplist = []         # ships to search


import os
os.chdir('E:/pythonFilesITU/')  # set directory

# read in csv file of MMSIs to search. Should be made up of one column of MMSIs.
import csv                                        
with open('MMSIsToSearch.csv', 'rb') as f:  
    reader = csv.reader(f)
    for row in reader:
        shiplist.append(row)

#print shiplist

for mmsi in shiplist:
    
    #Open URL
    driver.get('https://www.itu.int/mmsapp/ShipStation/list')

    inputElement = driver.find_element_by_id('Search_MaritimeMobileServiceIdentity')
    inputElement.send_keys(mmsi)

    inputElement.send_keys(Keys.ENTER)

    html_source = driver.page_source

    magic_number = html_source[html_source.find('<button type="submit" class="btn btn-xs" aria-label="Left Align" name="onview" value="')+86:html_source.find('" title="View Ship Station">')]

    if len(magic_number) < 10:
    
        #print('The magic_number for mmsi ' + str(mmsi) + ' is: ' + magic_number)

        magicNums.append(magic_number) # Add magic number to the last position of the list
        foundMMSIs.append(mmsi)        # Add MMSI to the last position of the list

    else:
        matchlessMMSIs.append(mmsi)

print(magicNums)
print(foundMMSIs)
print(matchlessMMSIs)

len(foundMMSIs) +  len(matchlessMMSIs)
len(shiplist)

with open('matchlessMMSIs.csv', 'wb') as csv_file:       # save list of ships that still need to be matched
        writer = csv.writer(csv_file, delimiter=',')
        for line in matchlessMMSIs:
            writer.writerow(line)


with open('MagicNumbers.csv', 'wb') as csv_file:       # save magic numbers
        writer = csv.writer(csv_file, delimiter=',')
        for line in magicNums:
            #print(line)
            writer.writerow([line])  # square brackets needed so string characters aren't split across columns
            

##############################################################################

#####             Part two: scarpe data for each ship                #########

##############################################################################


import requests

findvalues = ["MMSI", "Call Sign", "Ship Name", "General Classification", "Primary Individual Classification"]
alldat = [[],[],[],[],[]]   # list of lists to hold extracted data

for num in magicNums:
    
    URL = "https://www.itu.int/mmsapp/shipstation/one/" + num
    page = requests.get(URL)
    
    whichlist = 0               # to go through lists
    
    for val in findvalues:                        # for each desired ship info item
        searchindex = "<div>" + val + "</div>"
        index = page.content.find(searchindex)    # find where this ship info is
        start = page.content.find('">', index) + 2     # name/value starts here
        stop = page.content.find('</label>', index)    # name/value ends here
        dat = page.content[start:stop]
        alldat[whichlist].append(dat)
        whichlist = whichlist +1 



 
with open('ITUdata.csv','w') as csv_file:
    for x in zip(*alldat):
        csv_file.write("{0},{1},{2},{3},{4}\n".format(*x))   

# may need to manually replace apostrophes and '&'s in output, as they are encoded

