import json
import os
import requests
from opencc import OpenCC

# 繁中 转 简中
cc = OpenCC('t2s')

def merge_zh_en_data(zh_list, en_list):
    """
    合并中英文数据的通用函数
    :param zh_list: 中文数据列表
    :param en_list: 英文数据列表
    :return: 合并后的数据列表
    """
    mergeData = []
    for idx in range(len(zh_list)):
        zh = zh_list[idx]
        en = en_list[idx] if idx < len(en_list) else {}
        zh_contacts = zh.get("contact_person", [])
        en_contacts = en.get("contact_person", [])
        contact_person = []
        for i in range(len(zh_contacts)):
            zh_contact = zh_contacts[i]
            en_contact = en_contacts[i] if i < len(en_contacts) else {}
            contact = {}
            # name 字段合并为字典
            contact["name"] = {
                "zh": zh_contact.get("name", ""),
                "en": en_contact.get("name", "") if en_contact.get("name", "") else zh_contact.get("name", "")
            }
            # 其它字段直接保留
            for k, v in zh_contact.items():
                if k != "name":
                    contact[k] = v
            contact_person.append(contact)
        def fill_en(zh_val, en_val):
            return en_val if en_val else zh_val
        item = {
            "property_address": {"zh": zh.get("property_address", ""), "en": fill_en(zh.get("property_address", ""), en.get("property_address", ""))},
            "use": {"zh": zh.get("use", ""), "en": fill_en(zh.get("use", ""), en.get("use", ""))},
            "situation": {"zh": zh.get("situation", ""), "en": fill_en(zh.get("situation", ""), en.get("situation", ""))},
            "viewing_time": {"zh": zh.get("viewing_time", ""), "en": fill_en(zh.get("viewing_time", ""), en.get("viewing_time", ""))},
            "contact_person": contact_person
        }
        for k, v in zh.items():
            if k not in ["property_address", "use", "situation", "viewing_time", "contact_person"]:
                item[k] = v
        mergeData.append(item)
    return mergeData

def merge(type):
    if type == "aaproperty":
        # 执行aaproperty相关的操作
        print("Executing aaproperty merge operation")
        with open("wu_ye_json/aaproperty_detail.json", "r", encoding="utf-8") as f1:
            tc_aaproperty_detail = json.load(f1)
        with open("wu_ye_json/aaproperty_detail.json", "r", encoding="utf-8") as f2:
            sc_aaproperty_detail = json.load(f2)
        mergeData = merge_zh_en_data(tc_aaproperty_detail, sc_aaproperty_detail)
        getAddressDistrict(mergeData=mergeData)

    elif type == "chungsen":
        # 执行chungsen相关的操作
        print("Executing chungsen merge operation")
        with open("wu_ye_json/tc_chungsen_detail.json", "r", encoding="utf-8") as f1:
            tc_chungsen_detail = json.load(f1)
        with open("wu_ye_json/en_chungsen_detail.json", "r", encoding="utf-8") as f2:
            sc_chungsen_detail = json.load(f2)
        mergeData = merge_zh_en_data(tc_chungsen_detail, sc_chungsen_detail)
        getAddressDistrict(mergeData=mergeData)

    elif type == "mwal":
        # 执行mwal相关的操作
        with open("wu_ye_json/tc_mwal_detail.json", "r", encoding="utf-8") as f1:
            tc_mwal_detail_data = json.load(f1)
        with open("wu_ye_json/sc_mwal_detail.json", "r", encoding="utf-8") as f2:
            sc_mwal_detail_data = json.load(f2)
        mergeData = merge_zh_en_data(tc_mwal_detail_data, sc_mwal_detail_data)
        getAddressDistrict(mergeData=mergeData)
    else:
        print(f"Unknown type: {type}")

def getAddressDistrict(mergeData):
    url = "https://geodata.gov.hk/gs/api/v1.0.0/locationSearch?q="
    for property in mergeData:
        # 假设 property 是一个字典，包含 'property_address' 键
        address = property.get('property_address', {}).get('zh')
        if address:
            full_url = url + address
            print("拼接的 URL:", full_url)
            response = requests.get(full_url)
            if response.status_code == 200:
                if len(response.json()):
                    district = {"en": response.json()[0]['districtEN'], "zh": response.json()[0]['districtZH']  }
                else:
                    district = {"en": "", "zh": "", "cn": ""  }
                print(district)
                property["district"] = district 
            else:
                property["district"] = {"en": "", "zh": ""}
    addCnLang(mergeData)

def addCnLang(mergeData):
    for property in mergeData:
        property['property_address']['cn'] = cc.convert(property['property_address']['zh'])
        property['use']['cn'] = cc.convert(property['use']['zh'])
        property['viewing_time']['cn'] = cc.convert(property['viewing_time']['zh'])
        property['viewing_time']['cn'] = cc.convert(property['viewing_time']['zh'])
        property['situation']['cn'] = cc.convert(property['situation']['zh'])
        # property['district']['cn'] = cc.convert(property['district']['zh'])
        for contact in property['contact_person']:
            contact['name']['cn'] = contact['name']['zh']
    
    json_filename = 'wu_ye_json/merge/merge_detail.json'
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

    print("数据合并完成, 路径: wu_ye_json/merge/merge_detail.json")

def main():
    merge("mwal")
    merge("chungsen")
    merge("aaproperty")

    # with open("wu_ye_json/merge/merge_detail_backup.json", "r", encoding="utf-8") as f2:
    #     mergeData = json.load(f2)
    # addCnLang(mergeData=mergeData)

if __name__ == '__main__':
    main()