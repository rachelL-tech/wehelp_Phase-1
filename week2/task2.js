const services = [
  { "name":"S1", "r": 4.5, "c": 1000 },
  { "name":"S2", "r": 3,   "c": 1200 },
  { "name":"S3", "r": 3.8, "c": 800 }
];

// 建立時間表，並確保每個時間點都是一個陣列，以便使用push()存放多個service
let timeline = [];
for (let i = 0; i < 25; i++) {
timeline[i] = [];
}
/* 優化：可以用Set()避免includes()O(n)：因為includes()會去陣列裡「一個一個」比對，假設一個時段裡有100個服務，它就要檢查100次。這樣速度是「O(n)」——代表需要花的時間會隨資料量變多。
timeline[] = new Set();
timeline[].add();
timeline[9].has();//超快，只需一次查找 */

// 拆解criteria
function split_criteria (criteria) {
    let i = 0;
    let field = "";
    let operator = "";
    let value = "";
    const opChars = ["<", ">", "="];
    while (i<criteria.length && !opChars.includes(criteria[i])) {
        field += criteria[i];
        i++;
    }
    while (i<criteria.length && opChars.includes(criteria[i])) {
        operator += criteria[i];
        i++;
    }
    value = criteria.slice(i);
    return {field, operator, value};
}
/* 優化：
const m = criteria.trim().match(/^(\w+)\s*(<=|>=|=)\s*(.+)$/);
let [, field, operator, value] = m; */

// 找滿足criteria的service
function match_criteria (criteria) {
    let split_result = split_criteria(criteria);
    let field = split_result.field;
    let operator = split_result.operator;
    let value = split_result.value;
    let result = [];
    for (let s of services) {
        if (operator === "=") {
            if (s.name == value) {
                result.push(s.name);
            }
        } else if (operator === "<=") {
            if (s[field] <= Number(value)) {
                result.push(s.name);
            }
        } else if (operator === ">=") {
            if (s[field] >= Number(value)) {
                result.push(s.name);
            }
        }
    }
    return {result, field, value};
}

// 判斷時間有沒有重疊
function is_time_available(service, start, end){
    for (let i=start; i<end; i++){
        if (timeline[i].includes(service)){
            return false;
        }
    }
    return true;
}

// 分配時間
function allocate_time(service, start, end){
    for (let i=start; i<end; i++){
        timeline[i].push(service);
    }
}

// 主程式
function func2(ss, start, end, criteria){
    let { result, field, value } = match_criteria(criteria);
    let available_service = [];
    for (let r of result){
        if (is_time_available(r, start, end)){
            available_service.push(r);
        }
    }
    if (available_service.length === 0){
        console.log("Sorry");
    } 
    else if(available_service.length > 1){
        // 選出最佳解
        let min_range = Infinity;
        let best_service;
        for (let a of available_service){
            let matched_service = services.find(ss => ss.name === a);
            let range = Math.abs(matched_service[field]-Number(value));
            if (range < min_range){
                min_range = range;
                best_service = a;
            }
        }
        allocate_time(best_service, start, end);
        console.log(best_service);
    }
    else{
        allocate_time(available_service[0], start, end);
        console.log(available_service[0]);
    }
}