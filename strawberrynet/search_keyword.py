import requests

def get_strawberrynet_suggestions():
    url = "https://web-api.strawberrynet.com/HK/api/Search/GetAISuggestions"
    params = {
        "SearchField": "app"
    }
    
    headers = {
        "authority": "web-api.strawberrynet.com",
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9",
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
    
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            return data  # 返回JSON数据
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None

# 使用示例
if __name__ == "__main__":
    suggestions = get_strawberrynet_suggestions()
    if suggestions:
        print("搜索建议获取成功：")
        print(suggestions)
    else:
        print("获取搜索建议失败")