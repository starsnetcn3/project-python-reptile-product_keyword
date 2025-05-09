import requests
import json

def search_algolia_index(query):
    url = "https://51css5eb61-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.14.3)%3B%20Browser%3B%20Magento2%20integration%20(3.13.4)%3B%20autocomplete-core%20(1.7.1)%3B%20autocomplete-js%20(1.7.1)"
    
    # 注意：URL中已包含x-algolia-agent参数
    # url += "?x-algolia-agent=Algolia%20for%20JavaScript%20(4.14.3)%3B%20Browser%3B%20Magento2%20integration%20(3.13.4)%3B%20autocomplete-core%20(1.7.1)%3B%20autocomplete-js%20(1.7.1)"
    
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9",
        "connection": "keep-alive",
        "content-type": "application/x-www-form-urlencoded",
        "host": "51css5eb61-dsn.algolia.net",
        "origin": "https://www.broadwaylifestyle.com",
        "referer": "https://www.broadwaylifestyle.com/",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not:A-Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "x-algolia-api-key": "MTY3MmJiZTg1OTFjMDQ3OTMxN2VhNWRkMzdlN2E2YzgwN2NjNWY0ZTlhNWZlMTcxNTQ4NWE3YzFhOThjODk0ZWZpbHRlcnM9Y2F0YWxvZ19wZXJtaXNzaW9ucy5jdXN0b21lcl9ncm91cF8wKyUyMSUzRCswJnRhZ0ZpbHRlcnM9",
        "x-algolia-application-id": "51CSS5EB61"
    }
    
    try:

        query_params={"requests":[{"indexName":"magento2_live_hk_tc_suggestions","query":query,"params":"hitsPerPage=4&highlightPreTag=__aa-highlight__&highlightPostTag=__%2Faa-highlight__&clickAnalytics=true"},{"query":"apple","indexName":"magento2_live_hk_tc_products","params":"hitsPerPage=6&highlightPreTag=__aa-highlight__&highlightPostTag=__%2Faa-highlight__&analyticsTags=autocomplete&clickAnalytics=true&distinct=true&facets=%5B%22categories.level0%22%5D&numericFilters=visibility_search%3D1&ruleContexts=%5B%22magento_filters%22%2C%22%22%5D"},{"query":"apple","indexName":"magento2_live_hk_tc_categories","params":"hitsPerPage=4&highlightPreTag=__aa-highlight__&highlightPostTag=__%2Faa-highlight__&analyticsTags=autocomplete&clickAnalytics=true&distinct=true&numericFilters=include_in_menu%3D1"}]}
        # 注意：需要将请求体转换为URL编码格式
        response = requests.post(
            url,
            headers=headers,
            json=query_params,  # 直接传递已编码的字符串
            timeout=10,
        )
        print(response)
        if response.status_code == 200:
            data = response.json()
            return data['results'][0]['hits']
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None

# 使用示例
if __name__ == "__main__":

    query = "apple"
    result = search_algolia_index(query)
    if result:
        print("请求成功，返回数据：")
        print(result)
    else:
        print("请求失败")