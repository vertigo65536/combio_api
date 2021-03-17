import requests
import json
from bs4 import BeautifulSoup

timeout = 10

def search(search):
    r = requests.post(
        url='https://comb.io/a/q',
        data={
            'q': search
        },
        headers={
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-length': '3',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://comb.io',
            'referer': 'https://comb.io/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        },
        timeout=timeout
        )
    markup = json.loads(r.text[1:])
    href = []
    resultsMarkup = markup['payload']['markup']
    for i in range(len(resultsMarkup)):
        soup = BeautifulSoup(resultsMarkup[i], features='html.parser')
        for link in soup.findAll('a'):
            href.append([link.text, link.get('href'), link.get('src')])
    if href == []:
        return -1
    else:
        return href

def getDefaultTimestamps(url):
    largeID = url.split('/')[2]
    episodeID = largeID.split('?')[0]
    timestamp = largeID.split('?')[1][4:]
    
    ##retrieve video start and finish time stamps
    page = requests.get('https://comb.io' + url, timeout=timeout)
    soup = BeautifulSoup(page.text, features='html.parser')
    soup = soup.find(id="s")
    ts = []
    for timestamp in soup.findAll('input'):
        ts.append(timestamp['value'])
    
    data = dict()
    
    data['ts1'] = ts[0]
    data['ts2'] = ts[len(ts)-1]
        
    return data

def getAllTimestamps(url):
    largeID = url.split('/')[2]
    episodeID = largeID.split('?')[0]
    timestamp = largeID.split('?')[1][4:]
    
    ##retrieve video start and finish time stamps
    page = requests.get('https://comb.io' + url, timeout=timeout)
    ts = []
    ids = ["b", "s", "a"]
    for i in range(len(ids)):
        soup = BeautifulSoup(page.text, features='html.parser')
        soup = soup.find(id=ids[i])
        for timestampBlock in soup.findAll("div", {"class": "timeline-clip"}):
            tsBlockFormatted = dict()
            soup2 = BeautifulSoup(str(timestampBlock), features='html.parser')
            for tsInputString in soup2.findAll('input'):
                tsBlockFormatted[tsInputString['name']] = tsInputString['value']
            ts.append(tsBlockFormatted)
        
    return ts
    
    
def getVideoData(url, timestamps):
    if len(timestamps) != 2:
       return -1
    largeID = url.split('/')[2]
    data = {'media': largeID.split('?')[0]}
    data['ts1'] = timestamps['ts1']
    data['ts2'] = timestamps['ts2']
    
    r = requests.post(
        url='https://comb.io/create-clip',
        data=data,
        headers={
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-US,en;q=0.9',
            'content-length': '80',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://comb.io',
            'referer': 'https://comb.io'+url,
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        },
        timeout=timeout)
    soup = BeautifulSoup(r.text, features='html.parser')
    output = {}
    for link in soup.findAll('source'):
        href = link.get('src')
        output['link'] = href
    dataName = ['show', 'episode', 'views', 'quote']
    i = 0
    for wrapper in soup.findAll(attrs={'class': 'container'}):
        for dataBlock in wrapper.findAll(attrs={'style': 'float:left;'}):
            for metaData in dataBlock.findAll('div'):
                if i > len(dataName):
                    break
                if i == 2:
                    output[dataName[i]] = metaData.getText().replace('Views: ', '')
                else:
                    output[dataName[i]] = metaData.getText()
                i += 1
    return output
