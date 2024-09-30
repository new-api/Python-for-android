import requests
import time
from tqdm import tqdm
import hashlib

times = int(input("请输入执行次数："))

def createPost(key, detail, title, cat_id, tag_id):

    base_url = "http://floor.huluxia.com/post/create/ANDROID/4.2.2"
    device_code = "[d]00000000-0000-0000-0000-00000000000"

    url_params = {
        "platform": 2,
        "gkey": "000000",
        "app_version": "4.3.0.3",
        "versioncode": 20141494,
        "market_id": "floor_huluxia",
        "_key": key,
        "device_code": device_code
    }

    headers = {
        "User-Agent": "okhttp/3.8.1"
    }

    data = {
        "draft_id": 0,
        "cat_id": cat_id,
        "tag_id": tag_id,
        "type": 0,
        "title": title,
        "detail": detail,
        "patcha": "",
        "voice": "",
        "lng": "0.0",
        "lat": "0.0",
        "images": "",
        "user_ids": "",
        "recommendTopics": "",
        "remindTopics": "",
        "sign": "",
        "is_app_link": "4"
    }

    sign_data = f"_key{key}detail{detail}device_code{device_code}imagestitle{title}voicefa1c28a5b62e79c3e63d9030b6142e4b".encode('utf-8')
    sign = hashlib.md5(sign_data).hexdigest().upper()
    data["sign"] = sign

    response = requests.post(base_url, headers=headers, params=url_params, data=data)
    print(response.text)

    return response.text

def getImageSizeFromUrl(url):
    return 1920, 1080

def main():
    imageFile = input("请输入链接文件：")
    prefix = input("请输入帖子前缀：")
    for _ in range(times):
        content1 = requests.get("https://api.luoh.my.to/New/Yiyan/?t=诗词/all").text
        title = f"{prefix}{content1}"
        print(f"title: {title}")

        content2 = requests.get("https://api.luoh.my.to/New/Yiyan/?t=诗词/all").text
        detailTemp1 = f"<text>{content2}</text>"

        with open(imageFile, 'r') as file:
            lines = file.readlines()

        firstThreeLines = lines[:3]
        remainingLines = lines[3:]

        with open(imageFile, 'w') as file:
            file.writelines(remainingLines)

        values = []
        for line in firstThreeLines:
            imageUrl = line.strip()
            width, height = getImageSizeFromUrl(imageUrl)
            values.append((imageUrl, width, height))

        detailTemp2 = "".join([f"<image>{v[0]},{v[1]},{v[2]}</image>" for v in values])
        detailTemp2 = detailTemp2.replace("http://cdn.u1.huluxia.com/", "")

        detail = f"{detailTemp1}{detailTemp2}"

        key = "EB3022964961498CA4D04B6026E8C1D3EF52B4C9A37B27EC7E76189DDC127004BEF26BD0CF8A0EB925B476686B56062AC708496423A6C0CE"
        catId = 98
        tagId = 9804

        createPost(key, detail, title, catId, tagId)

        for _ in tqdm(range(60), desc="等待时间", unit="秒"):
            time.sleep(1)

if __name__ == "__main__":
    main()