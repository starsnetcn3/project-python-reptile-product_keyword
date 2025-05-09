import requests

def get_zalora_products(query="milk", limit=36, offset=0, shop="m"):
    url = "https://api.zalora.com.hk/v1/dynproducts/datajet/list"
    
    params = {
        "abtest": "djAbTest_True|uuid:b69b9d5f-aa5a-46a8-9ef4-798b468c6503|enable_helios_classifier:true",
        "anonymous_id": "976b3c56-832d-4b70-bedc-bc29eb19bf4d",
        "enableRelevanceClassifier": "true",
        "fullFacetCategory": "true",
        "image_format": "webp",
        "image_quality": "70",
        "image_resize": "533.4x770",
        "limit": limit,
        "offset": offset,
        "query": query,
        "search_method": "submit search",
        "shop": shop
    }
    
    headers = {
        "authority": "api.zalora.com.hk",
        "accept": "application/json",
        # "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-language": "en-HK",
        "cookie": "DEVICE_ID=976b3c56-832d-4b70-bedc-bc29eb19bf4d; sessionCount=1; userLanguage=en; ANONYMOUS_TRACKING_ID=cbd6f0d9-15bc-4f54-926e-d6a9251f216b; mp_9993377b1929812a95bc599a0637da4b_mixpanel=%7B%22distinct_id%22%3A%20%22%24device%3A196a49b634819db-058704b922ab0e-16462c6e-240000-196a49b634819db%22%2C%22%24device_id%22%3A%20%22196a49b634819db-058704b922ab0e-16462c6e-240000-196a49b634819db%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpr%22%3A%20%5B%5D%2C%22__mpap%22%3A%20%5B%5D%7D; pxcts=09815ef6-2a50-11f0-a4e6-5750d0ad85c9; _pxvid=09815330-2a50-11f0-a4e5-9387b29b4114; _gcl_au=1.1.1271187590.1746518370; _clck=c36hud%7C2%7Cfvo%7C0%7C1952; pageCount=2; zid=011jlEePkt; _clsk=1788h57%7C1746519271275%7C2%7C1%7Cb.clarity.ms%2Fcollect; _px3=7dbb7efda143ba5f3deffb9ce9f5a330185eb9040e41e41fca864476e4ff6656:g2/gOkelNscVF9u+5b5E1VophPrtYmUR5FSu9PH3j+wvRISuz3dzRkoh8bE9u2t95cn2wFnCvFpGiWD/yTqpGg==:1000:Z37Y6JlV+bWheImMY7NyUsfkPqF+v/FcBXW1yVwhAxpdDYbuO4Kb0KHGGbedF/GI78/YfcA+OGX0vB3B6VmoUr9rrhh5aSFkblloVai5N6Keija8SwDplHL2wFI3aM/I1k5SCH4gBfqFoNv+gKunFQs9RC4QHGA1ACbYpA56g2znrTON3aXd0geIcXYVzPsuJn9jKVxuUu8SVULq2zCuu7DRcwnq8dxdbxjk0kAxig0=; _uetsid=0afe1b202a5011f0bcc377e16abfeef1; _uetvid=0afe2ef02a5011f0aea87f077eae55ab",
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
        if response.status_code == 200:
            data  = response.json()
            return data['data']['Products']
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None

# 使用示例
if __name__ == "__main__":
    products = get_zalora_products(query="milk", limit=36)
    if products:
        print("商品列表获取成功，获取数量:", products[0])
        # print("示例商品:", products.get("products", [])[0]["name"] if products.get("products") else "无商品数据")
    else:
        print("获取商品列表失败")