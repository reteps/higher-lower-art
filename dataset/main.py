import re
import requests
import json
# Contemporary Art + Impressionist & Modern Art
scrape_url = "https://www.sothebys.com/en/results?from=&to=&f2=00000164-609b-d1db-a5e6-e9ff01230000&f2=00000164-609b-d1db-a5e6-e9ff08ab0000&f3=LIVE&f3=ONLINE&q=&p={}"
s = requests.Session()
pages = 517 // 15 + 1
urls = []
for page in range(pages):
    data = s.get(scrape_url.format(page+1), headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
    }).text
    # print(data)
    page_url = re.findall(
        "\"(https://www.sothebys.com/en/buy/auction/.*)\">", data)
    auction_pages = set(page_url)
    for auction_page in auction_pages:
        x = re.search("<link href=\"https://www.sothebys.com/buy/(.*-.*)\" rel",
                      s.get(auction_page, headers={
                          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
                      }).text)
        print(x.group(1))
        urls.append({"url": auction_page, "id": x.group(1)})

    print(f'processed page {page}')
    with open('lookup.json', 'w') as f:
        json.dump(urls, f, indent=2)
