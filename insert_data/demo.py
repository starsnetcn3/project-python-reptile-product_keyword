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

# 后端配置
API_URL = "http://127.0.0.1:3008"
API_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiaWF0IjoxNzQ3Mjk1NDI4LCJleHAiOjE3NDc5MDAyMjh9.fo4HKZWkxnLO1Du5oncvvyhHLab1J49lIQjrN8_0818"

# 插入数据库 start
def create_headers():
    """创建HTTP请求头"""
    return {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }



def main():
    product_item_id = "6815e4b4932afe000a7105cc"
    # 通过shopify的id去mongodb里面查询all的product
    all_product_data = requests.get(
        f"{API_URL}/common/all/MProduct",
        headers=create_headers(),
        params={
            "shopify_product_id": json.dumps({"$in": [str(product_item_id)]})
        }
    ).json()

    print("----all_product_data data", all_product_data["data"])

if __name__ == "__main__":
    main()