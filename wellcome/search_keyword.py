import requests
import json

def get_wellcome_search_suggestions(keyword="appl"):
    url = "https://www.wellcome.com.hk/api/item/searchSuggestions"
    
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9",
        "connection": "keep-alive",
        "content-type": "application/json;charset=UTF-8",
        "cookie": "superweb-locale=zh_HK; pickUpStoreId=; shipmentType=1; venderId=5; longitude=114.1249695; latitude=22.3433916; store=642; _ga=GA1.1.1433252170.1746501231; _fbp=fb.2.1746501231812.34882507957491783; ec-pixel-config=JTdCJTIyc2hvcElkJTIyJTNBbnVsbCUyQyUyMnNob3BQbGF0Zm9ybSUyMiUzQSUyMm93bnNpdGUlMjIlMkMlMjJ0ZWFtJTIyJTNBJTIyJUU2JTgzJUEwJUU1JUJBJUI3JTIwV2VsbGNvbWUlMjIlMkMlMjJlY2lkJTIyJTNBJTIyODViNWEzNTEtNDY2My00OTUyLTlhNTEtZGNlYzFkZjcwYzc1JTIyJTJDJTIyZW5hYmxlUGl4ZWwlMjIlM0F0cnVlJTJDJTIydHhMaW5rVHJhY2tpbmdMaWZldGltZSUyMiUzQTMwJTdE; ec-token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc0Fub255bW91cyI6InRydWUiLCJyb2xlIjowLCJ0Ijoi5oOg5bq3IFdlbGxjb21lIiwiZCI6Imt0NkN5NnBoNUw2dWRLY1lDRVhSbmsxUENWdXlVMERrQk5aUUtTbTBPNEk9IiwiZSI6Imt0NkN5NnBoNUw2dWRLY1lDRVhSbnJaNVRyZVJUNHViSUl0YjVsaEJOY1hvQk9RNlJTSml0Nm9YSFFLalVDZUhlaGtKQ1daMXZRS24xdWloSXZtVDhRPT0iLCJpc0FkbWluIjoiZmFsc2UiLCJzc28iOiJmYWxzZSJ9.xAR0LZmn3-EP_8yJD6dkj9KpGtaKH1OBQlbtvJ4WzuQ; is_general_subscriber_closed=true; __ocssid=u02x2rje-macb5j7j.1746523761535.1746523761536; __ocmm=-180357582; _ga_0ZXV7S2FZK=GS2.1.s1746523762$o3$g0$t1746523807$j15$l0$h1629882604",
        "domain-flag": "wellcome",
        "host": "www.wellcome.com.hk",
        "origin": "https://www.wellcome.com.hk",
        "referer": "https://www.wellcome.com.hk/",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not:A-Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
    
    payload = {
        "param": {
            "globalSelection": False,
            "keyword": keyword,
            "limit": 0,
            "stores": [{
                "businessCode": 1,
                "defaultChosed": False,
                "erpStoreId": 642,
                "name": "",
                "showTrack": False,
                "timestamp": "",
                "venderId": 5
            }]
        },
        "comm": {
            "dmTenantId": 15,
            "venderId": 5,
            "businessCode": 1,
            "origin": 26,
            "superweb-locale": "zh_HK",
            "storeId": 642,
            "pickUpStoreId": "",
            "shipmentType": 1
        }
    }
    
    try:
        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(payload),
            timeout=10,
            verify=False
        )
        if  response.status_code == 200:
            data = response.json()
            return data['data']
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None

# 使用示例
if __name__ == "__main__":
    suggestions = get_wellcome_search_suggestions(keyword="apple")
    if suggestions:
        print("搜索建议获取成功：")
        print(json.dumps(suggestions, indent=2, ensure_ascii=False))
    else:
        print("获取搜索建议失败")