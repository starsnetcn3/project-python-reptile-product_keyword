import ssl
import urllib3
import requests
import os


img_url = "https://www.chungsen.com.hk/attachment/2025-06/1748830671aIcck.jpg"

# Create less strict SSL context
ctx = ssl.create_default_context()
ctx.set_ciphers("DEFAULT@SECLEVEL=1")

# Fetch image
http = urllib3.PoolManager(ssl_context=ctx)
response = http.request("GET", img_url)

# Save image locally if successful
if response.status == 200:
    with open("temp.jpg", "wb") as f:
        f.write(response.data)
        print("Image downloaded.")
else:
    raise Exception(f"Failed to download image: status {response.status}")

upload_url = "https://file.starsnet.com.hk/api/upload/bucket/development"

with open("temp.jpg", "rb") as f:
    files = {"file": f.read()}
    response = requests.post(upload_url, files=files)

    if response.ok:
        print("Upload successful:", response.text)
    else:
        print("Upload failed:", response.status_code, response.text)

os.remove("temp.jpg")