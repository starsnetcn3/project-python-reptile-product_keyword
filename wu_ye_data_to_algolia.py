import json
import os


def main():
    with open("wu_ye_json/merge/wu_ye_new.auction_lots.json", "r", encoding="utf-8") as f2:
        mergeData = json.load(f2)
    for property in mergeData:
        property['objectID'] = property['_id']['$oid']
    # 检查文件是否存在，存在则读取原有内容
    if os.path.exists("wu_ye_json/merge/wu_ye.auction_algolia_lots.json"):
        with open("wu_ye_json/merge/wu_ye.auction_algolia_lots.json", 'r', encoding='utf-8') as json_file:
            try:
                old_data = json.load(json_file)
            except Exception:
                old_data = []
    else:
        old_data = []
    # 追加新数据
    all_data = old_data + mergeData
    with open("wu_ye_json/merge/wu_ye.auction_algolia_lots.json", 'w', encoding='utf-8') as json_file:
        json.dump(all_data, json_file, ensure_ascii=False, indent=4)

    print("数据合并完成, 路径: wu_ye_json/merge/merge_detail.json")
    
    print("处理完成")
if __name__ == '__main__':
    main()