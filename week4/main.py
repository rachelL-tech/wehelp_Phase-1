from fastapi import FastAPI, Request, Form # Request 可以接受到前端整個傳過來的請求
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

# 利用 uvicorn 去啟動伺服器在 http://127.0.0.1:8000

app = FastAPI() # 建立FastAPI物件
app.add_middleware(SessionMiddleware, secret_key="3453fgw45") # 開啟 session 管理使用者狀態

# 告訴FastAPI，Jinja2 模板放在 "templates" 這個資料夾
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def index(request: Request):
    context = {
        "request": request, # TemplateResponse內部強制要求context["request"]存在，而且要是一個 Request 物件
        "title": "歡迎光臨，請輸入信箱密碼"
    }
    return templates.TemplateResponse("index.html", context) # 用 TemplateResponse 把模板 + 資料組合起來

@app.post("/login")
async def login(
    request: Request, 
    email: str = Form(""), 
    password: str = Form("")
): # 把 Form() 拿掉後，FastAPI會把 email、password 視為query parameters
    if not email or not password: # 也忽略只輸入空白的情況
        return RedirectResponse(url="/ohoh?msg=請輸入信箱和密碼", status_code=303)
    if email == "abc@abc.com" and password == "abc":
        request.session["LOGGED-IN"] = True
        return RedirectResponse(url="/member", status_code=303)
    return RedirectResponse(url="/ohoh?msg=帳號、或密碼輸入錯誤", status_code=303)    

@app.get("/member")
async def member(request: Request):
    if not request.session.get("LOGGED-IN"): # 檢查 session 裡有沒有 LOGGED_IN
        return RedirectResponse(url="/", status_code=303)
    context = {
        "request": request,
        "title": "歡迎光臨，這是會員頁"
    }
    return templates.TemplateResponse("member.html", context)

@app.get("/ohoh")
async def ohoh(request: Request, msg: str = ""):
    context = {
        "request": request,
        "title": "失敗頁面",
        "message": msg
    }
    return templates.TemplateResponse("ohoh.html", context)

@app.get("/logout")
async def logout(request: Request):
    request.session["LOGGED-IN"] = False # 清 session，也可寫request.session.clear()
    return RedirectResponse(url="/", status_code=303)

@app.get("/hotel/{id}", response_class=HTMLResponse)
async def hotel(request: Request, id: int):
    hotel_info = merge.get(id)
    result = hotel_info['ChineseName'] + "、" + hotel_info['EnglishName'] + "、" + hotel_info['Phone']
    context = {
        "request": request,
        "result": result
    }
    return templates.TemplateResponse("hotel.html", context)

app.mount("/static", StaticFiles(directory="static"), name="static")

# task4 存取資料
import urllib.request as request
import json 
src_chinese = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch"
src_english = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en"
with request.urlopen(src_chinese) as response_chinese:
    data_chinese = json.load(response_chinese)
with request.urlopen(src_english) as response_english:
    data_english = json.load(response_english)
list1 = data_chinese["list"]
list2 = data_english["list"]
result_chinese = []
result_english = []
for hotel in list1:
    result_chinese.append({"id": hotel['_id'], "ChineseName": hotel['旅宿名稱'], "Phone": hotel['電話或手機號碼']})
for hotel in list2:
    result_english.append({"id": hotel['_id'], "EnglishName": hotel['hotel name']})
merge = {}
for ch in result_chinese:
    for eg in result_english:
        if ch['id'] == eg['id']:
            merge[int(ch['id'])] = {"ChineseName": ch["ChineseName"], "EnglishName": eg["EnglishName"], "Phone": ch["Phone"]}
            break
