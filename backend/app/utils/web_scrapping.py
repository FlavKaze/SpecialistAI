import requests
import bs4
from bs4 import BeautifulSoup
from app.utils.tools import split_sentences

headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4703.0 Safari/537.36"
    }

def find_in_google(query, return_links=False):
    response = requests.get(f"https://www.google.com/search?q={query}", headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    soup = BeautifulSoup(response.content, 'html.parser')
    if return_links:
        links = soup.find_all("a")
        links = [link.get("href") for link in links if link.get("href")]
        return links
    soup_text = soup.get_text(strip=True, separator=' ', types=(bs4.NavigableString))
    text_without_header = soup_text.split("Trecho da Web em destaque ")
    page_text = text_without_header[1] if len(text_without_header) > 1 else text_without_header[0]
    texts = split_sentences(page_text)
    return texts
        
def find_in_sites(query, url_site="https://pt.wikipedia.org/wiki/", find_size=1):
    links = find_in_google(f"site:{url_site} {query}", return_links=True)
    found_links = [link for link in links if link.startswith(url_site)]
    selected_links = found_links[:find_size] or links[:find_size]
    if not selected_links:
        return "Nada encontrado"
    sites_scraped = {}
    for link in selected_links:
        response = requests.get(link, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        page_text = soup.get_text(strip=True, separator=' ', types=(bs4.NavigableString))
        texts = split_sentences(page_text)
        sites_scraped[link] = texts
    return sites_scraped


if __name__ == "__main__":
    print(find_in_sites("Homer Simpson", find_size=3, url_site="https://pt.wikipedia.org/wiki/"))
    print(find_in_google("Homer Simpson"))