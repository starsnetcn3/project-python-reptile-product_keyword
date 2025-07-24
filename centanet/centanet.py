from collections import defaultdict
import glob
import json
import random
import threading
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
import ssl
import math
from concurrent.futures import ThreadPoolExecutor
import os
import asyncio
import aiohttp
from collections import defaultdict
from requests.adapters import HTTPAdapter


class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        context.set_ciphers("DEFAULT@SECLEVEL=1")  # 降低安全级别以兼容老旧服务器
        context.options |= 0x4  # 启用OP_LEGACY_SERVER_CONNECT
        kwargs["ssl_context"] = context
        return super().init_poolmanager(*args, **kwargs)


session = requests.Session()
session.mount("https://hk.centanet.com", TLSAdapter())
# 屋苑列表API
searchListUrl = "https://hk.centanet.com/estate/api/Estate/Search"
housingEstatePath = "./centanet/json/housingEstateList.json"
langs = ["en-US", "zh-TW", "zh-CN"]
CREATE_DB_URL = "http://localhost:3011/common/createMany/MEstate"
# ip_pool = [
#     "47.99.112.148:8060",
#     "39.102.213.187:8443",
#     "47.122.65.3247.122.65.32:80",
#     "47.92.194.235:8080",
# ]


# 请求屋苑列表API
def requestHouseIngEstateListAPI(params):
    try:
        start = time.time()
        # thread_id = threading.get_ident()
        # print(f"[线程{thread_id}] 开始请求 {params['offset']}")

        response = session.post(
            searchListUrl,
            json=params,
        )
        # 尝试解析 JSON 响应
        response_data = response.json()

        # print(
        #     f"[线程{thread_id}] 完成请求 {params['offset']}, 耗时: {time.time()-start:.2f}s"
        # )
        print(f"[完成请求 {params['offset']}, 耗时: {time.time()-start:.2f}s")
        return response_data["data"]
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
    except ValueError as e:
        print(f"解析 JSON 时出错: {e}")
    except Exception as e:
        print(f"发生错误: {e}")


# 整理API返回的数据 存入到JSON中
def getHousingEstateList():
    typeCodes = ["4-HK", "4-KL", "4-NE", "4-NW"]
    # 最终需要放到json文件的
    housingEstateJson = []
    total = 0
    params = {
        "typeCodes": [],
        "includeEstateTypes": ["Bigest", "Normal", "Single"],
        "offset": 0,
        "size": 1,  # 通过一条数据 来先获取 总数
    }
    try:
        for code in typeCodes:
            params["typeCodes"] = [code]
            print(f"正在请求屋苑列表: {code}")
            # 请求一次API 获取总数
            response = session.post(
                searchListUrl,
                json=params,
            )
            response_data = response.json()
            total = response_data["count"]
            print("总数量: ", total)
            # 需要请求的数量
            requestNumber = math.ceil(total / 100)
            print("请求数量:", requestNumber)
            params["size"] = 100
            # # 线程池 - 有问题 写的太简单了可能, 数据会混乱
            # concurrent_requests = 6
            # with ThreadPoolExecutor(max_workers=concurrent_requests) as executor:
            #     futures = []
            #     for i in range(requestNumber):
            #         params["offset"] = i
            #         # 提交请求并添加到 futures 列表
            #         futures.append(
            #             executor.submit(requestHouseIngEstateListAPI, params.copy())
            #         )

            #     for future in futures:
            #         result = future.result()
            #         if result:
            #             # 线程池返回的结果
            #             housingEstateJson.extend(result)
            for i in range(requestNumber):
                params["offset"] = i * 100
                print(f"正在请求屋苑列表: {code}, 偏移量: {params['offset']}")
                # 请求屋苑列表API
                time.sleep(0.5)
                result = requestHouseIngEstateListAPI(params)
                housingEstateJson.extend(result)

        os.makedirs(os.path.dirname(housingEstatePath), exist_ok=True)
        with open(housingEstatePath, "w", encoding="utf-8") as json_file:
            json.dump(housingEstateJson, json_file, ensure_ascii=False, indent=4)
            print(f"屋苑列表获取完成：保存到: {housingEstatePath}")
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
    except ValueError as e:
        print(f"解析 JSON 时出错: {e}")
    except Exception as e:
        print(f"发生错误: {e}")


# 爬取detail - 同步
def getHousingEstateDetail():

    # https://hk.centanet.com/estate/api/Estate/GetEstateDetail?typeCode=2-BEPPWPPASK&datasize=full
    with open(housingEstatePath, "r", encoding="utf-8") as file:
        data = json.load(file)
    print(len(data))
    # # 只取第一个屋苑的 typeCode 测试
    # typeCodes = [item["typeCode"] for item in data[:2]]
    # typeCodes = [item["typeCode"] for item in data[4353:]]
    typeCodes = [item["typeCode"] for item in data]
    detailJson = defaultdict(lambda: defaultdict(dict))
    for index, code in enumerate(typeCodes):
        for lang in langs:
            headers = {"lang": lang}
            print(f"正在请求屋苑详情: {code}, 语言: {lang}")
            try:
                response = session.get(
                    f"https://hk.centanet.com/estate/api/Estate/GetEstateDetail?typeCode={code}&datasize=full",
                    headers=headers,
                )
                response_data = response.json()
                # detailJson[code][lang] = response_data
                detailJson[lang] = response_data
                randomSleepTime = random.uniform(0, 1)
                print(f"暂停: {randomSleepTime}秒")
                time.sleep(randomSleepTime)
            except requests.exceptions.RequestException as e:
                print(f"请求错误: {e}")
            except ValueError as e:
                print(f"解析 JSON 时出错: {e}")
            except Exception as e:
                print(f"发生错误: {e}")

        estateDetailPath = f"./centanet/json/detail/{code}.json"
        os.makedirs(os.path.dirname(estateDetailPath), exist_ok=True)
        with open(estateDetailPath, "w", encoding="utf-8") as json_file:
            json.dump(detailJson, json_file, ensure_ascii=False, indent=4)
            print(f"屋苑详情获取完成：保存到: {estateDetailPath}")


# 异步 START
async def fetchEstateDetail(session, code, lang):
    headers = {"lang": lang}
    print(f"正在请求屋苑详情: {code}, 语言: {lang}")
    try:
        async with session.get(
            f"https://hk.centanet.com/estate/api/Estate/GetEstateDetail?typeCode={code}&datasize=full",
            headers=headers,
        ) as response:
            response_data = await response.json()
            return code, lang, response_data
    except Exception as e:
        print(f"请求错误: {e}, {code}")
        return code, lang, None


async def getHousingEstateDetailAsync():
    with open(housingEstatePath, "r", encoding="utf-8") as file:
        data = json.load(file)

    print(len(data))
    typeCodes = [item["typeCode"] for item in data[16975:]]
    detailJson = defaultdict(lambda: defaultdict(dict))

    # 创建自定义 SSL 上下文
    ssl_context = ssl.create_default_context()
    ssl_context.set_ciphers("DEFAULT@SECLEVEL=1")
    ssl_context.options |= 0x4
    connector = aiohttp.TCPConnector(ssl=ssl_context)

    async with aiohttp.ClientSession(connector=connector) as session:
        for i in range(0, len(typeCodes), 3):
            tasks = []
            error_codes = []  # 每组请求后重置错误代码列表

            for j in range(i, min(i + 3, len(typeCodes))):
                code = typeCodes[j]
                for lang in langs:
                    tasks.append(fetchEstateDetail(session, code, lang))

            # 执行当前组的所有请求
            results = await asyncio.gather(*tasks)

            for code, lang, response_data in results:
                if response_data is not None:
                    # 检查是否有错误信息
                    if (
                        "error" in response_data
                        and response_data["error"] == "API calls quota exceeded!"
                    ):
                        error_codes.append(code)  # 存储错误代码
                    else:
                        detailJson[code][lang] = response_data
                        estateDetailPath = f"./centanet/json/detail-3/{code}.json"
                        os.makedirs(os.path.dirname(estateDetailPath), exist_ok=True)
                        with open(estateDetailPath, "w", encoding="utf-8") as json_file:
                            json.dump(
                                detailJson[code],
                                json_file,
                                ensure_ascii=False,
                                indent=4,
                            )
                            print(f"屋苑详情获取完成：保存到: {estateDetailPath}")

            # 每组请求后保存错误代码到文件
            if error_codes:
                error_path = "./centanet/json/error"
                os.makedirs(error_path, exist_ok=True)
                error_file_path = os.path.join(error_path, "code.json")
                with open(error_file_path, "w", encoding="utf-8") as error_file:
                    json.dump(error_codes, error_file, ensure_ascii=False, indent=4)
                    print(f"错误代码已保存到: {error_file_path}")

            # 每组请求后暂停 2 秒
            await asyncio.sleep(2)


def appendToJson(filePath, newData):
    # 初始化数据
    data = []

    # 尝试读取现有的数据
    if os.path.exists(filePath):
        try:
            with open(filePath, "r", encoding="utf-8") as jsonFile:
                # 读取并解析 JSON 数据
                data = json.load(jsonFile)
        except (json.JSONDecodeError, ValueError) as e:
            print(f"解析 JSON 时出错: {e}. 将初始化为空列表。")
            data = []  # 如果解析失败，初始化为空列表

    # 检查 estate_code 是否已存在
    estate_code = newData.get("estate_code", "")
    if any(item.get("estate_code") == estate_code for item in data):
        print(f"estate_code '{estate_code}' 已存在，跳过追加。")
        return  # 如果已存在，跳过追加

    # 追加新数据
    data.append(newData)

    # 将更新后的数据写回文件
    with open(filePath, "w", encoding="utf-8") as jsonFile:
        json.dump(data, jsonFile, ensure_ascii=False, indent=4)


# 将爬取下俩的json,处理成我们需要的json
def handlerDetailJsonToOurJson():
    # "en-US", "zh-TW", "zh-CN"
    mongodbJson = {
        "estate_code": "",
        "estate_name": {"en": "", "zh": "", "cn": ""},
        "images": [],
        "description": {"en": "", "zh": "", "cn": ""},
        "join_time": [],
        "estate_phase": "",
        "property_quantity": "",
        "unit_quantity": "",
        "mtr": {"en": "", "zh": "", "cn": ""},
        "walking_time": "",
        "estate_type": {"en": "", "zh": "", "cn": ""},
        "estate_address": {"en": "", "zh": "", "cn": ""},
        "school_network": {
            "primary_school": "",
            "primary_school_network_url": "",
            "secondary_school": {"en": "", "zh": "", "cn": ""},
            "secondary_school_network_url": "",
        },
        "category_tags": {"en": "", "zh": "", "cn": ""},
        "developer": {"en": "", "zh": "", "cn": ""},
        "other_facility": [],
        "google_map": "",
    }

    folderPath = "./centanet/json/detail-test"
    jsonFiles = glob.glob(os.path.join(folderPath, "*.json"))
    outputFilePath = "./centanet/json/mongodbJson.json"

    for filePath in jsonFiles:
        with open(filePath, "r", encoding="utf-8") as file:
            data = json.load(file)
            # 处理每个屋苑的详情
            print(f"正在处理文件: {filePath}")
            mongodbJson["estate_code"] = data["en-US"].get("typeCode", "")

            mongodbJson["estate_name"]["en"] = (
                data["en-US"].get("route", {}).get("estateName", {}).get("en", "")
            )
            mongodbJson["estate_name"]["zh"] = (
                data["en-US"].get("route", {}).get("estateName", {}).get("hk", "")
            )
            mongodbJson["estate_name"]["cn"] = (
                data["en-US"].get("route", {}).get("estateName", {}).get("sc", "")
            )

            images = data["en-US"].get("media", {}).get("images", [])
            paths = [image.get("path", "") for image in images]
            mongodbJson["images"] = paths

            mongodbJson["description"]["en"] = data["en-US"].get(
                "estateDescription", ""
            )
            mongodbJson["description"]["zh"] = data.get("zh-TW", {}).get(
                "estateDescription", ""
            )
            mongodbJson["description"]["cn"] = data.get("zh-CN", {}).get(
                "estateDescription", ""
            )

            mongodbJson["join_time"] = [
                data["en-US"].get("minOpDate", ""),
                data["en-US"].get("maxOpDate", ""),
            ]

            mongodbJson["estate_phase"] = data["en-US"].get("phaseCount", "")
            mongodbJson["property_quantity"] = data["en-US"].get("buildingCount", "")
            mongodbJson["unit_quantity"] = data["en-US"].get("unitCount", "")

            mongodbJson["mtr"]["en"] = data["en-US"].get("mtrStation", "")
            mongodbJson["mtr"]["zh"] = data.get("zh-TW", {}).get("mtrStation", "")
            mongodbJson["mtr"]["cn"] = data.get("zh-CN", {}).get("mtrStation", "")

            mongodbJson["walking_time"] = data["en-US"].get("walkMtrTime", "")

            mongodbJson["estate_type"]["en"] = (
                data["en-US"].get("estateUsage", {}).get("label", "")
            )
            mongodbJson["estate_type"]["zh"] = (
                data.get("zh-TW", {}).get("estateUsage", {}).get("label", "")
            )
            mongodbJson["estate_type"]["cn"] = (
                data.get("zh-CN", {}).get("estateUsage", {}).get("label", "")
            )

            mongodbJson["estate_address"]["en"] = data["en-US"].get("address", "")
            mongodbJson["estate_address"]["zh"] = data.get("zh-TW", {}).get(
                "address", ""
            )
            mongodbJson["estate_address"]["cn"] = data.get("zh-CN", {}).get(
                "address", ""
            )

            mongodbJson["school_network"]["primary_school"] = (
                data["en-US"].get("schoolNet", {}).get("primarySchoolNetwork", "")
            )
            mongodbJson["school_network"]["primary_school_network_url"] = (
                data["en-US"].get("schoolNet", {}).get("schoolSchNetUrl", "")
            )
            mongodbJson["school_network"]["secondary_school"]["en"] = (
                data["en-US"]
                .get("schoolNet", {})
                .get("secondarySchoolScope", {})
                .get("db", "")
            )
            mongodbJson["school_network"]["secondary_school"]["zh"] = (
                data.get("zh-TW", {})
                .get("schoolNet", {})
                .get("secondarySchoolScope", {})
                .get("db", "")
            )
            mongodbJson["school_network"]["secondary_school"]["cn"] = (
                data.get("zh-CN", {})
                .get("schoolNet", {})
                .get("secondarySchoolScope", {})
                .get("db", "")
            )
            mongodbJson["school_network"]["secondary_school_network_url"] = (
                data.get("en-US", {})
                .get("schoolNet", {})
                .get("secondarySchoolDistbdUrl", "")
            )

            mongodbJson["category_tags"]["en"] = data["en-US"].get(
                "catLabelDescription", ""
            )
            mongodbJson["category_tags"]["zh"] = data.get("zh-TW", {}).get(
                "catLabelDescription", ""
            )
            mongodbJson["category_tags"]["cn"] = data.get("zh-CN", {}).get(
                "catLabelDescription", ""
            )

            mongodbJson["developer"]["en"] = data["en-US"].get("developer", "")
            mongodbJson["developer"]["zh"] = data.get("zh-TW", {}).get("developer", "")
            mongodbJson["developer"]["cn"] = data.get("zh-CN", {}).get("developer", "")

            # 处理 other_facility
            other_facilities = data["en-US"].get("otherFacilities", [])
            for index, fac in enumerate(other_facilities):
                mongodbJson["other_facility"].append(
                    {
                        "tag": {
                            "en": fac.get("tag", ""),
                            "zh": data.get("zh-TW", {})
                            .get("otherFacilities", [{}])[index]
                            .get("tag", ""),
                            "cn": data.get("zh-CN", {})
                            .get("otherFacilities", [{}])[index]
                            .get("tag", ""),
                        }
                    }
                )
            gMap = data["en-US"].get("gMap", {})
            # https://www.google.com/maps/embed?origin=mfe&pb=!1m3!2m1!1s22.243528366088867,114.14844512939453!6i15
            # mongodbJson["google_map"] = (
            #     f"https://www.google.com/maps/@{gMap.get('lat', '')},{gMap.get('lng', '')},15z"
            # )
            mongodbJson["google_map"] = (
                f"https://www.google.com/maps/embed?origin=mfe&pb=!1m3!2m1!1s{gMap.get('lat', '')},{gMap.get('lng', '')}!6i15"
            )
            appendToJson(outputFilePath, mongodbJson)

    print("所有文件处理完成，数据已保存到:", outputFilePath)


def createDataIntoDB():
    try:
        with open("./centanet/json/mongodbJson.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        # 发送 POST 请求到指定的 URL
        response = session.post(
            CREATE_DB_URL,
            json={"data": data, "field": "estate_code"},
        )

        # 检查响应状态码
        if response.status_code == 200:
            print("数据成功插入到数据库")
        else:
            print(
                f"插入数据失败，状态码: {response.status_code}, 错误信息: {response.text}"
            )

    except Exception as e:
        print(f"发生错误: {e}")


def main():
    # getHousingEstateList()
    # 异步 这个太快了,接口会限制
    asyncio.run(getHousingEstateDetailAsync())
    # 同步 选择一个执行
    # getHousingEstateDetail()
    # handlerDetailJsonToOurJson()
    # createDataIntoDB()
    pass


if __name__ == "__main__":
    main()
