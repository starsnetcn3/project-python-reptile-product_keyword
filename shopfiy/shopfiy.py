import requests
import json
import time
from functools import wraps

# 重试装饰器
def retry(max_retries=3, delay=1, exceptions=(Exception,)):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    retries += 1
                    if retries == max_retries:
                        raise
                    time.sleep(delay)
                    print(f"Retry {retries}/{max_retries} for {func.__name__} due to: {str(e)}")
        return wrapper
    return decorator

# 带重试的请求函数
@retry(max_retries=3, delay=2, exceptions=(requests.exceptions.RequestException,))
def fetch_with_retry(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # 如果状态码不是200，会抛出HTTPError
    return response

@retry(max_retries=3, delay=2, exceptions=(requests.exceptions.RequestException,))
def upload_with_retry(url, json_data):
    response = requests.post(url, json=json_data, timeout=10)
    response.raise_for_status()
    return response

def fetch_and_transform_products():
    try:
        # 获取原始数据（带重试）
        url = "https://www.tentree.com/products.json"
        response = fetch_with_retry(url)
        products_data = response.json().get('products', [])
        
        transformed_products = []
        print("111",len(products_data))
        for product in products_data:  # 测试时只处理第一个产品
            # 处理variants变体信息
            variants = []
            for variant in product.get('variants', []):
                variants.append({
                    "price": float(variant.get('price', 0)),
                    "sku": variant.get('sku', ''),
                    "variant_id": variant.get('id'),
                })
            
            # 构建转换后的产品数据
            transformed = {
                "title": {
                    "cn": product.get('title', ''),
                    "en": product.get('title', '')
                },
                "variants": variants,
                "image_url": product.get('images', [{}])[0].get('src', '') if product.get('images') else '',
                "description": {
                    "cn": product.get('body_html', '').replace('<p>', '').replace('</p>', ''),
                    "en": product.get('body_html', '').replace('<p>', '').replace('</p>', '')
                },
                "meta_keywords": product.get('tags', '') if product.get('tags') else [],
                "discount": 0
            }
            
            # 图片上传（带重试）
            image = transformed['image_url']
            if image:  # 只有有图片链接时才尝试上传
                extension = image.split('.')[-1][0:3]
                body = {
                    "url": image,
                    "extension": extension
                }
                try:
                    res = upload_with_retry(
                        "https://file.starsnet.com.hk/api/upload/bucket-by-url/development",
                        body
                    )
                    if res.status_code == 200:
                        transformed['image_url'] = res.text
                    else:
                        transformed['image_url'] = 'https://starsnet-production.oss-cn-hongkong.aliyuncs.com/png/4fb86ec5-2b42-4824-8c05-0daa07644edf.png'
                except requests.exceptions.RequestException as e:
                    print(f"图片上传失败，使用默认图片: {str(e)}")
                    transformed['image_url'] = 'https://starsnet-production.oss-cn-hongkong.aliyuncs.com/png/4fb86ec5-2b42-4824-8c05-0daa07644edf.png'
            
            transformed_products.append(transformed)
        
        return transformed_products
    
    except Exception as e:
        print(f"处理产品数据时发生错误: {str(e)}")
        return []

if __name__ == "__main__":
    try:
        result = fetch_and_transform_products()
        with open('transformed_products_with_variants.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        print("转换完成，结果已保存到 transformed_products_with_variants.json")
        print(f"共处理了 {len(result)} 个产品")
    except Exception as e:
        print(f"主程序发生错误: {e}")