import urllib.parse
import requests
import json
from currency_converter import CurrencyConverter
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('./creds.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
s = requests.Session()

c = CurrencyConverter()
# ref = db.reference("/artwork")

raw = None
with open('angolia_lookup_table.json') as f:
    raw = json.load(f)


# skip = "af79fca6-b7e6-4bff-8ee1-f13e44612089"
# found = False
n = 0
collection = db.collection(u'artwork')
for auction in raw:
    # if not found and auction['id'] != skip:
    #     continue
    # else:
    #     found = True
    artworks = auction['angolia']
    print(auction['id'], n)
    for artwork in artworks:
        price = int(
            c.convert(artwork['price']['amount'], artwork['price']['currency'], 'USD'))
        artwork_url = f'https://dam.sothebys.com/dam/image/lot/{artwork["objectID"]}/primary/extra_large'
        # print(artwork_url)
        data = None
        try:
            actual_artwork_url = urllib.parse.unquote(s.head(
                artwork_url, allow_redirects=False).headers['Location'].split('?url=')[-1])
            if 's3.amazonaws.com' not in actual_artwork_url:
                print(actual_artwork_url)

        # print(actual_artwork_url)

            data = {
                'artworkUrl': actual_artwork_url,
                'auctionID': artwork['auctionId'],
                'creators': [c for c in artwork['creators']],
                'departments': [d for d in artwork['departments']],
                'price': price,
                'resultID': artwork['objectID'],
                'title': artwork['title'],
                'url': "https://www.sothebys.com" + artwork['slug'],
            }
        except KeyError:
            print('ERROR, skipping.')
            # print("https://www.sothebys.com" + artwork['slug'])
            # print(artwork['objectID'])
            continue
        if price >= 1000:
            n += 1
            collection.document(artwork['objectID']).set(data)
        elif price == 0:
            pass
        else:
            pass
            # print(data['url'])
            # Add a new doc in collection 'cities' with ID 'LA'
