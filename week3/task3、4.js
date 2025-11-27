document.addEventListener('DOMContentLoaded', async function(){
    const URL_ATTRACTIONS = "https://cwpeng.github.io/test/assignment-3-1";
    const URL_IMAGES = "https://cwpeng.github.io/test/assignment-3-2";

    // 對兩個URL同時發請求抓資料+解析
    async function retrieveJsonFrom(url){
        const resp = await fetch(url);
        return await resp.json();
    }
    const [dataAttractions, dataImages] = await Promise.all([retrieveJsonFrom(URL_ATTRACTIONS), retrieveJsonFrom(URL_IMAGES)]);

    // 從dataAttractions、dataImages取出我要的資訊
    const attraction = [];
    const attraction_rows = dataAttractions["rows"];
    for (let i = 0; i < attraction_rows.length; i++){
        attraction.push({serial: attraction_rows[i]["serial"], sname: attraction_rows[i]["sname"]});
    }
    // 從字串中擷取出第一張圖片的網址的函式
    function slice_url(str){
        const i = str.indexOf(".jpg");
        return str.slice(0, i+4);
    }
    const image = [];
    const host = "https://www.travel.taipei";
    const image_rows = dataImages["rows"];
    for (let i = 0; i < image_rows.length; i++){
        image.push({serial: image_rows[i]["serial"], url: host + slice_url(image_rows[i]["pics"])})
    }
    // 以serial為key合併成map
    const merged = new Map();
    for (const {serial, sname} of attraction) { // 以attraction的順序為基底
        if (!merged.has(serial)){
            merged.set(serial, {Name: sname, url: undefined});
        }
    }
    for (const {serial, url} of image){
        if (merged.get(serial)){ // 當merged裡找得到這個serial時
            merged.get(serial).url = url;
        }
    }
    console.log(merged);
    // 將merged轉為陣列、切片
    const attractions = [...merged.values()];
    const barsData = attractions.slice(0, 3);
    const contentData = attractions.slice(3);
    let cursor = 3; // contentData的起始位置

    // 渲染到W1網頁
    const PAGE_SIZE = 10;
    // 抓節點
    const barsElement = document.querySelector('.bars');
    const contentElement = document.querySelector('.content');
    const loadMoreBtn = document.getElementById('load-more');
    // 清空原有元素
    function clear(node){
        while (node.firstChild){ // firstChild會回傳第一個子節點，如果沒有子節點則是null
            node.removeChild(node.firstChild);
        }
    }
    // 建立圖片節點
    function createImg({className, src, alt}){
        const img = document.createElement('img');
        img.className = className;
        img.src = src;
        img.alt = alt;
        return img;
    }
    // 渲染bars
    function renderBars(datas){
        clear(barsElement);
        datas.forEach(function ({Name, url}){
            // const frag = document.createDocumentFragment();
            const card = document.createElement('article');
            card.className = 'bar';
            const img = createImg({
                className: 'bar_image',
                src: url,
                alt: Name
            });
            const title = document.createElement('div');
            title.className = 'bar_text';
            title.textContent = Name;
            card.appendChild(img);
            card.appendChild(title);
            // frag.appendChild(card);
            barsElement.appendChild(card);
        });
        // barsElement.appendChild(frag);
    }
    // 清空content
    let cleared = false;
    function clearOldcontent(){
        if (cleared) return;
        clear(contentElement);
        cleared = true;
    }
    clearOldcontent();
    // 按鈕狀態
    function updateButtonstate(){
    const remaining = contentData.length - cursor;
    if (remaining <= 0){
        loadMoreBtn.textContent = "No More";
        loadMoreBtn.disabled = true;
    }else{
        loadMoreBtn.disabled = false;
    }
    }
    // 渲染首十筆content
    function renderContent(){
        const datas = contentData.slice(cursor, cursor + PAGE_SIZE);
        datas.forEach(function ({Name, url}){
            // const frag = document.createDocumentFragment();
            const card = document.createElement('article');
            card.className = 'blocks';
            const img = createImg({
                className: 'blocks_image',
                src: url,
                alt: Name
            });
            const star = createImg({
                className: 'blocks_star',
                src: 'star icon.png',
                alt: 'star'
            });
            const title = document.createElement('div');
            title.className = 'blocks_text';
            const span = document.createElement('span'); // 因為原本瀏覽器自動在文字外面包了一層匿名盒子（anonymous flex item），但不能對匿名盒子直接加樣式（做 ellipsis 控制），因此要包<span>讓文字節點成為明確的flex item。
            span.textContent = Name;
            title.appendChild(span);
            card.appendChild(img);
            card.appendChild(star);
            card.appendChild(title);
            // frag.appendChild(card);
            contentElement.appendChild(card);
        });
        // contentElement.appendChild(frag);
        cursor += PAGE_SIZE;
        updateButtonstate();
    }
    // 動態注入ellipsis樣式至<span>的寫法
    // function injectEllipsCSS(){
    //     const style = document.createElement('style');
    //     style.textContent = `
    //     .blocks_text span {
    //         white-space: nowrap;
    //         overflow: hidden;
    //         text-overflow: ellipsis;
    //         min-width: 0; 
    //         display: block;     
    //         width: 100%;       
    //         text-align: center;  
    //     }
    //     `;
    //     document.head.appendChild(style);
    // }
    // injectEllipsCSS();
    // 首次載入
    renderBars(barsData);
    renderContent(contentData);
    loadMoreBtn.addEventListener('click', renderContent);
});