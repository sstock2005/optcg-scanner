from scripts.constants import set_names, verbose
import requests
import json

def as_currency(amount):
    if amount >= 0:
        return '${:,.2f}'.format(amount)
    else:
        return '-${:,.2f}'.format(-amount)
    
def images(setdata: str):

    result = None
    start = 0

    set_name = set_names.get(setdata, None)
    if not set_name:
        print(f"[images::error] no hard coded set name for \"{setdata}\"")
        return

    url = "https://mp-search-api.tcgplayer.com/v1/search/request?isList=false&q="
    headers = {'Content-Type': 'application/json'}

    if verbose:
        print("[images::verbose] sending initial request")

    try:
        payload = json.dumps({
            "algorithm": "sales_dismax",
            "from": start,
            "size": 24,
            "filters": {
                "term": {
                    "productLineName": ["one-piece-card-game"],
                    "setName": [set_name],
                    "productTypeName": ["Cards"]
                }
            },
            "listingSearch": {
                "filters": {
                    "term": {"sellerStatus": "Live", "channelId": 0},
                    "range": {"quantity": {"gte": 1}},
                    "exclude": {"channelExclusion": 0}
                }
            },
            "context": {"shippingCountry": "US"},
            "settings": {"useFuzzySearch": True}
        })

        response = requests.post(url, headers=headers, data=payload).json()
        total_results = response["results"][0].get("totalResults", 0)

    except Exception as e:
        print(f"[images::error] {e}")
        return

    while start < total_results:
        if verbose:
            print(f"[images::verbose] fetching results {start} to {start + 24}")
        try:
            payload = json.dumps({
                "algorithm": "sales_dismax",
                "from": start,
                "size": 24,
                "filters": {
                    "term": {
                        "productLineName": ["one-piece-card-game"],
                        "setName": [set_name],
                        "productTypeName": ["Cards"]
                    }
                },
                "listingSearch": {
                    "filters": {
                        "term": {"sellerStatus": "Live", "channelId": 0},
                        "range": {"quantity": {"gte": 1}},
                        "exclude": {"channelExclusion": 0}
                    }
                },
                "context": {"shippingCountry": "US"},
                "settings": {"useFuzzySearch": True}
            })
            response = requests.post(url, headers=headers, data=payload).json()
            if not response.get("results") or not response["results"][0].get("results"):
                print(f"[images::warn] no results found from {start} to {start + 24}")
                break

            for result in response["results"][0]["results"]:
                found_card = result.get("customAttributes", {}).get("number", "Unknown")

                if found_card == None:
                    found_card = "None"
                    
                if result.get("rarityName", {}) == "Treasure Rare":
                    found_card = found_card + "_tr"
                
                if "Alternate Art" in result.get("productUrlName", {}):
                    found_card = found_card + "_alt"

                if "Parallel" in result.get("productUrlName", {}):
                    found_card = found_card + "_parallel"

                if "Manga" in result.get("productUrlName", {}):
                    found_card = found_card + "_manga"

                product_id = int(result.get("productId", {}))
                image_url = f"https://tcgplayer-cdn.tcgplayer.com/product/{product_id}_in_1000x1000.jpg"
                data = requests.get(image_url).content 

                f = open(f'sources/{found_card}.jpg','wb') 
                f.write(data) 
                f.close() 
                if verbose:
                    print("[images::verbose] saving image: " + found_card + ".jpg")

            start += 24
        except Exception as e:
            print(f"[images::error] {e}")
            break

def price(setdata: str):

    result = None
    start = 0

    set_name = set_names.get(setdata, None)
    if not set_name:
        print(f"[price::error] no hard coded set name for \"{setdata}\"")
        return

    url = "https://mp-search-api.tcgplayer.com/v1/search/request?isList=false&q="
    headers = {'Content-Type': 'application/json'}

    try:
        payload = json.dumps({
            "algorithm": "sales_dismax",
            "from": start,
            "size": 24,
            "filters": {
                "term": {
                    "productLineName": ["one-piece-card-game"],
                    "setName": [set_name],
                    "productTypeName": ["Cards"]
                }
            },
            "listingSearch": {
                "filters": {
                    "term": {"sellerStatus": "Live", "channelId": 0},
                    "range": {"quantity": {"gte": 1}},
                    "exclude": {"channelExclusion": 0}
                }
            },
            "context": {"shippingCountry": "US"},
            "settings": {"useFuzzySearch": True}
        })

        response = requests.post(url, headers=headers, data=payload).json()
        total_results = response["results"][0].get("totalResults", 0)
        
    except Exception as e:
        print(f"[price::error] {e}")
        return

    while start < total_results:
        if verbose:
            print(f"[price:verbose] fetching results {start} to {start + 24}")
        try:
            payload = json.dumps({
                "algorithm": "sales_dismax",
                "from": start,
                "size": 24,
                "filters": {
                    "term": {
                        "productLineName": ["one-piece-card-game"],
                        "setName": [set_name],
                        "productTypeName": ["Cards"]
                    }
                },
                "listingSearch": {
                    "filters": {
                        "term": {"sellerStatus": "Live", "channelId": 0},
                        "range": {"quantity": {"gte": 1}},
                        "exclude": {"channelExclusion": 0}
                    }
                },
                "context": {"shippingCountry": "US"},
                "settings": {"useFuzzySearch": True}
            })
            
            response = requests.post(url, headers=headers, data=payload).json()

            if not response.get("results") or not response["results"][0].get("results"):
                print("[price::warn] no results found")
                break

            for result in response["results"][0]["results"]:
                found_card = result.get("customAttributes", {}).get("number", "Unknown")

                if found_card == None:
                    found_card = "None"
                    
                if result.get("rarityName", {}) == "Treasure Rare":
                    found_card = found_card + "_tr"
                
                if "Alternate Art" in result.get("productUrlName", {}):
                    found_card = found_card + "_alt"

                if "Parallel" in result.get("productUrlName", {}):
                    found_card = found_card + "_parallel"

                if "Manga" in result.get("productUrlName", {}):
                    found_card = found_card + "_manga"
                    
                if result.get("marketPrice") == None:
                    market_price = 0.0
                else:
                    market_price = float(result.get("marketPrice"))
                
                f = open(f'sources/{found_card}.txt','w') 
                f.write(as_currency(market_price))
                f.close() 

            start += 24
        except Exception as e:
            print(f"[price::error]: {e}")
            break
