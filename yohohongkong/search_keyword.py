import requests
import json

def get_search_suggestions(keyword):
    url = f'https://api.yohohongkong.com/web/search/suggest?keywords={keyword}&lang=zh_tw'
    print(url)
    headers = {
        "accept": "application/json, text/plain, */*",
        # "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9",
        "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOi0xLCJzZXNzaW9uSWQiOiJlb3dNX2YwMXdKOHk1a1NmeEU4SF9OcndkZ1ZwaG5RUiIsImlhdCI6MTc0NjUwMzcxOCwiZXhwIjoxNzQ2NTA0MzE4LCJhdWQiOiJ5b2hvaG9uZ2tvbmcuY29tIiwiaXNzIjoieW9ob2hvbmdrb25nLmNvbSJ9.GQPu-pdNwRTuxOyTtpH1vZNkQ3-08mpRUvyre2QpRfU",
        "cookie": "refreshToken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOi0xLCJzZXNzaW9uSWQiOiJlb3dNX2YwMXdKOHk1a1NmeEU4SF9OcndkZ1ZwaG5RUiIsImlhdCI6MTc0NjUwMzcxOCwiZXhwIjoxNzQ3MTA4NTE4LCJhdWQiOiJ5b2hvaG9uZ2tvbmcuY29tIiwiaXNzIjoieW9ob2hvbmdrb25nLmNvbSJ9.7H8H1rQ2Hi99qdW02XPsyrS6MZf567SJJ72rydHyNrQ; yohosess=s%3AeowM_f01wJ8y5kSfxE8H_NrwdgVphnQR.%2BNdhdQhYYk%2FHDWsdQIPcXf4pji2ej62W71v0tnrOQp0; _gcl_au=1.1.1983331647.1746503725; _ga_3WW5HH68HY=GS2.1.s1746503724$o1$g0$t1746503724$j60$l0$h0; _ga=GA1.1.2136118022.1746503725",
        "origin": "https://www.yohohongkong.com",
        "referer": "https://www.yohohongkong.com/",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "x-api-key": "8d9317a5-bd40-4ce7-8ea9-11ee10af244b"
    }
    
    try:
        response = requests.get(url, headers=headers)
        # print(response.text)
        raw_content = response.content
        # decoded_content = raw_content.decode('utf-8', errors='replace')  # 使用 utf-8 解码
        # print("111",decoded_content)
        if response.status_code == 200:
            data = json.loads(response.text)
            # print(data['status'])
            return data['result']  # 返回 JSON 格式的数据  
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None

# 示例调用
if __name__ == "__main__":
    keyword='apple'
    suggestions = get_search_suggestions(keyword)
    print(suggestions)