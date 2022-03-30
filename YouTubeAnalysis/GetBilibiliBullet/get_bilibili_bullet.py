import re
import requests
import pandas as pd
import time
from tqdm import trange
import utils

# 视频页面点击“浏览器地址栏小锁-Cookie-bilibili.com-Cookie-SESSDATA”进行获取
SESSDATA = "393e5651%2C1658538566%2Ccaeed*11"
# 视频页面“按F12-Console-输入document.cookie”进行获取
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
    info["标题"] = data["data"]["View"]["title"]
    info["总弹幕数"] = data["data"]["View"]["stat"]["danmaku"]
    info["视频数量"] = data["data"]["View"]["videos"]
    info["cid"] = [dic["cid"] for dic in data["data"]["View"]["pages"]]
    if info["视频数量"] > 1:
        info["子标题"] = [dic["part"] for dic in data["data"]["View"]["pages"]]
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
        if info["视频数量"] > 1:
            print("cid:", cid, "弹幕数:", len(dms), "子标题:", info["子标题"][i])
        all_dms += dms
    print(f"共获取弹幕{len(all_dms)}条！")
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
    vid = input("输入视频编号: ")
    info = get_info(vid)
    bullets = get_bullet(info)
    print(len(bullets))
    sheet = utils.getCollection2MongoDB("bullet")
    sheet.insert_one({"vid": vid, "bullets": bullets})

