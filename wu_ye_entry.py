import json
import time
from aaproperty import aaproperty_lang
from mwal import mwal_lang
from chungsen import chungsen_lang
import wu_ye_data_merge_and_insert_new as merge_insert
import wu_ye_data_to_algolia as to_algolia
import requests
import concurrent.futures
import os
from dotenv import load_dotenv
from algoliasearch.search.client import SearchClientSync

load_dotenv()

COMMON_URL = os.getenv("COMMON_URL")

INDEX_NAME = os.getenv("INDEX_NAME")


def clear_non_directory_files(folder_path):
    # 遍历文件夹中的所有文件和子文件夹
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        # 检查是否为文件且不是文件夹
        if os.path.isfile(item_path):
            os.remove(item_path)  # 删除文件
            print(f"已删除文件: {item_path}")


def safe_execute(func, retries=3):
    for i in range(retries):
        try:
            return func()
        except Exception as e:
            print(f"尝试 {i + 1} 失败: {e}")
            if i < retries - 1:
                time.sleep(1)  # 等待一段时间后重试
            else:
                raise


def main():
    client = SearchClientSync(
        os.getenv("ALGOLIA_APPLICATION_ID"), os.getenv("ALGOLIA_API_KEY")
    )
    # aaproperty_lang.main()
    # mwal_lang.main()
    # chungsen_lang.main()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 提交任务
        futures = [
            executor.submit(safe_execute, aaproperty_lang.main),
            executor.submit(safe_execute, mwal_lang.main),
            executor.submit(safe_execute, chungsen_lang.main),
        ]

        # 等待所有任务完成
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()  # 获取结果，抛出异常（如果有的话）
            except Exception as e:
                print(f"任务失败: {e}")

    print("所有数据处理完成")

    merge_insert.main()
    print("所有数据已处理完成，请手动完成将数据上传到mogodb")
    print("json在wu_ye_json/merge/merge_detail_new.json")

    # 上传数据到MongoDB
    json_file_path = "wu_ye_json/merge/merge_detail_new.json"
    with open(json_file_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    try:
        response = requests.post(
            f"{COMMON_URL}/common/createMany/MAuctionLots", json=data
        )
        response.raise_for_status()  # 如果响应状态码不是 200，将引发 HTTPError
        print("数据上传成功:", response.json())

        lotsResponse = requests.get(f"{COMMON_URL}/common/all/MAuctionLots")
        lots = lotsResponse.json().get("data", [])
        lotsResponse.raise_for_status()  # 如果响应状态码不是 200，将引发 HTTPError

        # 指定文件路径
        file_path = "wu_ye_json/merge/auction_lots.json"

        # 将数据写入 JSON 文件
        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(lots, json_file, ensure_ascii=False, indent=4)

        print(f"数据已成功写入 {file_path}")

        to_algolia.main()

        # 将数据写入 Algolia
        json_file_path = "wu_ye_json/merge/wu_ye.auction_algolia_lots.json"
        algolia_data = []

        with open(json_file_path, "r", encoding="utf-8") as json_file:
            algolia_data = json.load(json_file)

        save_resp = client.save_objects(
            index_name=INDEX_NAME,
            objects=algolia_data,
        )
        print(save_resp[0].task_id)
        task_id = save_resp[0].task_id
        client.wait_for_task(index_name=INDEX_NAME, task_id=task_id)

        clear_non_directory_files("./wu_ye_json")
        clear_non_directory_files("./wu_ye_json/merge")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP 错误发生: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"请求错误发生: {req_err}")
    except Exception as e:
        print(f"发生错误: {e}")


if __name__ == "__main__":
    main()
    print(
        # "爬虫完成，最后请将 wu_ye_json/merge/wu_ye.auction_algolia_lots.json 手动上传到Algolia, 即完成所有操作"
        "爬虫完成，最后请分别到数据库和Algolia查看数据"
    )
