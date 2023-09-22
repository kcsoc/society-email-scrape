from bs4 import BeautifulSoup
import requests
import re
import time
import os
import sys
import urllib.parse

# Define DEBUG_MODE and debugprint function
DEBUG_MODE = False
if "DEBUG_MODE" in os.environ:
    DEBUG_MODE = True
debugprint = print if DEBUG_MODE else lambda *a, **k: None

# Define regular expressions for email and bad emails
email_regex = "[A-Za-z0-9]+[\.\-_]?[A-Za-z0-9]+[@]\w+([.]\w{2,8})+"
bad_emails = "|".join([
    "contact@hertfordshire.su",
    "union.reception@aston.ac",
    "ctivities@brunel.ac",
    "infooffice.su@coventry.ac",
    "societies.su@coventry.ac",
    "studentsunion@nottingham.ac",
    "studentsunion@cardiff.ac.uk",
    "union@imperial.ac.uk",
    "societies@roehampton.ac"
])

# Print CSV headers
print("Name, Email")

# Set headers for HTTP requests
headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
})

def get_domain(url):
    """This function gets the domain of a URL using the urllib library"""
    a = urllib.parse.urlsplit(url)
    return str(a.scheme) + "://" + str(a.hostname)

def get_urls(root):
    """Returns a list of all links to society pages

    Parameters:
        root (str): Root URL, society homepage.

    Returns:
        urls (list): List of URLs of all society pages.
    """
    urls = []
    classes = "|".join(["msl_organisation_list", "view-uclu-societies-directory",
                        "atoz-container", "listsocieties", "block-og-menu"])

    req = requests.get(root, headers)  # , cookies=cookies)
    soup = BeautifulSoup(req.content, 'html.parser')
    main = soup.find(['div', 'ul', 'section'], class_=re.compile(classes))

    for a in main.find_all('a', href=True):
        url = a['href']
        if url.startswith("/"):
            urls.append(domain + url)

        if url.startswith("https://society.tedu.edu"):
            urls.append(url)

    urls = list(dict.fromkeys(urls))
    return urls

try:
    # Get URL from command line arguments
    root = sys.argv[1].strip().strip("\"")
    domain = get_domain(root)
except:
    print("error in unis.yml file")

# Handle edge case for UCL's updated website
if "studentsunionucl" in root:
    urls = []
    for i in range(16):
        urls += get_urls(root + "?page=" + str(i))
        time.sleep(0.3)

    urls = list(dict.fromkeys(urls))
else:
    urls = get_urls(root)

if DEBUG_MODE:
    urls = [urls[i] for i in range(10)]

debugprint(urls)

for url in urls:
    req = requests.get(url, headers)  # , cookies=cookies)
    soup = BeautifulSoup(req.content, 'html.parser')
    try:
        if "cusu.co.uk" in root:
            # Coventry SU name edge case handling
            name = soup.find('h2').find('a').text.strip().lower()
        else:
            # Get name from title
            name = soup.find('title').text.strip().lower()
        try:
            # Try to find email address using classes
            email = soup.find('a',
                              class_=re.compile("msl_email|socemail")
                              )['href'][7:]
            if "infooffice.su@coventry.ac" in email:
                # Throw error to leave try block
                raise ValueError("_")
        except:
            email = soup.find(string=lambda s:
                              re.search(email_regex, s) and not
                              re.search(bad_emails, s)  # Remove default emails
                              )
            debugprint(email)
            reg = re.compile(
                "(" + email_regex + ")")
            email = str(reg.findall(email)[0][0])
            debugprint(email)

        # Cleanup society name
        name = name.replace("&", " and ")
        name = name.replace(",", "")
        name = name.replace("  ", " ")
        name = name.replace("   ", " ")
        name = re.sub(" \|.*", '', name)
        name = name.strip()
        name = name.title()

        print(name + ", " + email)

    except:  # Exception as e:
        # print(e)
        pass

    time.sleep(0.1)
