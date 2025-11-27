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