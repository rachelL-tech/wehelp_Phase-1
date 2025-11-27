document.addEventListener('DOMContentLoaded', () => {
  // Call Member Query API
  const queryInput  = document.querySelector("#query-id");
  const queryBtn    = document.querySelector("#query-btn");
  const queryResult = document.querySelector("#query-result");

  queryBtn.addEventListener("click", async () => {
    const number = (queryInput.value || "").trim();
    if (number === "") {
      queryResult.textContent = "請輸入會員編號"; // .textContent 會把東西當「純文字」，不當成 HTML；.innerHTML則是把東西當「HTML 程式碼」，會解析成標籤來處理（建立節點）
      return;
    }

    // if (!/^[1-9]\d*$/.test(raw)) { // 「/^[1-9]\d*$/」是正規表達式（regex），test() 是 regex 的方法，回傳 True 代表 raw 符合這個規則
    //   alert('請輸入正整數 ID');
    //   return;
    // }

    const res = await fetch(`/api/member/${encodeURIComponent(number)}`); // Template literal + encodeURIComponent()把空白、?、#、/、& 、中文、emoji等轉成百分比編碼（percent-encoding），如%20、%2F後，再塞進URL，避免伺服器誤以為是URL結構的一部份而非純資料
    const json = await res.json();

    if (json.data) {
      queryResult.textContent = `${json.data.name} (${json.data.email})`;
    } else {
      queryResult.textContent = "無此會員";
    }
  });

  // Updating name
  const updateInput  = document.querySelector("#update-name");
  const updateBtn    = document.querySelector("#update-btn");
  const updateStatus = document.querySelector("#update-status");

  updateBtn.addEventListener("click", async() => {
    const name = (updateInput.value || "").trim();
    if (name === "") {
      updateStatus.textContent = "請輸入姓名"; 
      return;
    }

    const res = await fetch("/api/member", {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ "name": name }) // 把 JS 物件變成 JSON 字串
    });
    const json = await res.json();

    if (json.ok) {
      updateStatus.textContent = "更新成功";
      const welcomeName = document.querySelector("#welcome-name");
      welcomeName.textContent = name;
    }else {
      updateStatus.textContent = "更新失敗";
    }
  });

  // Tracking member queries
  const trackBtn = document.querySelector("#track-refresh");
  const trackList = document.querySelector("#track-list");

  trackBtn.addEventListener("click", async() => {
    const res = await fetch("/api/member_query_log");
    const json = await res.json();

    trackList.textContent = "";

    if(!json.data || json.data.length === 0){
      trackList.innerHTML = "沒有人查詢過你";
      return;
    }
    
    json["data"].forEach( data => {
      const p = document.createElement("p");
      p.textContent = `${data.searcher_name} (${data.time})`;
      trackList.appendChild(p);
    })
  });
});

