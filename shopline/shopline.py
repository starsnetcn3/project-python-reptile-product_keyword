import requests
import asyncio
import aiohttp
import json
import re
import time
import random
from typing import List, Dict, Optional
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
# 配置


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.rngwine.com/',  # 模拟真实用户来源
    'Accept-Encoding': 'gzip, deflate',  # 避免使用br压缩
}
TIMEOUT = aiohttp.ClientTimeout(total=30)
CONCURRENCY_LIMIT = 5  # 控制并发请求数

async def fetch_html(session: aiohttp.ClientSession, url: str) -> Optional[str]:
    try:
        async with session.get(url, headers=HEADERS, timeout=TIMEOUT) as response:
            response.raise_for_status()
            return await response.text()
    except Exception as e:
        print(f"请求失败 {url}: {e}")
        return None

async def upload_image(session: aiohttp.ClientSession, image_url: str) -> str:
    if not image_url:
        return "https://starsnet-production.oss-cn-hongkong.aliyuncs.com/png/4fb86ec5-2b42-4824-8c05-0daa07644edf.png"
    
    extension = image_url.split('.')[-1][:3]
    payload = {"url": image_url, "extension": extension}
    
    try:
        async with session.post(
            "https://file.starsnet.com.hk/api/upload/bucket-by-url/development",
            json=payload
        ) as response:
            if response.status == 200:
                return await response.text()
            return image_url  # 上传失败则返回原URL
    except Exception:
        return image_url

async def get_product_ids(session: aiohttp.ClientSession, list_url: str) -> List[str]:
    html = await fetch_html(session, list_url)
    if not html:
        return []
    
    match = re.search(r"app\.value\('products', JSON\.parse\('(\[.*?\])'\)", html)
    if not match:
        return []
    
    try:
        products = json.loads(match.group(1).encode('utf-8').decode('unicode_escape'))
        return [p['id'] for p in products]  # 限制测试数量
    except (json.JSONDecodeError, KeyError) as e:
        print(f"解析产品ID失败: {e}")
        return []

async def get_product_details(session: aiohttp.ClientSession, product_id: str) -> Optional[Dict]:
    #         # 避免频繁请求导致被封，设置延迟
    # time.sleep(1)
    url = f"https://www.rngwine.com/products/{product_id}"
    html = await fetch_html(session, url)
    if not html:
        return None
    
    match = re.search(r"app\.value\('product', JSON\.parse\('({.*?})'\)", html)
    if not match:
        return None
    
    try:
        product = json.loads(match.group(1).encode('utf-8').decode('unicode_escape'))
        image_url = product.get('media', [{}])[0].get('images', {}).get('original', {}).get('url', '')
        
        # 异步上传图片
        uploaded_url = await upload_image(session, image_url)
        
        return {
            "title": {
                "cn": product.get('title_translations', {}).get('zh-hant', ''),
                "en": product.get('title_translations', {}).get('en', '')
            },
            "price": float(product.get('price', {}).get('dollars', 0)),
            "image_url": uploaded_url,
            "description": {
                "cn": product.get('title_translations', {}).get('zh-hant', ''),
                "en": product.get('title_translations', {}).get('en', '')
            },
            "meta_keywords": product.get('seo_keywords', []),
            "sku": product.get('sku', ''),
            "discount": 0
        }
    except Exception as e:
        print(f"解析产品详情失败 {product_id}: {e}")
        return None

async def main():
    async with aiohttp.ClientSession(headers=HEADERS, timeout=TIMEOUT) as session:
        # 获取产品ID列表
        product_ids = await get_product_ids(session, "https://www.rngwine.com/categories?page=2")
        print(product_ids)
        if not product_ids:
            print("未获取到产品ID")
            return
        
        # 并发获取产品详情
        tasks = [get_product_details(session, pid) for pid in product_ids]
        products = await asyncio.gather(*tasks)
        
        # 保存结果
        valid_products = [p for p in products if p]
        with open('products.json', 'w', encoding='utf-8') as f:
            json.dump(valid_products, f, ensure_ascii=False, indent=4)
        print(f"成功保存 {len(valid_products)} 个产品")

if __name__ == "__main__":
    asyncio.run(main())