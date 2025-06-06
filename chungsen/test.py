import requests

image = 'https://www.chungsen.com.hk/attachment/2025-04/1745291701XghkX.jpg'  
extension = image.split('.')[-1][:3]
# if extension == 'jpe':
extension = 'jpg'

print("2222", extension)

body = {
    "url": image,
    "extension": extension
}

try:
    res = requests.post("https://file.starsnet.com.hk/api/upload/bucket-by-url/development", json=body)
    print("20002202020", res)

    if res.status_code == 200:
        print("20002202020", res.text)
    else:
        print(f"Error: Received status code {res.status_code}. Response: {res.text}")

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except requests.exceptions.ConnectionError as conn_err:
    print(f"Connection error occurred: {conn_err}")
except requests.exceptions.Timeout as timeout_err:
    print(f"Timeout error occurred: {timeout_err}")
except requests.exceptions.RequestException as req_err:
    print(f"An error occurred: {req_err}")