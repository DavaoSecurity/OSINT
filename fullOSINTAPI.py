# by Nathan W Jones nat@davaosecurity.com
# pip install requests beautifulsoup4
# Logging Configuration: The logging is set up to log messages with timestamps and severity levels.
# Search Engines: The tool searches multiple search engines for the given query.
# Error Handling: The try-except blocks handle potential errors when making HTTP requests.
# API Integration: The tool integrates with the Hunter.io and Shodan APIs. You need to replace YOUR_HUNTER_API_KEY and YOUR_SHODAN_API_KEY 
# Email Detection: The tool checks if the input is an email address and queries the APIs accordingly.
# Results Logging: The results from both search engines and APIs are logged in a structured format.

import requests
from bs4 import BeautifulSoup
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class OSINTTool:
    def __init__(self):
        self.search_engines = [
            "https://www.google.com/search?q={}",
            "https://www.bing.com/search?q={}",
            "https://duckduckgo.com/?q={}"
        ]
        self.apis = {
            "hunter": "https://api.hunter.io/v2/email-verifier?email={}&api_key=YOUR_HUNTER_API_KEY",
            "shodan": "https://api.shodan.io/shodan/host/{}?key=YOUR_SHODAN_API_KEY"
        }

    def search(self, query):
        results = []
        for engine in self.search_engines:
            try:
                url = engine.format(query)
                logging.info(f"Searching: {url}")
                response = requests.get(url)
                response.raise_for_status()  # Raise an error for bad responses
                results.append(self.parse_results(response.text))
            except requests.RequestException as e:
                logging.error(f"Error retrieving results from {engine}: {e}")
        return results

    def parse_results(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and 'http' in href:
                links.append(href)
        return links

    def search_api(self, email):
        results = {}
        for name, url in self.apis.items():
            try:
                api_url = url.format(email)
                logging.info(f"Querying API: {api_url}")
                response = requests.get(api_url)
                response.raise_for_status()
                results[name] = response.json()
            except requests.RequestException as e:
                logging.error(f"Error querying {name} API: {e}")
        return results

    def run(self, query):
        logging.info(f"Running OSINT search for: {query}")
        if "@" in query:  # Check if the query is an email
            api_results = self.search_api(query)
            logging.info(f"API results: {json.dumps(api_results, indent=2)}")
        else:
            search_results = self.search(query)
            for idx, result in enumerate(search_results):
                logging.info(f"Results from search engine {idx + 1}:")
                for link in result:
                    logging.info(link)

if __name__ == "__main__":
    osint_tool = OSINTTool()
    query = input("Enter a website, email, or person's name to search: ")
    osint_tool.run(query)


