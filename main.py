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
main = soup.find(
    ['div', 'ul'],
    class_=re.compile('msl_organisation_list|view-uclu-societies-directory')
)

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
        try:
            email = soup.find('a', class_=re.compile(
                "msl_email|socemail"))['href'][7:]
        except:
            # email = soup.find(string=re.compile(
                # "[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}"))
            email = soup.find(string=lambda s:
                              re.search("[A-Za-z0-9]+[\._]?[A-Za-z0-9]+[@]\w+([.]\w{2,3})+", s) and not
                              re.search("contact@hertfordshire.su", s) and not
                              re.search("union.reception@aston.ac", s) and not
                              re.search("ctivities@brunel.ac", s)and not
                              re.search("infooffice.su@coventry.ac", s) and not
                              re.search("societies.su@coventry.ac", s) and not
                              re.search("studentsunion@nottingham.ac", s) and not
                              re.search("societies@roehampton.ac", s)
                              )
            reg = re.compile("[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}")
            email = str(reg.findall(email)[0])

        name = name.replace(" | hertfordshire students' union", "")
        name = name.replace(" | coventry university students' union", "")
        name = name.replace(" | clubs and societies | students' union ucl", "")
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
