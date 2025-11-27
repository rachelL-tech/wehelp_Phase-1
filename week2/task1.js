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