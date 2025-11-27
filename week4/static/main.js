document.addEventListener('DOMContentLoaded', () => 
{
// task1
    const loginForm = document.getElementById('login-form');
    const agree = document.getElementById('agree');

    if (loginForm && agree) {
    loginForm.addEventListener('submit', (e) => {
        if (!agree.checked) {
        e.preventDefault(); // 阻止提交
        alert('請勾選同意條款');
        }
    });
    }

// task4
  const hotelInput = document.getElementById('hotel-id');
  const hotelBtn = document.getElementById('hotel-go');

  function go(){
    const raw = (hotelInput.value || '').trim(); // 「?.」：若 hotelInput 是 null/undefined，hotelInput?.value 會回傳 undefined。「|| ''」：若左邊為「假值」（undefined、空字串等），會回空字串，確保後面可安全呼叫 trim()。trim()：.trim()：去除字串前後的空白字元。若沒有元素或沒有內容，最後會得到 ''。
    // 檢查是否為正整數
    if (!/^[1-9]\d*$/.test(raw)) { // 也可寫 isPosInt = Number.isInteger(Number(raw)) && Number(raw) > 0 && String(Number(raw)) === raw; if (!isPosInt) {alert('請輸入正整數');return;}
    alert('請輸入正整數');
    return; // 中止函式（不執行window.location.href）
    }
    window.location.href = `/hotel/${raw}` // location.href = url 會把 raw 插進 URL 字串，瀏覽器會立刻做一次完整導頁，對該 URL 發出 HTTP GET 請求並載入新頁面，而且保留這次導向在瀏覽器歷史中（可用返回鍵回到上一頁）。也可寫location.assign(url) 。location.replace(url) 則不保留歷史紀錄。
  }
  if (hotelBtn && hotelInput) {
    hotelBtn.addEventListener('click', go);
    // 讓輸入框按 Enter 時也能導向
    // hotelInput.addEventListener('keydown', (e) => {
    //   if (e.key === 'Enter') {
    //         go();
    //   }
    // });
  }
});

