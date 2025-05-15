import requests
import json

def fetch_and_transform_products():
    # 获取原始数据
    print("111")
    url = "https://www.tentree.com/products.json"
    response = requests.get(url,verify=False)
    products_data = response.json().get('products', [])
    
    transformed_products = []
    print(len(products_data))
    for product in products_data:
        # 处理 tags 字段 - 确保是列表格式
        # tags = product.get('tags', [])
        # if isinstance(tags, str):  # 如果 tags 是字符串，按逗号分割
        #     tags = [tag.strip() for tag in tags.split(',')]
        
        # 处理 variants 变体信息
        variants = []
        for variant in product.get('variants', []):
            variants.append({
                "price": float(variant.get('price', 0)),
                "sku": variant.get('sku', ''),
                # 可以添加其他需要的变体字段，例如：
                "variant_id": variant.get('id'),
                "title":variant.get('title', ''),
                # "inventory_quantity": variant.get('inventory_quantity', 0)
            })
        
        # 构建转换后的产品数据
        transformed = {
            "_id":product.get('id',''),
            "title": {
                "cn": product.get('title', ''),
                "en": product.get('title', '')
            },
            "variants": variants,  # 包含所有变体的数组
            "image_url": product.get('images', [{}])[0].get('src', '') if product.get('images') else '',
            "description": {
                "cn": product.get('body_html', '').replace('<p>', '').replace('</p>', ''),
                "en": product.get('body_html', '').replace('<p>', '').replace('</p>', '')
            },
            "meta_keywords": product.get('tags', '') if product.get('tags') else [],
            "discount": 0  # 根据业务需求可以计算折扣
        }
        image=transformed['image_url']
        # 后缀
        extension = image.split('.')[-1][0:3]
        print("2222",extension)
        body = {
            "url": image,
            "extension": extension
        }
        res = requests.post("https://file.starsnet.com.hk/api/upload/bucket-by-url/development",
                            json=body)
        print("20002202020",res.status_code,body)
        if res.status_code == 500:
            
            transformed['image_url'] = 'https://starsnet-production.oss-cn-hongkong.aliyuncs.com/png/4fb86ec5-2b42-4824-8c05-0daa07644edf.png'
        elif res.status_code == 200:
            print('res.text',res.text)
            transformed['image_url'] = res.text
        print(transformed)
        transformed_products.append(transformed)
    
    return transformed_products

# 执行并保存结果
if __name__ == "__main__":
    try:
        result = fetch_and_transform_products()
        with open('transformed_products_with_variants.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        print("转换完成，结果已保存到 transformed_products_with_variants.json")
        print(f"共处理了 {len(result)} 个产品")
    except Exception as e:
        print(f"发生错误: {e}")