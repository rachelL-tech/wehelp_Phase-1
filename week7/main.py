from fastapi import FastAPI, Request, Form, Body # Request 可以接受到前端整個傳過來的請求
from fastapi.responses import JSONResponse, RedirectResponse
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
async def index(request: Request):
    context = {
        "request": request # TemplateResponse內部強制要求context["request"]存在，而且要是一個 Request 物件
    }
    return templates.TemplateResponse("index.html", context) # 用 TemplateResponse 把模板 + 資料組合起來

@app.post("/signup")
async def signup(
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
async def login(
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
        WHERE email = %s AND password = %s
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
async def member(request: Request):
    user_id = request.session.get("id")
    if not user_id: # 檢查 session 裡有沒有 id
        return RedirectResponse(url="/", status_code=303)
    
    context = {
        "request": request,
        "name": request.session["name"],
    }
    return templates.TemplateResponse("member.html", context)

@app.get("/api/member/{member_id}")
async def get_member(member_id: int, request: Request):
    user_id = request.session.get("id")
    if user_id is None:
        return {"data": None} # Python 的 None 會在 JSON 轉換時對應成 null
    
    con = get_connection()
    cursor = con.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, name, email FROM member WHERE id = %s",
        (member_id,)
    )
    data = cursor.fetchone()
    cursor.close()
    con.close()

    if data is None: # WHERE id = xxx 沒符合時，data 會是 None
        return {"data": None}
    else:
        target_id = data["id"]
        
        if target_id != user_id:
            con = get_connection()
            query_cursor = con.cursor()
            query_cursor.execute(
                "INSERT INTO query(target_member_id, searcher_member_id) VALUES (%s, %s)",
                (target_id, user_id)
            )
            con.commit()
            query_cursor.close()
            con.close()

        return{
            "data": {
                "id": data["id"],
                "name": data["name"],
                "email": data["email"],
            }
        }

@app.patch("/api/member")
async def update_member(request: Request, name: str = Body(..., embed=True)): # 沒有embed=True，FastAPI 預期收到的 整個 body 是純字串；有embed=True，FastAPI 預期收到的 body 會變成 JSON 物件 { "name": name }
    user_id = request.session.get("id")
    if user_id is None:
        return {"error": True} 
    
    name = name.strip()
    if not name:
        return {"error": True}

    con = get_connection()
    cursor = con.cursor()
    cursor.execute(
        "UPDATE member SET name = %s WHERE id = %s",
        (name, user_id)
    )
    con.commit()
    cursor.close()
    con.close()

    request.session["name"] = name

    return {"ok": True}

@app.get("/api/member_query_log")
async def get_query_log(request: Request):
    user_id = request.session.get("id")
    if user_id is None:
        return
    
    con = get_connection()
    cursor = con.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT q.created_at, m.name AS searcher_name
        FROM query AS q
        JOIN member AS m ON q.searcher_member_id = m.id
        WHERE q.target_member_id = %s
        ORDER BY q.created_at DESC
        LIMIT 10
        """,
        (user_id,)
    )
    rows = cursor.fetchall()
    cursor.close()
    con.close()

    data = []
    for row in rows:
        time = row["created_at"].strftime("%Y-%m-%d %H:%M:%S") # created_at 是 datetime 物件，要用 strftime 把時間轉成字串
        data.append({
            "searcher_name": row["searcher_name"],
            "time": time
        })
    
    return {"data": data}

@app.get("/ohoh")
async def ohoh(request: Request, msg: str = ""):
    context = {
        "request": request,
        "message": msg
    }
    return templates.TemplateResponse("ohoh.html", context)

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)

app.mount("/static", StaticFiles(directory="static"), name="static") # name="static" 讓jinja2模板裡 url_for('static', ...) 找得到這個靜態檔案路由
