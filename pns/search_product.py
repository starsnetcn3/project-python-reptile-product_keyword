import requests
from datetime import datetime, timedelta
# 要换token
def fetch_pns_hk_search_products(query="apple"):
    # 动态生成 if-modified-since 时间（当前时间）
    # current_time = datetime.now()
    # if_modified_since = current_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
    
    url = "https://api.pns.hk/api/v2/pnshk/products/search"
    params = {
        "fields": "FULL",
        "query": f"{query}:mostRelevant",
        "pageSize": 18,
        "sort": "mostRelevant",
        "useDefaultSearch": "false",
        "brandRedirect": "true",
        "ignoreSort": "false",
        "lang": "zh_HK",
        "curr": "HKD"
    }
    
    headers = {
        "accept": "application/json, text/plain, */*",
        "authorization": "bearer x3eVgb2k5_qE5VdfJUzNYvPCdCA",
        "cache-control": "no-cache, no-store, must-revalidate, post-check=0, pre-check=0",
        "expires": "0",
        "if-modified-since": "Tue, 06 May 2025 07:15:54 GMT",
        "pragma": "no-cache",
        "queue-target": f"https://www.pns.hk/zh-hk/search?text={query}&useDefaultSearch=false&brandRedirect=true",
        "queueit-target": f"https://www.pns.hk/zh-hk/search?text={query}&useDefaultSearch=false&brandRedirect=true",
        "referer": "https://www.pns.hk/",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not:A-Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "vary": "*"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        # response.raise_for_status()  # 检查HTTP错误
        if response.status_code == 200:
            data = response.json()
            return data['products']
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None

# 使用示例
if __name__ == "__main__":
    result = fetch_pns_hk_search_products()
    if result:
        print("请求成功，返回数据示例：")
        print(result[0])  # 打印第一条产品数据
    else:
        print("请求失败")