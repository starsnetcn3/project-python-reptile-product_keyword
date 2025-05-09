import requests

# 要换token

def fetch_pns_autocomplete(query):
    """
    Fetch autocomplete suggestions from PNS API.
    
    Parameters:
        query (str): The search query string.
    
    Returns:
        dict: Response data if the request is successful.
        str: Error message if the request fails.
    """
    url = f'https://api.pns.hk/api/v2/pnshk/search/autocomplete/{query}?config=SearchBoxComponent&fields=DEFAULT,SUGGESTIONS&lang=zh_HK&curr=HKD'
    headers = {
        "accept": "application/json, text/plain, */*",
        "authorization": "bearer x3eVgb2k5_qE5VdfJUzNYvPCdCA",
        "cache-control": "no-cache, no-store, must-revalidate, post-check=0, pre-check=0",
        "expires": "0",
        "if-modified-since": "Tue, 06 May 2025 07:01:31 GMT",
        "pragma": "no-cache",
        "queue-target": "https://www.pns.hk/zh-hk/",
        "queueit-target": "https://www.pns.hk/zh-hk/",
        "referer": "https://www.pns.hk/",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "vary": "*"
    }
    params = {
        "config": "SearchBoxComponent",
        "fields": "DEFAULT,SUGGESTIONS",
        "lang": "zh_HK",
        "curr": "HKD",
        "query": query
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        # Check if the request was successful
        if response.status_code == 200:
            # print("1111",response.json())
            data = response.json()
            return data['suggestions']  # Return JSON response data
        else:
            return f"Error: Received status code {response.status_code}"
    except requests.RequestException as e:
        return f"Request failed: {e}"

# Example usage
if __name__ == "__main__":
    query = "pns"  # Replace with your search query
    result = fetch_pns_autocomplete(query)
    print(result)