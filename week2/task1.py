# 記錄角色位置，分左右兩邊
location_left = [["悟空", 0, 0], ["辛巴", -3, 3], ["貝吉塔", -4, -1], ["特南克斯", 1, -2]]
location_right = [["丁滿", -1, 4], ["弗利沙", 4, -1]]

# 製作絕對值函式
def absolute_value(num):
    if num < 0:
        return -num
    else:
        return num

# 計算距離函式
def calculate_distance(x1, y1, x2, y2):
    return absolute_value(x1 - x2) + absolute_value(y1 - y2)

# 記錄input與每個角色的距離
def record(name):
    each_distance = []
    for i, (n1, x1, y1) in enumerate(location_left):
        if n1 == name:
            for k, (n2, x2, y2) in enumerate(location_left):
                if k == i:
                    continue
                each_distance.append([n2, calculate_distance(x1, y1, x2, y2)])
            for (n2, x2, y2) in location_right:
                each_distance.append([n2, calculate_distance(x1, y1, x2, y2)+2])
    if not each_distance:
        for i, (n1, x1, y1) in enumerate(location_right):
            if n1 == name:
                for k, (n2, x2, y2) in enumerate(location_right):
                    if k == i:
                        continue
                    each_distance.append([n2, calculate_distance(x1, y1, x2, y2)])
                for (n2, x2, y2) in location_left:
                    each_distance.append([n2, calculate_distance(x1, y1, x2, y2)+2])
    return each_distance

# 主程式：找出最遠與最近的角色
def func1(name):
    lst = record(name)
    max_distance = float("-inf")
    min_distance = float("inf")
    max_character = ""
    min_character = ""
    for who, dist in lst:
        if dist > max_distance:
            max_distance = dist
            max_character = who
        elif dist == max_distance:
            max_character = max_character + "、" + who
    for who, dist in lst:
        if dist < min_distance:
            min_distance = dist
            min_character = who
        elif dist == min_distance:
            min_character = min_character + "、" + who
    print("最遠" + max_character + ";最近" + min_character)
