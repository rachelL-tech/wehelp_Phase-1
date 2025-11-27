// task1
//記錄角色位置，分左右兩邊
let location_left = [["悟空", 0, 0], ["辛巴", -3, 3], ["貝吉塔", -4, -1], ["特南克斯",1, -2]];
let location_right = [["丁滿", -1, 4], ["弗利沙", 4, -1]];

//製作絕對值函式
function absolute_value(num){
    if (num < 0){
        return -num;
    } else {
        return num;
    }
}

//計算距離函式
function calculate_distance(x1, y1, x2, y2){
    return absolute_value(x1 - x2) + absolute_value(y1 - y2);
}

//記錄input與每個角色的距離
function record(name){
    const each_distance = [];
    for (let i = 0; i < location_left.length; i++){
        if (location_left[i][0] === name){ // 代表找到input所在位置
            for (let k = 0; k < location_left.length; k++){
                if (k === i){
                    continue; // 跳過input
                }else {
                    each_distance.push([location_left[k][0],calculate_distance(location_left[i][1], location_left[i][2], location_left[k][1], location_left[k][2])]); // 記錄[左邊角色名稱, 距離]
                }
            }
            for (let k = 0; k < location_right.length; k++){ 
                each_distance.push([location_right[k][0],calculate_distance(location_left[i][1], location_left[i][2], location_right[k][1], location_right[k][2])+2]); // 記錄[右邊角色名稱, 距離+2]
            }
        }
    }
    if (!each_distance.length){ // 代表沒input不在左邊，換找右邊
        for (let i = 0; i < location_right.length; i++){
            if (location_right[i][0] === name){
                for (let k = 0; k < location_left.length; k++){
                    each_distance.push([location_left[k][0],calculate_distance(location_right[i][1], location_right[i][2], location_left[k][1], location_left[k][2])+2]);
                    }
                for (let k = 0; k < location_right.length; k++){
                    if (k === i){
                        continue;
                    }else {
                        each_distance.push([location_right[k][0],calculate_distance(location_right[i][1], location_right[i][2], location_right[k][1], location_right[k][2])]);
                    }
                }
            }    
        }
    }
    return each_distance;
}

//主程式：找出最遠與最近的角色
function func1(name){
    const list = record(name);
    let max_distance = -Infinity;
    let min_distance = Infinity;
    let max_character = "";
    let min_character = "";
    for (let i = 0; i < list.length; i++){
        if (list[i][1] > max_distance){ 
            max_distance = list[i][1];
            max_character = list[i][0];
        }else if (list[i][1] == max_distance){
            max_character = max_character + "、" + list[i][0];
        }
    }
    for(let j = 0; j < list.length; j++){
        if (list[j][1] < min_distance){
            min_distance = list[j][1];
            min_character = list[j][0];
        }else if (list[j][1] == min_distance){
            min_character = min_character + "、" + list[j][0];
        }
    }
    console.log("最遠" + max_character + ";最近" + min_character);
}
func1("辛巴");
func1("悟空"); 
func1("弗利沙"); 
func1("特南克斯"); 

// task2
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
func2(services, 15, 17, "c>=800");
func2(services, 11, 13, "r<=4");
func2(services, 10, 12, "name=S3");
func2(services, 15, 18, "r>=4.5");
func2(services, 16, 18, "r>=4");
func2(services, 13, 17, "name=S1");
func2(services, 8, 9, "c<=1500");

// task3
function func3(index){
    let quotient = Math.floor(index/4);
    let remainder = index%4;
    if (remainder === 0){
        let answer = 23 + (-2) * (quotient - 1);
        console.log(answer);
    }else if (remainder === 1){
        let answer = 23 + (-2) * quotient;
        console.log(answer);
    }else if (remainder === 2){
        let answer = 23 + (-2) * quotient + (-3);
        console.log(answer);
    }else if (remainder === 3){
        let answer = 23 + (-2) * quotient + (-2);
        console.log(answer);
    }
}
// 更有邏輯的寫法是
// function func3(index){
//     let base = [25, 23, 20, 21];
//     let quotient = Math.floor(index/4);
//     let remainder = index%4;
//     let answer = base[remainder] + (-2) * quotient;
//     console.log(answer);
// }
func3(1); 
func3(5); 
func3(10); 
func3(30);

// task4
function func4(sp, stat, n){
    let available_seat = sp;
    let status = [];
    let range = [];
    let min = Infinity;
    let most_fitted_car = -1;
    //把status從字串改為陣列
    for (let s of stat) {
        status.push(Number(s));
    }
    //計算每個車廂的available spaces與乘客數量的差異（以找出最佳解）
    for (let a of available_seat){
        range.push(Math.abs(a-n));
    }
    //判斷可乘車廂，再判斷該車廂為最佳解
    let i = 0;
    for (let r of range){
        if (status[i] === 0){
            if ( r < min){
                most_fitted_car = i;
                min = r;
            }
        }
        i++;
    }
    console.log(most_fitted_car);
}
func4([3, 1, 5, 4, 3, 2], "101000", 2);
func4([1, 0, 5, 1, 3], "101000", 4);
func4([4, 6, 5, 8], "1000", 4);