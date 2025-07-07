import json
import os

import requests
from opencc import OpenCC

# 繁中 转 简中
cc = OpenCC('t2s')

def getAddressDistrict(mergeData):
    url = "https://geodata.gov.hk/gs/api/v1.0.0/locationSearch?q="
    for property in mergeData:
        # 假设 property 是一个字典，包含 'property_address' 键
        address = property.get('property_address', '')
        if address:
            full_url = url + address
            print("拼接的 URL:", full_url)
            response = requests.get(full_url)
            if response.status_code == 200:
                if len(response.json()):
                    district = {"en": response.json()[0]['districtEN'], "zh": response.json()[0]['districtZH'] , "cn": cc.convert( response.json()[0]['districtZH']) }
                else:
                    district = {"en": "", "zh": "", "cn": ""  }
                print(district)
                property["district"] = district 
            else:
                property["district"] = {"en": "", "zh": "", "cn": ""}
    json_filename = 'wu_ye_json/test_auction_auction_lots_lang.json'
    # 检查文件是否存在，存在则读取原有内容
    if os.path.exists(json_filename):
        with open(json_filename, 'r', encoding='utf-8') as json_file:
            try:
                old_data = json.load(json_file)
            except Exception:
                old_data = []
    else:
        old_data = []
    # 追加新数据
    all_data = old_data + mergeData
    with open(json_filename, 'w', encoding='utf-8') as json_file:
        json.dump(all_data, json_file, ensure_ascii=False, indent=4)

    print("数据合并完成, 路径: wu_ye_json/test_auction_auction_lots_lang.json")

def main():
    with open("wu_ye_json/test_auction_auction_lots.json", "r", encoding="utf-8") as f1:
        data = json.load(f1)
    getAddressDistrict(data)


if __name__ == '__main__':
    main()