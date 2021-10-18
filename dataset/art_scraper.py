import requests
import json

from requests.sessions import session
GRAPHQL = "https://clientapi.prod.sothelabs.com/graphql"
# Get


s = requests.Session()

res = s.post(GRAPHQL, json={
             "query": "{ algoliaSearchKey { key \n timeToLive } }"}).json()
key = res['data']['algoliaSearchKey']['key']

ANGOLIA = "https://kar1ueupjd-dsn.algolia.net/1/indexes/prod_lots/query"

departments = ["Impressionist/Modern", "Contemporary Art"]

lookup_table = json.loads(open('lookup.json').read())

for i in range(len(lookup_table)):
    auctionId = lookup_table[i]['id']
    print(auctionId)
    query = """
      {
    auction(id: "XYZ") {
        sessions {
        lotCards {
            lotId
            currentBid {
            amount
            currency
            }
        }
        }
    }
    }
    """.replace("XYZ", auctionId)
    # print(query)
    sessions_merged = {}
    graphql_response = s.post(GRAPHQL, json={
        "query": query
    }).json()["data"]["auction"]["sessions"]
    # print(graphql_response)
    for sess in graphql_response:
        for card in (sess['lotCards'] or []):
            sessions_merged[card['lotId']] = card['currentBid']
    # print(sessions_merged)
    payload = {"query": "", "filters": f"auctionId:{auctionId} AND objectTypes:\"All\"", "facetFilters": [
        [f"departments:{x}" for x in departments], ["lotState:Closed"], ["withdrawn:false"]], "hitsPerPage": 1000, "page": 0, "facets": ["*"], "numericFilters": []}
    res = s.post(ANGOLIA, json=payload, headers={
        'x-algolia-application-id': 'KAR1UEUPJD', 'x-algolia-api-key': key}).json()["hits"]
    formatted_res = {}
    for item in res:
        formatted_res[item['objectID']] = item
        formatted_res[item['objectID']
                      ]['price'] = sessions_merged[item['objectID']]
    lookup_table[i]["angolia"] = res

with open("angolia_lookup_table.json", "w") as f:
    json.dump(lookup_table, f, indent=2)
