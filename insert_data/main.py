import requests
import time
from datetime import datetime
import re
import json
import asyncio
import aiohttp
import random
from typing import List, Dict, Optional, Tuple
from functools import wraps
from urllib.parse import unquote


# 登录所需的用户凭证
payload = {
    "login_id": "su@starsnet.com.hk",
    "password": "Password12345"
}

# shopline配置
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

def login(login_url):
    # 发送POST请求
    response =  requests.post(f"{login_url}/auth/login", json=payload)
    print("response",response)
    # 检查响应状态
    if response.status_code == 200 or response.status_code == 201:
        # 登录成功
        print("登录成功！登陆的url:" ,login_url)
        # 获取返回的数据（如token等）
        data = response.json()
        return data['token']
    else:
        # 登录失败
        print("登录失败！")
        print(f"状态码: {response.status_code}, 响应内容: {response.text}")

# shopify 获取原始数据 start
def fetch_and_transform_products_shopfiy(shop_url):
    # 获取原始数据
    print("-----shopify----start---")
    print("--------------now shop_url",shop_url)
    response = requests.get(shop_url,verify=False)
    products_data = response.json().get('products', [])
    
    transformed_products = []
    print(len(products_data))
    for product in products_data:
        # 处理 tags 字段 - 确保是列表格式
        # tags = product.get('tags', [])
        # if isinstance(tags, str):  # 如果 tags 是字符串，按逗号分割
        #     tags = [tag.strip() for tag in tags.split(',')]
        
        # 处理 variants 变体信息
        # variants = []
        # for variant in product.get('variants', []):
        #     variants.append({
        #         "price": float(variant.get('price', 0)),
        #         "sku": variant.get('sku', ''),
        #         # 可以添加其他需要的变体字段，例如：
        #         "variant_id": variant.get('id'),
        #         "title":variant.get('title', ''),
        #         # "inventory_quantity": variant.get('inventory_quantity', 0)
        #     })
        
        # # 构建转换后的产品数据
        # transformed = {
        #     "_id":product.get('id',''),
        #     "title": {
        #         "cn": product.get('title', ''),
        #         "en": product.get('title', '')
        #     },
        #     "variants": variants,  # 包含所有变体的数组
        #     "image_url": product.get('images', [{}])[0].get('src', '') if product.get('images') else '',
        #     "description": {
        #         "cn": product.get('body_html', '').replace('<p>', '').replace('</p>', ''),
        #         "en": product.get('body_html', '').replace('<p>', '').replace('</p>', '')
        #     },
        #     "meta_keywords": product.get('tags', '') if product.get('tags') else [],
        #     "discount": 0  # 根据业务需求可以计算折扣
        # }
        # image=transformed['image_url']

        # 上传【图片
        # # 后缀
        # images = product.get('images', [])
        # upload_images = []
        # for image in images:
        #     extension = image['src'].split('.')[-1][0:3]
        #     print("2222",extension)
        #     body = {
        #         "url": image['src'],
        #         "extension": extension
        #     }
        #     res = requests.post("https://file.starsnet.com.hk/api/upload/bucket-by-url/development",
        #                         json=body)
        #     print("20002202020",res.status_code,body)
        #     if res.status_code == 500:
        #         image['src'] = 'https://starsnet-production.oss-cn-hongkong.aliyuncs.com/png/4fb86ec5-2b42-4824-8c05-0daa07644edf.png'
        #         # product["images"][0]['image_url'] = 'https://starsnet-production.oss-cn-hongkong.aliyuncs.com/png/4fb86ec5-2b42-4824-8c05-0daa07644edf.png'
        #     elif res.status_code == 200:
        #         print('res.text',res.text)
        #         image['src'] = res.text
            
        #     upload_images.append(image)
        # # print(transformed)
        # product['images'] = upload_images

        # # 变体的图片
        # variants = product.get('variants', [])
        # upload_variants=[]
        # for variant in variants:
        #     extension = variant['featured_image']['src'].split('.')[-1][0:3]
        #     print("2222",extension)
        #     body = {
        #         "url": variant['featured_image']['src'],
        #         "extension": extension
        #     }
        #     res = requests.post("https://file.starsnet.com.hk/api/upload/bucket-by-url/development",
        #                         json=body)
        #     print("20002202020",res.status_code,body)
        #     if res.status_code == 500:
        #         variant['featured_image']['src'] = 'https://starsnet-production.oss-cn-hongkong.aliyuncs.com/png/4fb86ec5-2b42-4824-8c05-0daa07644edf.png'
        #         # product["images"][0]['image_url'] = 'https://starsnet-production.oss-cn-hongkong.aliyuncs.com/png/4fb86ec5-2b42-4824-8c05-0daa07644edf.png'
        #     elif res.status_code == 200:
        #         print('res.text',res.text)
        #         variant['featured_image']['src'] = res.text
            
        #     upload_variants.append(variant)
        # # print(transformed)
        # product['variants'] = upload_variants

        transformed_products.append(product)
    
    return transformed_products
# shopify 获取原始数据 end

# shopline 获取原始数据 start
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
    # print("extension",extension)
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

async def fetch_and_transform_products_shopline(shop_url):
    """主函数"""
    print("----shopline----start---")
    print("--------------now shop_url",shop_url)
    
    semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)
    
    async with aiohttp.ClientSession(headers=HEADERS, timeout=TIMEOUT) as session:
        print("Fetching product IDs...")
        product_ids = await get_product_ids(session, shop_url)
        print(f"Found {len(product_ids)} products")
        
        if not product_ids:
            print("No products found")
            return
        
        print("Processing products...")
        tasks = [process_product(session, pid, semaphore) for pid in product_ids]
        products = await asyncio.gather(*tasks)
        for item in products:
            item['id'] = item.pop('_id')  # 将 _id 修改为 id
            item['variants'] = [item.copy()]  
        return products
        
        # valid_products = [p for p in products if p]
        # with open('products.json', 'w', encoding='utf-8') as f:
        #     json.dump(valid_products, f, ensure_ascii=False, indent=4)
        
        # print(f"Successfully saved {len(valid_products)}/{len(product_ids)} products")
        # if len(valid_products) < len(product_ids):
        #     print("Warning: Some products failed to process")

# shopline 获取原始数据 end


# 插入数据库 start
def create_headers(token=None):
    """创建HTTP请求头"""
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }


def insert_data_shopify(data,markup,token,base_url):
    """插入或更新数据"""
    for product_item in data:
        product_item_id = product_item["id"]
        
        # 通过shopify的id去mongodb里面查询all的product
        all_product_data = requests.get(
            f"{base_url}/common/all/MProduct",
            headers=create_headers(token),
            params={
                "shopify_product_id": json.dumps({"$in": [str(product_item_id)]})
            }
        ).json()

        # 1. 插入新的产品
        if not all_product_data["data"]:
            print(f"===insert product id {product_item_id}")
            
            # 插入产品
            insert_product = requests.post(
                f"{base_url}/common/create/MProduct",
                json={
                    "shopify_product_id": str(product_item_id),
                    "title": {
                        "en": product_item["title"],
                        "zh": product_item["title"],
                        "cn": product_item["title"]
                    },
                    "short_description": {
                        "en": product_item["handle"],
                        "zh": product_item["handle"],
                        "cn": product_item["handle"]
                    },
                    "long_description": {
                        "en": product_item["body_html"],
                        "zh": product_item["body_html"],
                        "cn": product_item["body_html"]
                    },
                    "status": "ACTIVE",
                    "shopify_link": "",
                    "images": [item["src"] for item in product_item["images"]]
                },
                headers=create_headers(token)
            ).json()

            # 插入的product_id
            insert_product_id = insert_product["data"]["_id"]

            # 插入产品变体
            for variant_item in product_item["variants"]:
                print(f"======insert variant id {variant_item['id']}")
                requests.post(
                    f"{base_url}/common/create/MProductVariant",
                    json={
                        "product_id": insert_product_id,
                        "shopify_product_variant_id": str(variant_item["id"]),
                        "title": {
                            "en": variant_item["title"],
                            "zh": variant_item["title"],
                            "cn": variant_item["title"]
                        },
                        "short_description": {
                            "en": product_item["handle"],
                            "zh": product_item["handle"],
                            "cn": product_item["handle"]
                        },
                        "long_description": {
                            "en": product_item["body_html"],
                            "zh": product_item["body_html"],
                            "cn": product_item["body_html"]
                        },
                        "price": float(variant_item["price"]*(1 + markup)),
                        "status": "ACTIVE",
                        "shopify_link": "",
                        "images": [variant_item.get("featured_image", {}).get("src")]
                    },
                    headers=create_headers(token)
                )
        # 2. 更新产品
        else:
            print(f"===update product id {product_item_id}")
            
            # 通过shopify_id去查找需要更新的产品id
            get_one_product = requests.get(
                f"{base_url}/common/all/MProduct",
                headers=create_headers(token),
                params={
                    "shopify_product_id": json.dumps({"$in": [str(product_item_id)]})
                }
            ).json()

            # 拿到需要更新的产品id
            update_product_id = get_one_product["data"][0]["_id"]

            # 更新产品
            requests.put(
                f"{base_url}/common/update/{update_product_id}/MProduct",
                json={
                    "title": {
                        "en": product_item["title"],
                        "zh": product_item["title"],
                        "cn": product_item["title"]
                    },
                    "short_description": {
                        "en": product_item["handle"],
                        "zh": product_item["handle"],
                        "cn": product_item["handle"]
                    },
                    "long_description": {
                        "en": product_item["body_html"],
                        "zh": product_item["body_html"],
                        "cn": product_item["body_html"]
                    },
                    "status": "ACTIVE",
                    "shopify_link": "",
                    "images": [item["src"] for item in product_item["images"]]
                },
                headers=create_headers(token)
            )

            # 更新产品变体
            for variant_item in product_item["variants"]:
                print(f"======update variant id {variant_item['id']}")
                
                # 通过shopify_id去查找需要更新的产品变体id
                get_one_variant = requests.get(
                    f"{base_url}/common/all/MProductVariant",
                    headers=create_headers(token),
                    params={
                        "shopify_product_variant_id": json.dumps({"$in": [str(variant_item["id"])]})
                    }
                ).json()

                # 拿到需要更新的产品变体id
                update_variant_id = get_one_variant["data"][0]["_id"]

                requests.put(
                    f"{base_url}/common/update/{update_variant_id}/MProductVariant",
                    json={
                        "title": {
                            "en": variant_item["title"],
                            "zh": variant_item["title"],
                            "cn": variant_item["title"]
                        },
                        "short_description": {
                            "en": product_item["handle"],
                            "zh": product_item["handle"],
                            "cn": product_item["handle"]
                        },
                        "long_description": {
                            "en": product_item["body_html"],
                            "zh": product_item["body_html"],
                            "cn": product_item["body_html"]
                        },
                        "price": float(variant_item["price"]*(1 + markup)),
                        "status": "ACTIVE",
                        "shopify_link": "",
                        "images": [variant_item.get("featured_image", {}).get("src")]
                    },
                    headers=create_headers(token)
                )

    # 3. 删除产品
    # 获取数据库的全部产品id
    all_product_id = requests.get(
        f"{base_url}/common/all/MProduct",
        headers=create_headers(token)
    ).json()

    # 获取数据库的全部产品id
    all_shopify_product_id_list = [
        {"id": item["shopify_product_id"], "_id": item["_id"]}
        for item in all_product_id["data"]
    ]

    # 获取shopify的全部产品id
    shopify_product_id_list = data

    # 获取需要删除的product
    difference = [
        obj1 for obj1 in all_shopify_product_id_list
        if not any(str(obj2["id"]) == obj1["id"] for obj2 in shopify_product_id_list)
    ]

    # 需要删除的产品id
    delete_product_id_list = [item["_id"] for item in difference]

    print("===delete_product_id_list", delete_product_id_list)

    # 删除不存在的产品
    if delete_product_id_list:
        # 删除产品
        requests.delete(
            f"{base_url}/common/delete/MProduct",
            headers=create_headers(token),
            json={"targetIds": delete_product_id_list}
        )
        
        # 获取需要删除的产品变体
        all_product_variant_id = requests.get(
            f"{base_url}/common/all/MProductVariant",
            headers=create_headers(token),
            params={
                "product_id": json.dumps({"$in": delete_product_id_list})
            }
        ).json()
        
        # 获取需要删除的产品变体id
        delete_product_variant_id_list = [item["_id"] for item in all_product_variant_id["data"]]
        print("===delete_product_variant_id_list", delete_product_variant_id_list)
        
        # 删除产品变体
        requests.delete(
            f"{base_url}/common/delete/MProductVariant",
            headers=create_headers(token),
            json={"targetIds": delete_product_variant_id_list}
        )

def insert_data_shopline(data,markup,token,base_url):
    """插入或更新数据"""
    for product_item in data:
        product_item_id = product_item["id"]
        print("----product_item_id", product_item_id)
        
        # 通过shopify的id去mongodb里面查询all的product
        all_product_data = requests.get(
            f"{base_url}/common/all/MProduct",
            headers=create_headers(token),
            params={
                "shopify_product_id": json.dumps({"$in": [str(product_item_id)]})
            }
        ).json()

        # 1. 插入新的产品
        if not all_product_data["data"]:
            print(f"===insert product id {product_item_id}")
            
            # 插入产品
            insert_product = requests.post(
                f"{base_url}/common/create/MProduct",
                json={
                    "shopify_product_id": str(product_item_id),
                    "title": {
                        "en": product_item["title"]["en"],
                        "zh": product_item["title"]["en"],
                        "cn": product_item["title"]["en"]
                    },
                    "short_description": {
                        "en": product_item["description"]["en"],
                        "zh": product_item["description"]["en"],
                        "cn": product_item["description"]["en"]
                    },
                    "long_description": {
                        "en": product_item["description"]["en"],
                        "zh": product_item["description"]["en"],
                        "cn": product_item["description"]["en"]
                    },
                    "status": "ACTIVE",
                    "shopify_link": "",
                    "images": [product_item["image_url"]]
                },
                headers=create_headers(token)
            ).json()

            # 插入的product_id
            insert_product_id = insert_product["data"]["_id"]

            # 插入产品变体
            for variant_item in product_item["variants"]:
                print(f"======insert variant id {variant_item['id']}")
                requests.post(
                    f"{base_url}/common/create/MProductVariant",
                    json={
                        "product_id": insert_product_id,
                        "shopify_product_variant_id": str(variant_item["id"]),
                        "title": {
                            "en": variant_item["title"]["en"],
                            "zh": variant_item["title"]["en"],
                            "cn": variant_item["title"]["en"]
                        },
                        "short_description": {
                            "en": product_item["description"]["en"],
                            "zh": product_item["description"]["en"],
                            "cn": product_item["description"]["en"]
                        },
                        "long_description": {
                            "en": product_item["description"]["en"],
                            "zh": product_item["description"]["en"],
                            "cn": product_item["description"]["en"]
                        },
                        "price": float(variant_item["price"]*(1 + markup)),
                        "status": "ACTIVE",
                        "shopify_link": "",
                        "images": [product_item["image_url"]]
                    },
                    headers=create_headers(token)
                )
        # 2. 更新产品
        else:
            print(f"===update product id {product_item_id}")
            
            # 通过shopify_id去查找需要更新的产品id
            get_one_product = requests.get(
                f"{base_url}/common/all/MProduct",
                headers=create_headers(token),
                params={
                    "shopify_product_id": json.dumps({"$in": [str(product_item_id)]})
                }
            ).json()

            # 拿到需要更新的产品id
            update_product_id = get_one_product["data"][0]["_id"]
            print("----update_product_id", update_product_id)

            # 更新产品
            requests.put(
                f"{base_url}/common/update/{update_product_id}/MProduct",
                json={
                    "title": {
                        "en": product_item["title"]["en"],
                        "zh": product_item["title"]["en"],
                        "cn": product_item["title"]["en"]
                    },
                    "short_description": {
                        "en": product_item["description"]["en"],
                        "zh": product_item["description"]["en"],
                        "cn": product_item["description"]["en"]
                    },
                    "long_description": {
                        "en": product_item["description"]["en"],
                        "zh": product_item["description"]["en"],
                        "cn": product_item["description"]["en"]
                    },
                    "status": "ACTIVE",
                    "shopify_link": "",
                    "images": [product_item["image_url"]]
                },
                headers=create_headers(token)
            )

            # 更新产品变体
            for variant_item in product_item["variants"]:
                print(f"======update variant id {variant_item['id']}")
                
                # 通过shopify_id去查找需要更新的产品变体id
                get_one_variant = requests.get(
                    f"{base_url}/common/all/MProductVariant",
                    headers=create_headers(token),
                    params={
                        "shopify_product_variant_id": json.dumps({"$in": [str(variant_item["id"])]})
                    }
                ).json()

                # 拿到需要更新的产品变体id
                update_variant_id = get_one_variant["data"][0]["_id"]

                requests.put(
                    f"{base_url}/common/update/{update_variant_id}/MProductVariant",
                    json={
                        "title": {
                            "en": variant_item["title"]["en"],
                            "zh": variant_item["title"]["en"],
                            "cn": variant_item["title"]["en"]
                        },
                        "short_description": {
                            "en": product_item["description"]["en"],
                            "zh": product_item["description"]["en"],
                            "cn": product_item["description"]["en"]
                        },
                        "long_description": {
                            "en": product_item["description"]["en"],
                            "zh": product_item["description"]["en"],
                            "cn": product_item["description"]["en"]
                        },
                        "price": float(variant_item["price"]*(1 + markup)),
                        "status": "ACTIVE",
                        "shopify_link": "",
                        "images": [product_item["image_url"]]
                    },
                    headers=create_headers(token)
                )

    # 3. 删除产品
    # 获取数据库的全部产品id
    all_product_id = requests.get(
        f"{base_url}/common/all/MProduct",
        headers=create_headers(token)
    ).json()

    # 获取数据库的全部产品id
    all_shopify_product_id_list = [
        {"id": item["shopify_product_id"], "_id": item["_id"]}
        for item in all_product_id["data"]
    ]

    # 获取shopify的全部产品id
    shopify_product_id_list = data

    # 获取需要删除的product
    difference = [
        obj1 for obj1 in all_shopify_product_id_list
        if not any(str(obj2["id"]) == obj1["id"] for obj2 in shopify_product_id_list)
    ]

    # 需要删除的产品id
    delete_product_id_list = [item["_id"] for item in difference]

    print("===delete_product_id_list", delete_product_id_list)

    # 删除不存在的产品
    if delete_product_id_list:
        # 删除产品
        requests.delete(
            f"{base_url}/common/delete/MProduct",
            headers=create_headers(token),
            json={"targetIds": delete_product_id_list}
        )
        
        # 获取需要删除的产品变体
        all_product_variant_id = requests.get(
            f"{base_url}/common/all/MProductVariant",
            headers=create_headers(token),
            params={
                "product_id": json.dumps({"$in": delete_product_id_list})
            }
        ).json()
        
        # 获取需要删除的产品变体id
        delete_product_variant_id_list = [item["_id"] for item in all_product_variant_id["data"]]
        print("===delete_product_variant_id_list", delete_product_variant_id_list)
        
        # 删除产品变体
        requests.delete(
            f"{base_url}/common/delete/MProductVariant",
            headers=create_headers(token),
            json={"targetIds": delete_product_variant_id_list}
        )


# 插入数据库 end

# 获取配置 start
def get_config():
    """获取配置信息"""
    config = requests.get(
        "http://localhost:5000/api/destinations",
        headers=create_headers()
    ).json()
    return config
# 获取配置 end

# 定时任务 start
def start_timer(interval):
    """开始定时器"""
    print(f"开始定时任务，每{interval}秒执行一次")

    asyncio.run(loop_execute_sources())


async def loop_execute_sources():
    """循环执行sources"""
    config = get_config()
    for source in config:
        token =  login(source["base_url"])
        for source_item in source["source_arr"]:
            print("----shopify_url", source_item["base_url"])
            print("----markup", source["markup"])
            print("----backend_url", source["base_url"])
            if source_item["type"] == "SHOPIFY":
                result = await fetch_and_transform_products_shopfiy(source_item["base_url"])
                insert_data_shopify(result,source["markup"],token,source["base_url"])
            elif source_item["type"] == "SHOPLINE":
                result = await fetch_and_transform_products_shopline(source_item["base_url"])
                insert_data_shopline(result,source["markup"],token,source["base_url"])

# 定时任务 end

def main():
    # interval = 10  # 每隔10秒获取一次数据
    # start_timer(interval)
    asyncio.run(loop_execute_sources())

    # token = login("http://127.0.0.1:3008/auth/login")
    # print("token",token)


# 执行并保存结果
if __name__ == "__main__":
    try:
        main()
        # result = fetch_and_transform_products()
        # print("result",result)
        # with open('transformed_products_with_variants.json', 'w', encoding='utf-8') as f:
        #     json.dump(result, f, ensure_ascii=False, indent=4)
        # print("转换完成，结果已保存到 transformed_products_with_variants.json")
        # print(f"共处理了 {len(result)} 个产品")
    except Exception as e:
        print(f"发生错误: {e}")