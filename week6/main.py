from fastapi import FastAPI, Request, Form # Request 可以接受到前端整個傳過來的請求
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import mysql.connector

# 利用 uvicorn 去啟動伺服器在 http://127.0.0.1:8000

app = FastAPI() # 建立FastAPI物件
app.add_middleware(SessionMiddleware, secret_key="3453fgw45") # 開啟 session 管理使用者狀態

# 告訴FastAPI，Jinja2 模板放在 "templates" 這個資料夾
templates = Jinja2Templates(directory="templates")

#建立共用的 MySQL 連線函式
def get_connection(): 
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="website",
        charset="utf8mb4",
        use_unicode=True
    )

@app.get("/") # 宣告一條路由：當有人對 / 發 GET 請求時，呼叫這個函式處理並回應
def index(request: Request):
    context = {
        "request": request # TemplateResponse內部強制要求context["request"]存在，而且要是一個 Request 物件
    }
    return templates.TemplateResponse("index.html", context) # 用 TemplateResponse 把模板 + 資料組合起來

@app.post("/signup")
def signup(
    # request: Request, 
    name: str = Form(""), 
    email: str = Form(""), 
    password: str = Form("")
):
    con = get_connection()
    cursor = con.cursor(dictionary=True) # 用字典(dict)回傳，而不是用tuple，以便用「欄位名字」取值

    # 不分大小寫，檢查有無重複 email
    email_lower = email.lower()
    cursor.execute("SELECT id FROM member WHERE email = %s", (email_lower,))
    existing = cursor.fetchone()
    if existing:
        con.close()
        return RedirectResponse(url="/ohoh?msg=重複的電子郵件", status_code=303)
    
    # 插入member資料，因為有early return不用寫else
    cursor.execute(
        "INSERT INTO member(name, email, password) VALUES (%s, %s, %s)",
        (name, email_lower, password)
    )
    con.commit()
    cursor.close()
    con.close()
    return RedirectResponse(url="/", status_code=303)

@app.post("/login")
def login(
    request: Request, 
    email: str = Form(""), 
    password: str = Form("")
): # email: str = Form() 告訴 FastAPI：從 HTML 表單（application/x-www-form-urlencoded 或 multipart/form-data）的欄位 name="email" 讀入，並轉成 str。如果把 Form() 拿掉，FastAPI會把 email、password 視為query parameters
    con = get_connection()
    cursor = con.cursor(dictionary=True)

    email_lower = email.lower()
    fetchData = """
        SELECT id, name, email 
        FROM member
        WHERE LOWER(email) = LOWER(%s) AND password = %s
    """
    cursor.execute(fetchData, (email_lower, password))
    memberData = cursor.fetchone()
    cursor.close()
    con.close()

    # 不存在該member
    if not memberData:
        return RedirectResponse(url="/ohoh?msg=電子郵件或密碼錯誤", status_code=303)
    
    # 存在該member，設定登入狀態
    request.session["id"] = memberData["id"]
    request.session["name"] = memberData["name"]
    request.session["email"] = memberData["email"]
    return RedirectResponse(url="/member", status_code=303)

@app.get("/member")
def member(request: Request):
    id = request.session.get("id")
    if not id: # 檢查 session 裡有沒有 id
        return RedirectResponse(url="/", status_code=303)
    
    con = get_connection()
    cursor = con.cursor(dictionary=True)

    fetchData = """
        SELECT message.id AS message_id, message.content, message.member_id, member.name 
        FROM message
        JOIN member ON message.member_id = member.id
        ORDER BY message.id DESC
    """
    cursor.execute(fetchData)
    messages = cursor.fetchall()
    cursor.close()
    con.close()

    context = {
        "request": request,
        "name": request.session["name"],
        "messages": messages,
        "id": id
    }
    return templates.TemplateResponse("member.html", context)

@app.post("/createMessage")
def createMessage(request:Request, content: str = Form("")):
    id = request.session.get("id")
    if not id:
        return RedirectResponse(url="/", status_code=303)
    if not content:
        return RedirectResponse(url="/member", status_code=303)
    
    con = get_connection()
    cursor = con.cursor()

    cursor.execute("INSERT INTO message (member_id, content) VALUES (%s, %s)", (id, content))
    con.commit()
    cursor.close()
    con.close()

    return RedirectResponse(url="/member", status_code=303)

@app.post("/deleteMessage")
def deleteMessage(
    request: Request, 
    message_id: int = Form("")
):
    id = request.session.get("id")
    if not id:
        return RedirectResponse(url="/", status_code=303)
    
    con = get_connection()
    cursor = con.cursor(dictionary=True)

    cursor.execute("DELETE FROM message WHERE id = %s AND member_id = %s", (message_id, id))
    # 可以用 cursor.rowcount == 0 判斷DELETE有執行到，進而判斷是否為惡意刪除(被硬改 hidden input / 用 curl、fetch() 亂送)

    con.commit()
    cursor.close()
    con.close()
    return RedirectResponse(url="/member", status_code=303)


@app.get("/ohoh")
def ohoh(request: Request, msg: str = ""):
    context = {
        "request": request,
        "message": msg
    }
    return templates.TemplateResponse("ohoh.html", context)

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)

app.mount("/static", StaticFiles(directory="static"), name="static") # name="static" 讓jinja2模板裡 url_for('static', ...) 找得到這個靜態檔案路由
