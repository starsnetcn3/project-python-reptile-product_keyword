import requests


def http_request(method, url, data=None, headers=None):
    try:
        # 根据请求方法发送请求
        if method.upper() == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method.upper() == "GET":
            response = requests.get(url, headers=headers)
        elif method.upper() == "PUT":
            response = requests.put(url, json=data, headers=headers)
        elif method.upper() == "DELETE":
            response = requests.delete(url, json=data, headers=headers)
        else:
            raise ValueError("不支持的请求方法: {}".format(method))

        # 确保请求成功
        response.raise_for_status()
        return response.json()  # 返回响应的 JSON 数据

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP 错误: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"连接错误: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"请求超时: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"请求错误: {req_err}")
    except ValueError as json_err:
        print(f"JSON 解码错误: {json_err}")
    except Exception as e:
        print(f"其他错误: {e}")
