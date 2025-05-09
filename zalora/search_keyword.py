import requests

def get_zalora_suggestions(query="apple", limit=5):
    url = "https://api.zalora.com.hk/v1/suggestions/genericv2/datajet"
    
    params = {
        "limit": limit,
        "query": query
    }
    
    headers = {
        "authority": "api.zalora.com.hk",
        "accept": "application/json",
        # "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-language": "en-HK",
        "cookie": "DEVICE_ID=976b3c56-832d-4b70-bedc-bc29eb19bf4d; sessionCount=1; pageCount=1; userLanguage=en; ANONYMOUS_TRACKING_ID=cbd6f0d9-15bc-4f54-926e-d6a9251f216b; zid=8tZ2g1dQbp; mp_9993377b1929812a95bc599a0637da4b_mixpanel=%7B%22distinct_id%22%3A%20%22%24device%3A196a49b634819db-058704b922ab0e-16462c6e-240000-196a49b634819db%22%2C%22%24device_id%22%3A%20%22196a49b634819db-058704b922ab0e-16462c6e-240000-196a49b634819db%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpr%22%3A%20%5B%5D%2C%22__mpap%22%3A%20%5B%5D%7D; pxcts=09815ef6-2a50-11f0-a4e6-5750d0ad85c9; _pxvid=09815330-2a50-11f0-a4e5-9387b29b4114; _gcl_au=1.1.1271187590.1746518370; _uetsid=0afe1b202a5011f0bcc377e16abfeef1; _uetvid=0afe2ef02a5011f0aea87f077eae55ab; _clck=c36hud%7C2%7Cfvo%7C0%7C1952; _clsk=1788h57%7C1746518376245%7C1%7C1%7Cb.clarity.ms%2Fcollect; _px3=6f76bb267621fd4e7fc1299e633b5ca72f3372d160fbea451c67740bc8a3b4e5:LY5g6Ym9APs9ewvQ1EbCGOdH3TVObBYYrYtRZ0nMbK5OzwKiiIYaiAzptG/Va9mO6qq3h7AdyMK2hwkmCMs+LQ==:1000:9LjO3NReYadxV8vmWw3/JQVd7kJW3tvTmPfV9t2sSY6wBzv83qgv9pd3U1u0LsmW4mUegK0+yvbVQNjOr9pAapKGN4owGtW4RFcFBDYxqdyjAnDOhNukq2ESWy0bmAKxHdZMwznHvLkVN5Zb1wLj6kHV1kuFk/FRLgap3XVKcublhZFXvPhXngh+Q3gZC2v3LpsRKR5ulK4zCFK5IhxvYUEDNSbWoCFyKMpvd+sbDdU=",
        "origin": "https://www.zalora.com.hk",
        "priority": "u=1, i",
        "referer": "https://www.zalora.com.hk/",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not:A-Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=10
        )
        print(response.text)
        if response.status_code == 200:
            data  = response.json()
            return data['data']['SearchSuggestions']
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None

# 使用示例
if __name__ == "__main__":
    suggestions = get_zalora_suggestions(query="apple", limit=5)
    if suggestions:
        print("搜索建议获取成功：")
        print(suggestions)
    else:
        print("获取搜索建议失败")