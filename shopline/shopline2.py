import re
import json
import asyncio
import aiohttp
import random
from typing import List, Dict, Optional, Tuple
from functools import wraps
from urllib.parse import unquote

# 配置
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.rngwine.com/',
    'Accept-Encoding': 'gzip, deflate',
}
TIMEOUT = aiohttp.ClientTimeout(total=30)
CONCURRENCY_LIMIT = 5
MAX_RETRIES = 3
BASE_DELAY = 1
RANDOM_DELAY_RANGE = (0.5, 1.5)
DEFAULT_IMAGE = "https://starsnet-production.oss-cn-hongkong.aliyuncs.com/png/4fb86ec5-2b42-4824-8c05-0daa07644edf.png"

# 工具函数
def get_extension(url: str) -> str:
    """健壮的扩展名提取函数"""
    if not url:
        return ''
    
    # 解码URL并清理
    decoded_url = unquote(url)
    clean_url = decoded_url.split('?')[0].split('#')[0].lower()
    
    # 支持的图片扩展名
    extensions = {
        '.jpeg': 'jpeg',
        '.jpg': 'jpg',
        '.png': 'png',
        '.webp': 'webp',
        '.gif': 'gif'
    }
    
    for ext, ext_name in extensions.items():
        if clean_url.endswith(ext):
            return ext_name
    
    return 'jpg'  # 默认值

def fix_unicode_text(text: str) -> str:
    """修复Unicode乱码"""
    if not text:
        return text
    
    # 常见乱码模式修复
    if 'ç' in text or 'å' in text:
        try:
            return text.encode('latin1').decode('utf-8')
        except:
            pass
    
    return text

def parse_product_json(json_str: str) -> Dict:
    """健壮的JSON解析函数"""
    try:
        # 尝试直接解析
        data = json.loads(json_str.encode('utf-8').decode('unicode_escape'))
        
        # 深度修复可能存在的乱码
        def deep_fix(item):
            if isinstance(item, str):
                return fix_unicode_text(item)
            elif isinstance(item, dict):
                return {k: deep_fix(v) for k, v in item.items()}
            elif isinstance(item, list):
                return [deep_fix(i) for i in item]
            return item
        
        return deep_fix(data)
    except json.JSONDecodeError:
        # 如果失败，尝试修复常见JSON格式问题
        fixed_str = re.sub(r'\\+"', '"', json_str)  # 修复转义引号
        return json.loads(fixed_str.encode('utf-8').decode('unicode_escape'))

# 重试装饰器
def async_retry(max_retries: int = MAX_RETRIES, 
               base_delay: float = BASE_DELAY,
               exceptions: Tuple = (Exception,)):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    if retries > 0:
                        delay = base_delay * (2 ** (retries - 1))
                        delay += random.uniform(*RANDOM_DELAY_RANGE)
                        print(f"Retry {retries}/{max_retries}, waiting {delay:.2f}s...")
                        await asyncio.sleep(delay)
                    return await func(*args, **kwargs)
                except exceptions as e:
                    retries += 1
                    if retries == max_retries:
                        print(f"Max retries reached for {func.__name__}: {str(e)}")
                        raise
        return wrapper
    return decorator

# 核心功能
@async_retry()
async def fetch_html(session: aiohttp.ClientSession, url: str) -> Optional[str]:
    """带重试的HTML获取"""
    try:
        async with session.get(url, headers=HEADERS, timeout=TIMEOUT) as response:
            response.raise_for_status()
            return await response.text()
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        raise

@async_retry(max_retries=2)
async def upload_image(session: aiohttp.ClientSession, image_url: str) -> str:
    """图片上传函数"""
    if not image_url:
        return DEFAULT_IMAGE
    
    # image=image_url
    extension = get_extension(image_url)
    if extension == 'jpeg':
        extension = 'jpg'
    # extension = image.split('.')[-1][0:3]
    print("extension",extension)
    payload = {"url": image_url, "extension": extension}
    
    try:
        async with session.post(
            "https://file.starsnet.com.hk/api/upload/bucket-by-url/development",
            json=payload
        ) as response:
            if response.status == 200:
                return await response.text()
            return image_url  # 上传失败返回原URL
    except Exception as e:
        print(f"Image upload failed: {e}")
        return image_url

@async_retry()
async def get_product_ids(session: aiohttp.ClientSession, list_url: str) -> List[str]:
    """获取产品ID列表"""
    html = await fetch_html(session, list_url)
    if not html:
        return []
    
    match = re.search(r"app\.value\('products', JSON\.parse\('(\[.*?\])'\)", html)
    if not match:
        return []
    
    try:
        products = parse_product_json(match.group(1))
        return [str(p['id']) for p in products]
    except Exception as e:
        print(f"Failed to parse product IDs: {e}")
        raise

@async_retry()
async def get_product_details(session: aiohttp.ClientSession, product_id: str) -> Optional[Dict]:
    """获取产品详情"""
    url = f"https://www.rngwine.com/products/{product_id}"
    html = await fetch_html(session, url)
    if not html:
        return None
    
    match = re.search(r"app\.value\('product', JSON\.parse\('({.*?})'\)", html)
    if not match:
        return None
    
    try:
        product = parse_product_json(match.group(1))
        image_url = product.get('media', [{}])[0].get('images', {}).get('original', {}).get('url', '')
        
        # 处理多语言标题
        title_translations = product.get('title_translations', {})
        cn_title = fix_unicode_text(title_translations.get('zh-hant', ''))
        en_title = fix_unicode_text(title_translations.get('en', ''))
        
        # 异步上传图片
        uploaded_url = await upload_image(session, image_url)
        
        return {
            "_id":product.get('_id', ''),
            "title": {
                "cn": cn_title,
                "en": en_title
            },
            "price": float(product.get('price', {}).get('dollars', 0)),
            "image_url": uploaded_url,
            "description": {
                "cn": cn_title,
                "en": en_title
            },
            "meta_keywords": product.get('seo_keywords', []),
            "sku": product.get('sku', ''),
            "discount": 0
        }
    except Exception as e:
        print(f"Failed to parse product {product_id}: {e}")
        raise

async def process_product(session: aiohttp.ClientSession, product_id: str, semaphore: asyncio.Semaphore):
    """处理单个产品（带并发控制）"""
    async with semaphore:
        await asyncio.sleep(random.uniform(0.5, 2))  # 随机延迟防封
        try:
            return await get_product_details(session, product_id)
        except Exception as e:
            print(f"Error processing product {product_id}: {e}")
            return None

async def main():
    """主函数"""
    semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)
    
    async with aiohttp.ClientSession(headers=HEADERS, timeout=TIMEOUT) as session:
        print("Fetching product IDs...")
        product_ids = await get_product_ids(session, "https://www.rngwine.com/categories?page=2")
        print(f"Found {len(product_ids)} products")
        
        if not product_ids:
            print("No products found")
            return
        
        print("Processing products...")
        tasks = [process_product(session, pid, semaphore) for pid in product_ids]
        products = await asyncio.gather(*tasks)
        for item in products:
            item['id'] = item.pop('_id')  # 将 _id 修改为 id
            item['variants'] = [item.copy()]  # 创建variants并复制原始项的数据

        
        valid_products = [p for p in products if p]
        with open('products.json', 'w', encoding='utf-8') as f:
            json.dump(valid_products, f, ensure_ascii=False, indent=4)
        
        print(f"Successfully saved {len(valid_products)}/{len(product_ids)} products")
        if len(valid_products) < len(product_ids):
            print("Warning: Some products failed to process")

if __name__ == "__main__":
    asyncio.run(main())