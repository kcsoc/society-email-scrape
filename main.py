from bs4 import BeautifulSoup
import requests
import re
import time
import os
import sys
import urllib.parse

# Constants
DEBUG_MODE = "DEBUG_MODE" in os.environ and os.environ["DEBUG_MODE"] == "True"
EMAIL_REGEX = "[A-Za-z0-9]+[\.\-_]?[A-Za-z0-9]+[@]\w+([.]\w{2,8})+"
BAD_EMAILS = [
    "contact@hertfordshire.su",
    "union.reception@aston.ac",
    "ctivities@brunel.ac",
    "infooffice.su@coventry.ac",
    "societies.su@coventry.ac",
    "studentsunion@nottingham.ac",
    "studentsunion@cardiff.ac.uk",
    "union@imperial.ac.uk",
    "societies@roehampton.ac"
]
CSV_HEADERS = "Name, Email"
USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'

# Debug print function
debugprint = print if DEBUG_MODE else lambda *a, **k: None

def get_domain(url):
    """Get the domain of a URL."""
    parsed_url = urllib.parse.urlsplit(url)
    return f"{parsed_url.scheme}://{parsed_url.hostname}"

def get_page_urls(root_url):
    """Retrieve a list of society page URLs from the given root URL."""
    page_urls = []
    classes = "|".join(["msl_organisation_list", "view-uclu-societies-directory",
                        "atoz-container", "listsocieties", "block-og-menu"])

    req = requests.get(root_url, headers={"User-Agent": USER_AGENT})
    soup = BeautifulSoup(req.content, 'html.parser')
    main = soup.find(['div', 'ul', 'section'], class_=re.compile(classes))

    for a in main.find_all('a', href=True):
        url = a['href']
        if url.startswith("/"):
            page_urls.append(domain + url)

        if url.startswith("https://society.tedu.edu"):
            page_urls.append(url)

    return list(set(page_urls))  # Use set to remove duplicates

def clean_name(name):
    """Clean up the society name."""
    name = name.replace("&", " and ")
    name = name.replace(",", "")
    name = re.sub(r'\s+', ' ', name).strip()
    name = re.sub(r' \|.*', '', name)
    return name.title()

def extract_email(soup, root_url):
    """Extract the email address from the HTML soup."""
    try:
        email = soup.find('a', class_=re.compile("msl_email|socemail"))['href'][7:]
        if "infooffice.su@coventry.ac" in email:
            raise ValueError("Invalid email")
    except:
        email_match = re.search(f"({EMAIL_REGEX})", str(soup))
        email = email_match.group(1) if email_match else ""
    return email

def process_society_page(url, root_url):
    """Process a society page and print name and email."""
    try:
        req = requests.get(url, headers={"User-Agent": USER_AGENT})
        soup = BeautifulSoup(req.content, 'html.parser')

        if "cusu.co.uk" in root_url:
            # Coventry SU name edge case handling
            name = soup.find('h2').find('a').text.strip().lower()
        else:
            # Get name from title
            name = soup.find('title').text.strip().lower()

        email = extract_email(soup, root_url)
        name = clean_name(name)
        print(f"{name}, {email}")

    except Exception as e:
        debugprint(f"Error processing page {url}: {str(e)}")

def main():
    try:
        root_url = sys.argv[1].strip().strip("\"")
        global domain
        domain = get_domain(root_url)
    except:
        print("Error in unis.yml file")
        return

    page_urls = get_page_urls(root_url)

    if DEBUG_MODE:
        page_urls = page_urls[:10]

    print(CSV_HEADERS)
    
    for url in page_urls:
        process_society_page(url, root_url)
        time.sleep(0.1)

if __name__ == '__main__':
    main()
