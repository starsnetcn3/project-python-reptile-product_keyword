import requests
import json

def get_search_products(keyword):
  # 目标 URL
    url = "https://www.yohohongkong.com/_next/data/c5zfqlY2lXgNMdt_J4-6F/zh-hk/keyword/apple.json?keyword=apple"
    print(url)

    headers = {
        "authority": "www.yohohongkong.com",
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9",
        "cookie": "refreshToken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOi0xLCJzZXNzaW9uSWQiOiJlb3dNX2YwMXdKOHk1a1NmeEU4SF9OcndkZ1ZwaG5RUiIsImlhdCI6MTc0NjUwMzcxOCwiZXhwIjoxNzQ3MTA4NTE4LCJhdWQiOiJ5b2hvaG9uZ2tvbmcuY29tIiwiaXNzIjoieW9ob2hvbmdrb25nLmNvbSJ9.7H8H1rQ2Hi99qdW02XPsyrS6MZf567SJJ72rydHyNrQ; yohosess=s%3AeowM_f01wJ8y5kSfxE8H_NrwdgVphnQR.%2BNdhdQhYYk%2FHDWsdQIPcXf4pji2ej62W71v0tnrOQp0; YOHO_POP_UP_ADV_FIRST_LOADED=yohobanner-popup-first-loaded; YOHO_FLOAT_PROMOTE_FIRST_LOADED=yohobanner-float-promote-first-loaded; _gcl_au=1.1.1983331647.1746503725; _ga_3WW5HH68HY=GS2.1.s1746503724$o1$g0$t1746503724$j60$l0$h0; _ga=GA1.1.2136118022.1746503725",
        "priority": "u=1, i",
        "referer": "https://www.yohohongkong.com/zh-hk",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "x-nextjs-data": "1"
    }
    try:
        response = requests.get(url, headers=headers)
        # print(response.text)
        if response.status_code == 200:
            data = json.loads(response.text)
            # print(data['status'])
            return data['pageProps']['fallback']['$inf$#url:\"https://api.yohohongkong.com/web/search/product-list\",params:#start_position:0,sort:\"best_match\",order:\"desc\",limit:120,lang:\"zh-hk\",keywords:\"apple\",,method:\"GET\",']  # 返回 JSON 格式的数据  
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None






# 示例调用
if __name__ == "__main__":
    keyword='apple'
    products = get_search_products(keyword)
    print(products[0][0])