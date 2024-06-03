import requests
from bs4 import BeautifulSoup
import json

def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract text data from the website
    text_data = soup.get_text()

    # Check for common error messages or empty content
    if "404" in text_data or len(text_data.strip()) == 0:
        return None

    return text_data

def get_all_links(base_url):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    links = set()
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith('/'):
            href = base_url + href
        if base_url in href and not href.endswith(('.pdf', '.doc', '.ppt', '.xls', '.jpg', '.png', '.gif')):
            links.add(href)
    return links

def scrape_all_pages(base_url):
    links = get_all_links(base_url)
    all_data = {}

    for link in links:
        try:
            print(f"Scraping {link}")
            data = scrape_website(link)
            if data:
                all_data[link] = data
        except Exception as e:
            print(f"Failed to scrape {link}: {e}")

    return all_data

def save_data(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    base_url = 'https://u.ae/en/information-and-services'
    all_data = scrape_all_pages(base_url)
    save_data(all_data, 'web_content.json')
