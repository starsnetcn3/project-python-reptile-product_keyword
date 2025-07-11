import requests
from requests.adapters import HTTPAdapter, Retry


def main():
    pass

if __name__ == "__main__":
    urls = [
        {
        "name": "香港島",
        "url": "https://www.28hse.com/estate/"
        },
        # {
        # "name": "九龍",
        # "url": "https://hk.centanet.com/estate/list/%E4%B9%9D%E9%BE%8D/4-KL"
        # },
        # {
        # "name": "新界東",
        # "url": "https://hk.centanet.com/estate/list/%E6%96%B0%E7%95%8C%E6%9D%B1/4-NE"
        # },
        # {
        # "name": "新界西",
        # "url": "https://hk.centanet.com/estate/list/%E6%96%B0%E7%95%8C%E8%A5%BF/4-NW"
        # }
    ]
    for url in urls:
        print(f"正在获取数据: {url['name']}, URL: {url['url']}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive'
        }
        response = requests.get(url['url'], verify=False, timeout=10)
        if response.get('status') == 'success':
            print(f"数据获取成功: {url['name']}")
        else:
            print(f"数据获取失败: {url['name']}, 错误信息: {response.get('message', '未知错误')}")

    main()