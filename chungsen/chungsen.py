# import requests
from curl_cffi import requests
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
def format_time_str(time_str):
    """
    处理格式: "11/6/2025 (星期三) 下午3時正"
    输出: "2025-06-11 PM 3:00"
    """
    # 提取日期和时间部分
    date_part = re.search(r'(\d+/\d+/\d+)', time_str).group(1)
    period = "PM" if "下午" in time_str else "AM"
    time_part = re.search(r'[\d]+', time_str.split()[-1]).group()
    
    # 解析日期 - 修正顺序为 日/月/年
    day, month, year = map(int, date_part.split('/'))
    
    # 格式化输出
    return f"{year}-{month:02d}-{day:02d} {period} {time_part}:00"
def scrape_aa_property(url,cid):
    # 设置请求头，模拟浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }
    
    try:
        # 发送HTTP请求
        response = requests.get(url, impersonate="chrome110")  # 模拟Chrome的SSL行为
        # response.raise_for_status()  # 检查请求是否成功
        
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # select_element = soup.select_one('select.form-select')
        # 拿到了拍卖的时间之类的
        # print("soup",select_element)
        # optionValue = select_element.find('option', {'value': cid})
        # print("soup",optionValue.text)
        auction_sub_title = soup.find('div', class_='auction_sub_title')
        if auction_sub_title:
            # paragraphs = auction_sub_title.find('p')
            print(auction_sub_title.text)
        else:
            print("No div with class 'auction_info' found.")

        table = soup.find('table', class_='tb_auction')
        print("tanle",table)
        print("tanle",len(table.find_all('tr')))
        #  # 提取数据
        data=[]
        for row in table.find_all('tr')[1:]:  # 跳过表头
            cols = row.find_all('td')
            a_tag = cols[1].find('a')
            href = a_tag['href'] if a_tag else ''

            row_data = {
                    'image': '',
                    'serial_number': '',
                    'property_address': '',
                    'use': '',
                    'situation': '',
                    'price': '',
                    'viewing_time': '',
                    'contact_person': '',
                    'completion_year':'',
                    'building_area': '',
                    'saleable_area': '',
                    'a_link':'',
                    'google_link':'',
                }
            row_data['serial_number'] = cols[0].text
            row_data['property_address'] = cols[1].text
            row_data['use'] = cols[2].text
            row_data['building_area'] = cols[3].text  # 没有匹配时设置为空
            row_data['saleable_area'] = cols[4].text  # 没有匹配时设置为空
            row_data['price'] = cols[5].text
            row_data['viewing_time'] = cols[6].text
            row_data['contact_person'] = cols[7].text
            row_data['a_link'] = href
            data.append(row_data)
        # 创建一个字典来保存数据
        output_data = {
            "data": data,
            # "optionValue": optionValue.text
              "paragraphs": auction_sub_title.text
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
        print("json_data['optionValue']",json_data['paragraphs'])
        time_match = re.search(r'(\d{1,2}/\d{1,2}/\d{4} \(星期\w+\) 下午\d{1,2}時正)', json_data['paragraphs'])
        address_match = re.search(r'(香港.+?室)', json_data['paragraphs'])

        if time_match:
            time = format_time_str(time_match.group(1))
        else:
            time = ''

        if address_match:
            address = address_match.group(1).strip()
        else:
            address = ''

        print("时间:", time)
        print("地址:", address)
        company="忠誠集團"
        data = {
                'time': time,
                'address':address,
                'company':company
        }
        print("data",data)
        flag = safe_insert_user('auction','time',data)
        print("flag11111",flag)
        inserted_id=''
        if flag:
             inserted_id = mongo_db.insert_data('auction', data)
             print("Inserted document ID:", inserted_id)
        colums=json_data['data']
        for cols in colums:
                # 创建一个字典来存储每一行的数据
            row_data = {
                    'image': [],
                    'serial_number': '',
                    'property_address': '',
                    'use': '',
                    'situation': '',
                    'price': 0,
                    'viewing_time': '',
                    'contact_person': {},
                    'completion_year':'',
                    'building_area': 0,
                    'saleable_area': 0,
                    'property_number':'',
                    'created_at':datetime.now(),
                    'google_link':'',
                    'auction_id':inserted_id,
                    'detail_url':''
                }
            print("colums",cols)
            row_data['property_address'] = clean_property_address(cols.get('property_address').strip().replace('\n', '').replace('\t', '').replace('\r', ''))
            wuye_flag = safe_insert_user('auction_lots','property_address',row_data)
            print("wuye_flag",wuye_flag)
            if wuye_flag:
                row_data['serial_number'] = cols.get('serial_number').strip().replace('\n', '').replace('\t', '').replace('\r', '')
                row_data['use'] = cols.get('use').strip().replace('\n', '').replace('\t', '').replace('\r', '')
                row_data['situation'] = cols.get('situation').strip().replace('\n', '').replace('\t', '').replace('\r', '')
                # 去抓取详情页面
                detail_id= cols.get('a_link')
                detail_url =f'https://www.chungsen.com.hk/tc/{detail_id}'
                row_data['detail_url'] = detail_url
                response = requests.get(detail_url)
                soup = BeautifulSoup(response.text, 'html.parser')
                iframes = soup.find('iframe')
                if iframes.get('src'):
                    row_data['google_link']=iframes.get('src')

                print("iframes",iframes)
                div_img = soup.select('.product-galleryslider a')
                print("222222222",div_img)
                # 提取所有 src 属性
                img_srcs = [img['href'].replace("../", "", 1) for img in div_img if img.get('href').replace("../", "", 1)]
                for image in img_srcs[1:]:
                    print ("halloxion",image)
                    extension = image.split('.')[-1][0:3]
                    if extension == 'jpe':
                        extension = 'jpg'
                    print("2222",extension)
                    imgage_url='https://www.chungsen.com.hk/'+ image
                    print ("222222222",imgage_url)
                    body = {
                        "url": imgage_url,
                        "extension": extension
                    }
                    res = requests.post("https://file.starsnet.com.hk/api/upload/bucket-by-url/development",
                                                json=body)
                    print("20002202020",res.text)
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

                # 面积的处理
                building_area = cols.get('building_area').strip().replace('\n', '').replace('\t', '').replace('\r', '')
                saleable_area = cols.get('saleable_area').strip().replace('\n', '').replace('\t', '').replace('\r', '')
                # 正则表达式匹配数字
                building_numbers = re.findall(r'(\d+)', building_area)
                saleable_numbers = re.findall(r'(\d+)', saleable_area)
                # 将提取的数字转换为整数并计算总和
                row_data['building_area'] = sum(int(num) for num in building_numbers)
                row_data['saleable_area'] = sum(int(num) for num in saleable_numbers)
                price = cols.get('price').strip().replace('\n', '').replace('\t', '').replace('\r', '')
                # 提取数字
                price_matches = re.findall(r'(\d+)', price)
                # 将提取的数字转换为整数，如果没有找到，则默认为 0
                prices = [int(price) for price in price_matches]
                row_data['price'] = sum(prices) * 10000 if prices else 0

                row_data['viewing_time'] = cols.get('viewing_time').strip().replace('\n', '').replace('\t', '').replace('\r', '')
                contact_person = cols.get('contact_person').strip().replace('\n', '').replace('\t', '').replace('\r', '')
                # 正则表达式匹配姓名和电话
                matches =  re.findall(r'(\d{4}\s*\d{4}|\d{8})\s*([\u4e00-\u9fa5]+)', contact_person)
                print("matches",matches)
                row_data['contact_person'] = [{"phone": phone.replace(" ", ""), "name": name} for phone, name in matches]

                row_data['completion_year'] = cols.get('completion_year').strip().replace('\n', '').replace('\t', '').replace('\r', '')
                # 正则表达式匹配物业编号中的数字
                property_match = re.search(r'(\d+)$', row_data['property_address'])
                # 如果找到，提取数字；否则默认为 ''
                print("property_match",property_match)
                row_data['property_number'] = property_match.group(1) if property_match else ''
                print("row_data",row_data)
                product_id = mongo_db.insert_data('auction_lots', row_data)
                print("Product document ID:", product_id)

if __name__ == "__main__":
    # print("mongoDB",mongo_db)
    reesponse_data = requests.get("https://www.chungsen.com.hk/tc/auction.php?&wid=82&cid=651")
    soup = BeautifulSoup(reesponse_data.text, 'html.parser')
    select_element = soup.find('select',class_='form-select')
    print("soup",select_element)

        # 提取所有 option 的 value
    values = [option['value'] for option in select_element.find_all('option') if option.get('value', '').strip() != '']

    # 输出结果
    print(values)
    for cid in values:
        url = f'https://www.chungsen.com.hk/tc/auction.php?&wid=82&cid={cid}'
        # 暂且先写死
        # cid= cid
        auction_data = scrape_aa_property(url,cid)
        handle_data()
