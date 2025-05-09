import requests
import json

# 这里需要更改cookie

def fetch_fortress_autocomplete(keyword: str, auth_token: str = None):
    """
    获取Fortress香港的自动补全建议
    
    参数:
        keyword (str): 搜索关键词
        auth_token (str): 可选的Bearer token，如果不提供会使用默认值
        
    返回:
        Optional[Dict]: 解析后的JSON数据，失败时返回None
    """
    # 动态构造URL
    url = f"https://api.fortress.com.hk/api/v2/ftrhk/search/autocomplete/{keyword}?config=SearchBoxComponent&fields=DEFAULT,AUTOCOMPLETE,SUGGESTIONS&lang=en&curr=HKD"
    
    # 默认headers配置
    headers = {
        "authority": "api.fortress.com.hk",
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache, no-store, must-revalidate, post-check=0, pre-check=0",
        "origin": "https://www.fortress.com.hk",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.fortress.com.hk/",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not:A-Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "vary": "*",
        "cookie": "PIM-SESSION-ID=NTah1n4FwTZxF0xh; ROUTE=.api-6667d5f685-lp76v; _gcl_au=1.1.196649336.1746503862; _gid=GA1.3.1106562324.1746503865; _fbp=fb.2.1746503865091.13096066276907968; OptanonConsent=isGpcEnabled=0&datestamp=Tue+May+06+2025+15%3A01%3A07+GMT%2B0800+(%E9%A6%99%E6%B8%AF%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202411.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=def3ad97-0ae0-4815-a771-09b3526c3f6d&interactionCount=1&isAnonUser=1&landingPath=https%3A%2F%2Fwww.fortress.com.hk%2Fen%2F&groups=C0001%3A1%2CC0003%3A1%2CC0009%3A1; AKA_A2=A; bm_sz=E362773DD8FC0E91D0DA3832E9B4413B~YAAQLtgjF5MZxn6WAQAA62TFpBvIwBQWRCFtCQMyi0Rkv3qfa3zoLNn1jSzB77i/K247EHl/nbGIVfGGggQ6fgBTVF6e+lfaNY07cOpoqjq2xr33DXsJQGrj8ea4fU797XL8Bml30ky/3u2ec0Tc66TB8wpGkJNq7RJTJ7bRB6ELMtsEWxqvr8RDRdX5UCTKWtKIbn0h93a+A1E7310J34p995MprbiQOWvvKTai9vBrc28STb9MHoZRR5mB/IQUU6TcZZgUjnL7Og6M9MCI7zuMrE6p1FujmAiQ2izp5cqnl5hTwclo/rWfKIAdHiI/3NOzuPs1pggemaw1AhP7MBhbenNWdsnpIfMQ23Z2hc8MU3mpDT2M2CDHAvf2BZ7xMI3LYzvLlAcamuWTsyeP2Iyd~3420214~3686713; _abck=BBB5FEAE168DA0311E3BE4F9E5247A0C~0~YAAQLtgjF7UZxn6WAQAA/2XFpA0zZvQQ9/hekWx1u6gUv96rcSni2ouZcL/x1J8SHkvG4GQDqhyiJGC/fYkoDTrx5+zq2muwYrG5IuC23PwtQzrOc8OEnfMA2XV0eLIxS7m1Z1IipUOngqY80fwDYZHrJLLntLF6j1/aKmCb/hr7B+mUcXX8KfuozG1SVZTSoF3W0x1RInFgw3C4uXwfT+yyRcSbW8uMSUlKpHiHIhhaslIg+WyzCDX4lM0kmmA4bNUpmHfhQHjhmeqfflLPlWMqfSJjPKufb2UH95rYg1z1Kto/2BGTVkXLNbU1Wp7Iu5v0+nQDbf1Px355by43mJVf/ynIVjlTXpFRfdd+GxjN0SsjVp9wY3Y89wgo/cNxejdlEEQsbonuYnshor5X6NX5qYy9htKHPreNULhIbG9vQA3hFyqoPScJsJ0O5sxHebc6XraRa12+5Vme8MbGulndfEh2wMBbCqfS52mwTkH88R6rQO+YSqO9KdvRrGoi5FbQmbCVywgqqfXq+fvgsX5rm3fHHIP6bpK6x+m+2CycU0jeI7/B2eNZYlGg3ZkgDkTceFfKbhtjFAQz6fQA6SsSg23khB0KsP5uz9FdPhwCElMBZxz44WpJjgrZGA==~-1~-1~-1; authorization=fw7WRzbkc1WseHixcLHL31zEnFg; token_type=guest; ak_bmsc=3EEEE4718ED8B0CC62DE6B3B34A5F38B~000000000000000000000000000000~YAAQBNgjF9ijVn2WAQAAqMXFpBvpw4a967UWnk3pQ4rSBodgDy0oojTaJ0Cq/CUCzaBGHDaq0So9O9onoFHyOrSBQ6cVM9e+zlGU1n8/daBHjSth2591DZwRFvTNI5Oo9mybbeDipONjqaApUaGk8Dry3TDwBwophNehrtRn3T0fx4znxlNISP5pk4ZgDUJEAqWYQFmtN3m8hgnT1x0CgTYAd6aqk7C3fAfcTgRmMiOBQIftNhPMx0cd3ESC44mVbEXczBiQ4eUniRWJWKlN2TT6OLveWC/4tYE9CKwFTA82GZkAZGL5O7kRW2/Xpehr7i93Qv2WodJ8c9eJVndZqav+QU65QCgt2gpH6rxSaKXVeitHgPTaxwweCh0nkH9AVgCyX+7V6XUFxzgaQQuntypjrcuL7tIN02fFWlKBa8tPNXyGWxtH8yMRMnKJsph9Kj76QBSwXsybwR8=; bm_sv=315DCE64C62AFF17E9C130EF025D308C~YAAQBNgjFxOlVn2WAQAAktDFpBvwsDmZggmLfG1pgVzHvlTsaa5tGssKzyPcsm2+Ux6eqzMAFPq3AJrdgD3GXBoW6KG7GtokRPBnyjKp+ndmrrLvmVOdGpYs9jHu/njWp2D2MHhJjtvnjeM+fCwGKPR9SaJup1xMG+KFQVm+7DngcbkJbOgk77hFpHqVbeb2wo03JbNsurzSl0K/sXYZmB293M6qRwtBPHg7Uhgdt2SbEYW/2tEllcBPU997vOtqzonKkhE=~1; _ga=GA1.3.1223661085.1746503862; _gat_UA-31289854-2=1; _dc_gtm_UA-31289854-2=1; _ga_GPE6FF4J9Y=GS2.1.s1746521149$o5$g0$t1746521168$j0$l0$h18000416"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=15,
            verify=True  # 保持SSL验证，如遇证书问题可设为False
        )

        # 检查响应状态
        response.raise_for_status()
        print(response.text)
        if response.status_code == 200:
            data = json.loads(response.text)
            return data['suggestions']
        # # 处理可能的压缩响应
        # if response.headers.get('Content-Encoding') == 'gzip':
        #     import gzip
        #     import io
        #     compressed_stream = io.BytesIO(response.content)
        #     decompressed = gzip.GzipFile(fileobj=compressed_stream).read()
        #     return json.loads(decompressed.decode('utf-8'))

        # return response.json()

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {type(e).__name__}: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"响应状态码: {e.response.status_code}")
            print(f"响应头: {e.response.headers}")
            print(f"响应内容 (前200字符): {e.response.text[:200]}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON解析失败: {str(e)}")
        print(f"原始响应: {response.text[:500]}")
        return None

# 使用示例
if __name__ == "__main__":
    # 测试搜索  关键词
    result = fetch_fortress_autocomplete("apple")
    
    if result:
        print("成功获取数据:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("请求失败，请检查错误信息")