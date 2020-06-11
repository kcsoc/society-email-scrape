from bs4 import BeautifulSoup
import requests
import re
import http.cookiejar
import time
import os
import re

# Set headers
headers = requests.utils.default_headers()
headers.update(
    {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
# cookies = http.cookiejar.MozillaCookieJar('cookies.txt')
# cookies.load()

root = "https://www.warwicksu.com/societies-sports/societies/"
newrls = []

req = requests.get(root, headers)  # , cookies=cookies)
soup = BeautifulSoup(req.content, 'html.parser')
main = soup.find('div', class_=re.compile('msl_organisation_list'))

for a in main.find_all('a', href=True):
    url = a['href']
    if url.startswith("/societies-sports/societies"):
        newrls.append("https://warwicksu.com" + url)

newrls = list(dict.fromkeys(newrls))

for url in newrls:
    req = requests.get(url, headers)  # , cookies=cookies)
    soup = BeautifulSoup(req.content, 'html.parser')
    try:
        name = str(soup.find('h2', class_=re.compile(
            'orgName')).text.strip()).lower()
        email = soup.find('a', class_=re.compile('msl_email'))['href'][7:]

        name = name.replace("society", "")
        name = name.replace("warwick", "")
        name = name + " society exec"
        name = name.replace("  ", " ")
        name = name.strip()
        name = name.title()

        print(name + ", " + email)

    except:
        pass
    time.sleep(0.5)
