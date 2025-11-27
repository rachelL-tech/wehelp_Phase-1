# 下載http、把資料存進變數
import urllib.request as request
import json 
src_chinese = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch"
src_english = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en"
with request.urlopen(src_chinese) as response_chinese:
    data_chinese = json.load(response_chinese)
with request.urlopen(src_english) as response_english:
    data_english = json.load(response_english)
print(data_chinese)
list1 = data_chinese["list"]
list2 = data_english["list"]
result_chinese = []
result_english = []
for hotel in list1:
    result_chinese.append({"id": hotel['_id'], "ChineseName": hotel['旅宿名稱'], "ChineseAddress": hotel['地址'], "Phone": hotel['電話或手機號碼'], "RoomCount": int(hotel['房間數'])})
for hotel in list2:
    result_english.append({"id": hotel['_id'], "EnglishName": hotel['hotel name'], "EnglishAddress": hotel['address'], "Phone": hotel['tel']})

# 抽行政區，同時每筆依行政區，累計{'ＸＸ區': {'hotels': , 'rooms': }}字典
districts = {}
for r in result_chinese:
    dist = r['ChineseAddress'][3:6]
    # 中文版本地址去掉台北市ＸＸ區，覆蓋回原資料
    r['ChineseAddress'] = r['ChineseAddress'][6:]
    rooms = r['RoomCount']
    if dist not in districts: # 第一次掃到那個區時
        districts[dist] = {"HotelCount": 0, "RoomCount": 0}
    districts[dist]["HotelCount"] += 1
    districts[dist]["RoomCount"] += rooms
# 英文版本也把地址去掉", Dist., Taipei City, Taiwan (R.O.C.)"部分後，覆蓋回原資料
for r in result_english:
    for key in ["Taipei City", "taipei city", "Taipei", "Taipei city"]:
        i = r["EnglishAddress"].find(key)
        if i != -1: # 因為find()會"Taipei City", "taipei city", "Taipei", "Taipei city"三個都找，找不到時，return會是-1
            r["EnglishAddress"] = r["EnglishAddress"][:i-2]
            break

# 中英資料合併
merge = []
for ch in result_chinese:
    for eg in result_english:
        if ch['id'] == eg['id']:
            merge.append([ch["ChineseName"], eg["EnglishName"], ch['ChineseAddress'], eg["EnglishAddress"], ch["Phone"], ch["RoomCount"]])

# 輸出hotels.csv
with open("hotels.csv", "w", encoding="utf-8", newline="") as hotel_file: # 以寫入模式開一個文字檔，編碼 UTF-8
    for hotel in merge:
        hotel_file.write(hotel[0]+","+hotel[1]+","+hotel[2]+","+hotel[3]+","+hotel[4]+","+str(hotel[5])+"\n")

# 輸出districts.csv
with open("districts.csv", "w", encoding="utf-8", newline="") as district_file:
    for k, v in districts.items():
        district_file.write(k+","+str(v["HotelCount"])+","+str(v["RoomCount"])+"\n")
