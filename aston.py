from bs4 import BeautifulSoup
import requests
import re
import http.cookiejar
import time
import os
import re

print("Name, Email")

# Set headers
headers = requests.utils.default_headers()
headers.update(
    {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
# cookies = http.cookiejar.MozillaCookieJar('cookies.txt')
# cookies.load()

root = "https://www.astonsu.com/union/student-activities/clubs-and-societies/"
newrls = []

req = requests.get(root, headers)  # , cookies=cookies)
soup = BeautifulSoup(req.content, 'html.parser')
main = soup.find('div', class_=re.compile('msl_organisation_list'))

for a in main.find_all('a', href=True):
    url = a['href']
    if url.startswith("/society/"):
        newrls.append("https://www.astonsu.com/" + url)

newrls = list(dict.fromkeys(newrls))

for url in newrls:
    req = requests.get(url, headers)  # , cookies=cookies)
    soup = BeautifulSoup(req.content, 'html.parser')
    try:
        name = soup.find('h1').text.strip().lower()
        email = soup.find('a', class_=re.compile('msl_email'))['href'][7:]

        name = name.replace("society", "")
        name = name.replace("brunel", "")
        name = name + " society"
        name = name.replace("  ", " ")
        name = name.strip()
        name = name.title()

        print(name + ", " + email)

    except Exception as e:
        # print(e)
        pass
    time.sleep(0.5)
