# task1
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
func1("辛巴");
func1("悟空"); 
func1("弗利沙"); 
func1("特南克斯"); 

# task2
services = [
    {"name": "S1", "r": 4.5, "c": 1000},
    {"name": "S2", "r": 3, "c": 1200},
    {"name": "S3", "r": 3.8, "c": 800}
]

timeline = [[] for _ in range(25)]

def split_criteria(criteria):
    i = 0
    field = ""
    operator = ""
    value = ""
    opChars = ["<", ">", "="]
    while i < len(criteria) and criteria[i] not in opChars:
        field += criteria[i]
        i += 1
    while i < len(criteria) and criteria[i] in opChars:
        operator += criteria[i]
        i += 1
    value = criteria[i:]
    return {"field": field, "operator": operator, "value": value}

def match_criteria(criteria):
    split_result = split_criteria(criteria)
    field = split_result["field"]
    operator = split_result["operator"]
    value = split_result["value"]
    result = []
    for s in services:
        if operator == "=":
            if s["name"] == value:
                result.append(s["name"])
        elif operator == "<=":
            if s[field] <= float(value):
                result.append(s["name"])
        elif operator == ">=":
            if s[field] >= float(value):
                result.append(s["name"])

    return {"result": result, "field": field, "value": value}

def is_time_available(service, start, end):
    for i in range(start, end):
        if service in timeline[i]:
            return False
    return True

def allocate_time(service, start, end):
    for i in range(start, end):
        timeline[i].append(service)

def func2(ss, start, end, criteria):
    mc = match_criteria(criteria)
    result = mc["result"]
    field = mc["field"]
    value = mc["value"]
    available_service = []
    for r in result:
        if is_time_available(r, start, end):
            available_service.append(r)
    if len(available_service) == 0:
        print("Sorry")
    elif len(available_service) > 1:
        min_range = float("inf")
        best_service = ""
        for a in available_service:
           for s in services:
                if s["name"] == a:
                    rge = abs(s[field] - float(value))
                    if rge < min_range:
                        min_range = rge
                        best_service = a
        allocate_time(best_service, start, end)
        print(best_service)
    else:
        allocate_time(available_service[0], start, end)
        print(available_service[0])
func2(services, 15, 17, "c>=800")
func2(services, 11, 13, "r<=4")
func2(services, 10, 12, "name=S3")
func2(services, 15, 18, "r>=4.5")
func2(services, 16, 18, "r>=4")
func2(services, 13, 17, "name=S1")
func2(services, 8, 9, "c<=1500")

# task3
def func3(index: int) -> None:
    base = [25, 23, 20, 21]
    quotient = index // 4
    remainder = index % 4
    answer = base[remainder] + (-2) * quotient
    print(answer)
func3(1)
func3(5)
func3(10)
func3(30)

# task4
def func4(sp, stat, n):
    available_seat = sp
    status = []
    rng = []
    min_diff = float('inf')
    most_fitted_car = -1
    for s in stat:
        status.append(int(s))
    for a in available_seat:
        rng.append(abs(a-n))
    i = 0
    for r in rng:
        if status[i] == 0:
            if r < min_diff:
                most_fitted_car = i
                min_diff = r
        i += 1
    print(most_fitted_car)
func4([3, 1, 5, 4, 3, 2], "101000", 2)
func4([1, 0, 5, 1, 3], "101000", 4)
func4([4, 6, 5, 8], "1000", 4)