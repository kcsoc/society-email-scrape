from bs4 import BeautifulSoup
import requests
import re
import http.cookiejar
import time
import os
import re
import sys
import urllib.parse

print("Name, Email")

# Set headers
headers = requests.utils.default_headers()
headers.update(
    {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
# cookies = http.cookiejar.MozillaCookieJar('cookies.txt')
# cookies.load()


def get_domain(url):
    a = urllib.parse.urlsplit(url)
    return str(a.scheme) + "://" + str(a.hostname)


try:
    root = sys.argv[1].strip().strip("\"")
    domain = get_domain(root)
except:
    print("error in unis.yml file")

urls = []

req = requests.get(root, headers)  # , cookies=cookies)
soup = BeautifulSoup(req.content, 'html.parser')
main = soup.find('div', class_=re.compile('msl_organisation_list'))

for a in main.find_all('a', href=True):
    url = a['href']
    if url.startswith("/"):
        urls.append(domain + url)

urls = list(dict.fromkeys(urls))

for url in urls:  # [urls[i] for i in range(3)]:
    req = requests.get(url, headers)  # , cookies=cookies)
    soup = BeautifulSoup(req.content, 'html.parser')
    try:
        name = soup.find('title').text.strip().lower()
        email = soup.find('a', class_=re.compile(
            "msl_email|socemail"))['href'][7:]

        name = name.replace("&", " and ")
        name = name.replace(",", "")
        name = name.replace("  ", " ")
        name = name.replace("   ", " ")
        name = name.strip()
        name = name.title()

        print(name + ", " + email)

    except:  # Exception as e:
        # print(e)
        pass
    time.sleep(0.1)
