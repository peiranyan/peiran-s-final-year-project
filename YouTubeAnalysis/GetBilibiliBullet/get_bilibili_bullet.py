import re
import requests
import pandas as pd
import time
from tqdm import trange


# Click on "cookie-bilibili.com-Cookie-SESSDATA" in your browser's address bar to get it.
SESSDATA = "393e5651%2C1658538566%2Ccaeed*11"
# "Press F12-Console-enter document.cookie" to get video page
cookie = "buvid3=6EADC56B-5867-6BD4-D6F9-3DA1A5DDB97F38051infoc; i-wanna-go-back=-1; " \
         "_uuid=4BD8C246-6BF4-5E5D-10FEC-E55A9CB13A9538290infoc; sid=cel91s1j; buvid_fp_plain=undefined; " \
         "DedeUserID=36858087; DedeUserID__ckMd5=751e0d42f9c0541a; b_ut=5; bp_t_offset_36858087=618896695645092229; " \
         "LIVE_BUVID=AUTO9516429367085911; CURRENT_BLACKGAP=0; blackside_state=0; rpdid=|(k|~|mlR~kl0J'uYRkmJ))k); " \
         "PVID=1; fingerprint=0e34cabb908b3a6eb2960ba05e34cab1; bili_jct=f3418c63daa9c90dc6e47f3fd2f29d55; " \
         "buvid4=2F9E65F0-9979-FC19-1F3F-A85A13565C0309399-022012507-jRbf6X/z8RCBThLE2tWFrQ%3D%3D; " \
         "buvid_fp=0e34cabb908b3a6eb2960ba05e34cab1; CURRENT_FNVAL=4048; b_lsid=47FF137D_17EA0C5F37B; innersign=0 "
cookie += f";SESSDATA={SESSDATA}"
headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/96.0.4664.110 Safari/537.36",
    "cookie": cookie,
}


def get_info(vid):
    url = f"https://api.bilibili.com/x/web-interface/view/detail?bvid={vid}"
    response = requests.get(url, headers=headers)
    response.encoding = "utf-8"
    data = response.json()
    info = {}
    info["Title"] = data["data"]["View"]["title"]
    info["Total no. of bullet chats"] = data["data"]["View"]["stat"]["danmaku"]
    info["No. of videos"] = data["data"]["View"]["videos"]
    info["cid"] = [dic["cid"] for dic in data["data"]["View"]["pages"]]
    if info["No. of videos"] > 1:
        info["Child title"] = [dic["part"] for dic in data["data"]["View"]["pages"]]
    for k, v in info.items():
        print(k + ":", v)
    return info


def get_danmu(info, start, end):
    date_list = [i for i in pd.date_range(start, end).strftime("%Y-%m-%d")]
    all_dms = []
    for i, cid in enumerate(info["cid"]):
        dms = []
        for j in trange(len(date_list)):
            url = f"https://api.bilibili.com/x/v2/dm/web/history/seg.so?type=1&oid={cid}&date={date_list[j]}"
            response = requests.get(url, headers=headers)
            # response.encoding = "utf-8"
            print(response.text)
            data = re.findall(r"[:](.*?)[@]", response.text)
            dms += [dm[1:] for dm in data]
            time.sleep(3)
        if info["No. of videos"] > 1:
            print("cid:", cid, "No. of bullet chats:", len(dms), "Child title:", info["Child title"][i])
        all_dms += dms
    print(f"There {len(all_dms)} bullet chats！")
    return all_dms


def get_bullet(information):
    result = []
    url = "https://comment.bilibili.com/{}.xml".format(information["cid"][0])
    response = requests.get(url)
    response.encoding = "utf-8"
    data = re.findall(r"(\">)(.*?)(</d>)", response.text)

    for c in data:
        result.append(c[1])
        print(c[1])
    return result


if __name__ == "__main__":
    vid = input("Input BV number: ")
    info = get_info(vid)
    bullets = get_bullet(info)
    with open("../Resource/Bullets/" + vid + ".txt", "w", encoding="utf-8") as f:
        for b in bullets:
            f.write(b + "\n")
