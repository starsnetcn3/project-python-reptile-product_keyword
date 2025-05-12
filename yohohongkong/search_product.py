import requests
import json

def get_search_products(keyword):
  # 目标 URL
    url = f'https://api.yohohongkong.com/web/search/product-list?keywords={keyword}&sort=best_match&order=desc&start_position=0&limit=120&lang=zh_tw'

    headers = {
        "authority": "api.yohohongkong.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        "accept-version": "1.0.0",
        "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOi0xLCJzZXNzaW9uSWQiOiJlb3dNX2YwMXdKOHk1a1NmeEU4SF9OcndkZ1ZwaG5RUiIsImlhdCI6MTc0NzAyMTk2MiwiZXhwIjoxNzQ3MDIyNTYyLCJhdWQiOiJ5b2hvaG9uZ2tvbmcuY29tIiwiaXNzIjoieW9ob2hvbmdrb25nLmNvbSJ9.H1NpnUHP4FQctIyAaMjY3N_PQwWR9NmB1O1_1vbsOTc",
        "cookie": "yohosess=s%3AeowM_f01wJ8y5kSfxE8H_NrwdgVphnQR.%2BNdhdQhYYk%2FHDWsdQIPcXf4pji2ej62W71v0tnrOQp0; _gcl_au=1.1.1983331647.1746503725; _ga=GA1.1.2136118022.1746503725; _fbp=fb.1.1746508431743.83335590213066920; refreshToken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOi0xLCJzZXNzaW9uSWQiOiJlb3dNX2YwMXdKOHk1a1NmeEU4SF9OcndkZ1ZwaG5RUiIsImlhdCI6MTc0NzAyMTM0NCwiZXhwIjoxNzQ3NjI2MTQ0LCJhdWQiOiJ5b2hvaG9uZ2tvbmcuY29tIiwiaXNzIjoieW9ob2hvbmdrb25nLmNvbSJ9._ouxyWernfSOLwpo3jbEuw5ackgBJPPuZZ91K3GbdSM; accessToken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOi0xLCJzZXNzaW9uSWQiOiJlb3dNX2YwMXdKOHk1a1NmeEU4SF9OcndkZ1ZwaG5RUiIsImlhdCI6MTc0NzAyMTM0NCwiZXhwIjoxNzQ3MDIxOTQ0LCJhdWQiOiJ5b2hvaG9uZ2tvbmcuY29tIiwiaXNzIjoieW9ob2hvbmdrb25nLmNvbSJ9.jLqbR52NSVxqdFNTCe0WOs3Sls9h1a0332VC_Rpg4_M; _ga_3WW5HH68HY=GS2.1.s1747021357$o5$g0$t1747021357$j60$l0$h0",
        "origin": "https://www.yohohongkong.com",
        "priority": "u=1, i",
        "referer": "https://www.yohohongkong.com/",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not:A-Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "x-api-key": "8d9317a5-bd40-4ce7-8ea9-11ee10af244b"
    }
    try:
        response = requests.get(url, headers=headers)
        print(response.text)
        if response.status_code == 200:
            data = json.loads(response.text)
            return data['result']
            # print(data['status'])
           
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None

if __name__ == "__main__":
    keyword='apple'
    products = get_search_products(keyword)
    try:
        with open('result1.json', 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=4)
    except Exception as e:
            print(f"写入文件时出错: {e}")