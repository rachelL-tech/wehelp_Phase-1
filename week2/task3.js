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
