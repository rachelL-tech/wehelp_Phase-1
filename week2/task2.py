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