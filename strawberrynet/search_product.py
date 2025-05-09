import requests
import json

def search_strawberrynet_products(search_term="apple", category_id=0, page=1, sort=8, currency="HKD"):
    url = "https://web-api.strawberrynet.com/HK/api/Product/AISearchPagedProductList"
    
    params = {
        "SearchField": search_term,
        "CatgId": category_id,
        "Page": page,
        "Sort": sort,
        "currid": currency
    }
    
    headers = {
        "authority": "web-api.strawberrynet.com",
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-type": "application/json",
        "currid": "US$",
        "langid": "1",
        "origin": "https://www.strawberrynet.com",
        "priority": "u=1, i",
        "referer": "https://www.strawberrynet.com/",
        "region": "usa",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not:A-Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
    
    # 注意：虽然请求头中有content-length:4，但实际请求体为空对象{}
    request_body = {}
    
    try:
        response = requests.post(
            url,
            headers=headers,
            params=params,
            json=request_body,
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            return data['prods'] # 返回JSON数据       
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None

# 使用示例
if __name__ == "__main__":
    result = search_strawberrynet_products(search_term="apple", page=1)
    if result:
        print("商品搜索成功！")
        print(f"总商品 ",result[0])
 
    else:
        print("商品搜索失败")