import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import sys
import os
import json
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.mongo_connection import MongoDB

# 连接到 MongoDB
mongo_db = MongoDB('mongodb://starsnet:password@192.168.3.19:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false', 'test_auction')

def clean_property_address(text):
    """
    清理物业地址文本，去除物业编号及其标识
    :param text: 包含物业地址和编号的原始文本
    :return: 清理后的纯地址文本
    """
    # 定义匹配物业编号的正则表达式模式（覆盖所有格式）
    patterns = [
        r'物業編號\s*[:：]?\s*[A-Z0-9]+',  # 匹配中文"物业编号"及各种符号
        r'\(物業編號:\s*\d+\)',          # 匹配括号内的编号
        r'物業編號﹕[A-Z0-9]+',           # 匹配全角冒号情况
        r'Property No\.?\s*[:：]?\s*\w+'  # 如果需要匹配英文格式
    ]
    
    # 逐个模式替换
    cleaned_text = text
    for pattern in patterns:
        cleaned_text = re.sub(pattern, '', cleaned_text, flags=re.IGNORECASE)
    
    # 清理多余空格和换行
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    
    # 处理可能残留的括号
    cleaned_text = cleaned_text.replace('()', '').replace('（）', '')
    
    return cleaned_text
def safe_insert_user(collection_name,filed,user_data):
        # 先查询是否已存在
        existing = mongo_db.find_one(
            collection_name,
            {filed: user_data[filed]}  # 按username查重
        )
        
        if existing:
            print(f"用户已存在，跳过插入")
            return False
        else:
            return True

def format_time_str_2(time_str):
    """
    处理格式: "2025/05/07 下午3:00-5:00"
    输出: "2025-05-07 PM 3:00-5:00"
    """
    # 分割日期和时间
    date_part, time_part = time_str.split()
    
    # 处理日期
    year, month, day = map(int, date_part.split('/'))
    
    # 处理时间
    period = "PM" if "下午" in time_part else "AM"
    time_range = time_part.replace("上午", "").replace("下午", "").strip()
    
    # 格式化输出
    return f"{year}-{month:02d}-{day:02d} {period} {time_range}"

def scrape_aa_property(url,bid):
    # 设置请求头，模拟浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # 发送HTTP请求
        response = requests.get(url, headers=headers)
        # response.raise_for_status()  # 检查请求是否成功
        
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        # print("soup",soup)
        select_element = soup.select_one('select#biddate')
        # 拿到了拍卖的时间之类的
        optionValue = select_element.find('option', {'value': bid})
        # print("soup",optionValue.text)
        # 使用正则表达式分离时间和地址


        table = soup.find_all('table')[4]
        # print("tanle",len(table))
        print("tanle",len(table.find_all('tr')))
         # 提取数据
        data=[]
        for row in table.find_all('tr')[7:-2]:  # 跳过表头
            cols = row.find_all('td')
            a_tag = cols[2].find('a')
            href = a_tag['href'] if a_tag else ''
            row_data = {
                    'image': '',
                    'serial_number': '',
                    'property_address': '',
                    'use': '',
                    'situation': '',
                    'area': '',
                    'price': '',
                    'viewing_time': '',
                    'contact_person': '',
                    'completion_year':'',
                    'a_link':'',
                    'google_link':'',
                }
            print ("cols",cols[2])
            row_data['image'] = 'https://www.aaproperty.com.hk/aa/'+ cols[0].find('img')['src'] if cols[0].find('img') else ''
            row_data['serial_number'] = cols[1].text
            row_data['property_address'] = cols[2].text
            row_data['use'] = cols[3].text
            row_data['situation'] = cols[4].text
            row_data['area'] = cols[5].text  # 没有匹配时设置为空
            row_data['price'] = cols[6].text
            row_data['viewing_time'] = cols[7].text
            row_data['contact_person'] = cols[8].text
            row_data['a_link'] = href
            data.append(row_data)
        # 创建一个字典来保存数据
        output_data = {
            "data": data,
            "optionValue": optionValue.text
        }

        # 将数据写入 JSON 文件
        with open('output.json', 'w', encoding='utf-8') as json_file:
            json.dump(output_data, json_file, ensure_ascii=False, indent=4)

        print("数据已写入 output.json")
    except Exception as e:
        print(f"抓取过程中发生错误: {e}")
        return None

def handle_data():
        # 读取 JSON 文件
        with open('output.json', 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)
        print("json_data['optionValue']",json_data['optionValue'])
        match = re.match(r'(.+?) \| (.+)', json_data['optionValue'])
        if match:
            time = format_time_str_2(match.group(1))
            address = match.group(2)
            company = '環亞物業拍賣有限公司(A A Property Auctioneers Limited)'
            print("Time:", time)
            print("Address:", address)
            # 插入数据
            data = {
                'time': time,
                'address':address,
                'company':company
            }
            print("data",data)
            flag = safe_insert_user('auction','time',data)
            print("flag11111",flag)
            inserted_id=""
            if flag:
                inserted_id = mongo_db.insert_data('auction', data)
                print("Inserted document ID:", inserted_id)
        else:
            print("No match found.")

        colums=json_data['data']
        for cols in colums:
                # 创建一个字典来存储每一行的数据
            row_data = {
                    'image': [],
                    'serial_number': '',
                    'property_address': '',
                    'use': '',
                    'situation': '',
                    'building_area': 0,
                    'saleable_area': 0,
                    'price': 0,
                    'viewing_time': '',
                    'contact_person': {},
                    'completion_year':'',
                    'property_number':'',
                    'created_at':datetime.now(),
                    'auction_id':inserted_id,
                    'detail_url':''
                }
            print("colums",cols)
            row_data['property_address'] = clean_property_address(cols.get('property_address').strip().replace('\n', '').replace('\t', '').replace('\r', ''))
            # 用property_address来判断数据库是不是有
            wuye_flag = safe_insert_user('auction_lots','property_address',row_data)
            print("wuye_flag",wuye_flag)
            if wuye_flag:
                row_data['serial_number'] = cols.get('serial_number').strip().replace('\n', '').replace('\t', '').replace('\r', '')
                row_data['use'] = cols.get('use').strip().replace('\n', '').replace('\t', '').replace('\r', '')
                row_data['situation'] = cols.get('situation').strip().replace('\n', '').replace('\t', '').replace('\r', '')
                # 去抓取详情页面
                detail_id= cols.get('a_link')
                detail_url =f'https://www.aaproperty.com.hk/aa/{detail_id}'
                # 存一个url用来前端跳转
                row_data['detail_url']=detail_url
                response = requests.get(detail_url)
                soup = BeautifulSoup(response.text, 'html.parser')
                # 找google_link
                item_no_match = re.search(r'item_no=(\d+)', detail_id)
                if item_no_match:
                    item_no = item_no_match.group(0)  # 获取匹配的字符串，格式为 item_no=20250725

                    # 找到所有包含 item_no 的 <a> 标签
                    target_links = soup.find('a', href=lambda href: href and item_no in href)
                    if target_links:
                        map_id = target_links.get('href')
                        map_url=f'https://www.aaproperty.com.hk/aa/{map_id}'     
                        response_map = requests.get(map_url)
                        soup_map = BeautifulSoup(response_map.text, 'html.parser')
                        iframes = soup_map.find('iframe')
                        row_data['google_link'] = iframes.get('src')
                    else:
                        row_data['google_link'] = ''
                        print("iframes",iframes)
                    print("target_links",target_links)
                # target_links = soup.find_all('a', href=lambda href: href and detail_id.replace in href)
                table = soup.find_all('table')
                img_all = table[5].find_all('img')
                images_without_title = [img for img in img_all if not img.has_attr('title')]
                # 拿到所有的图片之后开始遍历
                print ("soup22222222",images_without_title)
                if len(images_without_title):
                    for image in images_without_title[1:]:
                        extension = image['src'].split('.')[-1][0:3]
                        print("2222",extension)
                        imgage_url=' https://www.aaproperty.com.hk/aa/'+ image['src']
                        body = {
                            "url": imgage_url,
                            "extension": extension
                        }
                        res = requests.post("https://file.starsnet.com.hk/api/upload/bucket-by-url/development",
                                                    json=body)
                        print("20002202020",res.status_code)
                        if res.status_code == 200:
                            row_data['image'].append(res.text)
                            print("20002202020",row_data['image'])
                    # 假设每列的顺序是固定的
                # if cols.get('image'):
                #     image = cols.get('image')
                #     extension = image.split('.')[-1][0:3]
                #     print("2222",extension)
                #     body = {
                #         "url": image,
                #         "extension": extension
                #     }
                #     res = requests.post("https://file.starsnet.com.hk/api/upload/bucket-by-url/development",
                #                                 json=body)
                #     print("20002202020",res.status_code,body)
                #     if res.status_code == 500:
                #         row_data['image'] = ''
                #     elif res.status_code == 200:
                #         row_data['image'] = res.text


                # 处理面积字段
                area_text = cols.get('area').strip().replace('\n', '').replace('\t', '').replace('\r', '')
                print(area_text)

                # 提取建筑面积（包括可能的叠加情况）
                building_area_match = re.search(r'建築\(約\)\s*([\d+]+(?:\+\w+\d+)*)', area_text)

                # 提取实用面积（包括可能的叠加情况） - 修改后的正则表达式
                saleable_area_match = re.search(r'實用\(約\)\s*((?:\d+\+\w+\d+|\d+)(?:\+\w+\d+)*)', area_text)
                print("Matched saleable area:", saleable_area_match.group(1) if saleable_area_match else "No match")

                # 处理建筑面积
                if building_area_match:
                    # 提取所有数字并计算总和
                    building_numbers = re.findall(r'(\d+)', building_area_match.group(1))
                    print(f"Building Area numbers: {building_numbers}")
                    row_data['building_area'] = sum(int(num) for num in building_numbers)
                else:
                    row_data['building_area'] = 0  # 没有匹配时设置为 0

                # 处理实用面积
                if saleable_area_match:
                    # 提取所有数字并计算总和
                    saleable_numbers = re.findall(r'(\d+)', saleable_area_match.group(1))
                    print(f"Saleable Area numbers: {saleable_numbers}")
                    row_data['saleable_area'] = sum(int(num) for num in saleable_numbers)
                else:
                    row_data['saleable_area'] = 0  # 没有匹配时设置为 0

                price = cols.get('price').strip().replace('\n', '').replace('\t', '').replace('\r', '')
                # 提取数字
                price_match = re.search(r'(\d+)', price)
                # 将提取的数字转换为整数，如果没有找到，则默认为 0
                row_data['price'] = int(price_match.group(1)) * 10000 if price_match else 0
                row_data['viewing_time'] = cols.get('viewing_time').strip().replace('\n', '').replace('\t', '').replace('\r', '')
                contact_person = cols.get('contact_person').strip().replace('\n', '').replace('\t', '').replace('\r', '')
                # 正则表达式匹配姓名和电话
                matches =  re.findall(r'(\d{4}\s*\d{4}|\d{8})\s*([\u4e00-\u9fa5]+)', contact_person)
                print("matches",matches)
                print("matches",row_data)
                row_data['contact_person'] = [{"phone": phone.replace(" ", ""), "name": name} for phone, name in matches]

                row_data['completion_year'] = cols.get('completion_year').strip().replace('\n', '').replace('\t', '').replace('\r', '')
                # 提取物业编号
                property_number_match = re.search(r'物業編號:\s*(\d+)', row_data['property_address'])
                # 如果找到，提取数字；否则默认为 ''
                print("property_match",property_number_match)
                row_data['property_number'] = property_number_match.group(1) if property_number_match else ''

                
                print("row_data",row_data)
                product_id = mongo_db.insert_data('auction_lots', row_data)
                print("Product document ID:", product_id)

if __name__ == "__main__":
    # print("mongoDB",mongo_db)
    reesponse_data = requests.get("https://www.aaproperty.com.hk/aa/bid_list.php")
    soup = BeautifulSoup(reesponse_data.text, 'html.parser')
        # print("soup",soup)
    select_element = soup.select_one('select#biddate')
    # 提取所有 option 的 value
    values = [option['value'] for option in select_element.find_all('option') if option.get('value', '').strip() != '']

    # 输出结果
    print(values)
    for bid in values:
        url = f'https://www.aaproperty.com.hk/aa/bid_list.php?bid={bid}'
        # bid=bid
        auction_data = scrape_aa_property(url,bid)
        handle_data()
