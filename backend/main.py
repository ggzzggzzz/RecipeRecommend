from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from passlib.hash import bcrypt
import cx_Oracle
from ultralytics import YOLO
import requests
import re
import os
from datetime import datetime
from bs4 import BeautifulSoup

from typing import List, Dict, Any
import xml.etree.ElementTree as ET
from dotenv import load_dotenv


app = FastAPI()

# Oracle DB 연결 정보
dsn = cx_Oracle.makedsn("localhost", 1521, service_name="XEPDB1")
conn = cx_Oracle.connect(user="HihgTechChef", password="1234", dsn=dsn)
cursor = conn.cursor()

# -------------------------------
# 회원가입 API
# -------------------------------
@app.post("/signup")
def signup(user_id: str = Form(...), nickname: str = Form(...), email: str = Form(...), password: str = Form(...)):
    hashed_pw = bcrypt.hash(password)

    # 중복 확인
    cursor.execute("SELECT * FROM USERS WHERE USER_ID = :1 OR EMAIL = :2", (user_id, email))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="이미 사용 중인 아이디 또는 이메일입니다.")

    # 삽입
    try:
        cursor.execute("""
            INSERT INTO USERS (USER_ID, NICKNAME, EMAIL, PASSWORD)
            VALUES (:1, :2, :3, :4)
        """, (user_id, nickname, email, hashed_pw))
        conn.commit()
        return {"message": "회원가입 성공!"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------------
# 로그인 API
# -------------------------------
@app.post("/login")
def login(user_id: str = Form(...), password: str = Form(...)):
    cursor.execute("SELECT PASSWORD, NICKNAME FROM USERS WHERE USER_ID = :1 AND STATUS = 'Y'", (user_id,))
    row = cursor.fetchone()

    if not row:
        raise HTTPException(status_code=401, detail="존재하지 않는 계정입니다.")
    
    hashed_pw, nickname = row
    if not bcrypt.verify(password, hashed_pw):
        raise HTTPException(status_code=401, detail="비밀번호가 일치하지 않습니다.")

    return {"message": "로그인 성공!", "nickname": nickname}



# YOLO 모델 로드
model = YOLO('best.pt')



# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 이미지 저장 경로
UPLOAD_DIR = "./image"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 사용자 보유 재료
user_ingredients = {
    "닭다리살", "밥", "양파", "파", "마늘", "계란", "소주", "간장", "후추",
    "설탕", "소금", "물", "올리브오일", "올리고당", "버터", "케찹", "전분가루",
    "맛술", "물엿", "짜파게티", "다시다", "소고기 등심", "돈까스소스", "양송이 버섯"
}

tool_keywords = {
    "접시", "도마", "냄비", "프라이팬", "볼", "스푼", "위생장갑",
    "조리용가위", "조리용나이프", "계량컵", "조리용스푼", "스텐트레이"
}

def clean_ingredient_name(text):
    text = re.sub(r"([가-힣a-zA-Z])(\d)", r"\1 \2", text)
    text = re.sub(r"\d+[\/\d]*\s*[a-zA-Z가-힣%]*", "", text)
    text = re.sub(r"[^\w\s가-힣]", "", text)
    text = re.sub(r"(약간|조금|적당량|기호에 따라|취향껏|약|조금)", "", text)
    text = re.sub(r"\(.*?\)", "", text)
    return text.strip()

def extract_ingredient_names(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    title_tag = soup.select_one("div.view2_summary h3")
    title = title_tag.text.strip() if title_tag else "제목 없음"

    ingredients = soup.select("div.ready_ingre3 ul li")
    cleaned = set()
    for item in ingredients:
        raw = item.get_text(strip=True).replace("구매", "")
        name = clean_ingredient_name(raw)
        if name and name not in tool_keywords and len(name) <= 15:
            cleaned.add(name)

    return title, cleaned

# ✅ 레시피 추천 API
@app.get("/recommend")
def get_recommendations():
    urls = [
        "https://www.10000recipe.com/recipe/6906510",  # 치킨데리야끼덮밥
        "https://www.10000recipe.com/recipe/7038639",  # 찹스테이크
        "https://www.10000recipe.com/recipe/7038158",  # 간짜파게티

        "https://www.10000recipe.com/recipe/6955624", # 토마토 양파 샐러드
        "https://www.10000recipe.com/recipe/6904655", #초간단 토마토 양파 스프
        "https://www.10000recipe.com/recipe/6903806", #이나영,원빈의 다이어트식단 떠먹는 스테이크 토마토 양파 스테이크 (토마토스튜)
        ]
    exact_match = []
    near_match = []

    for url in urls:
        try:
            title, recipe_ingredients = extract_ingredient_names(url)
            missing = recipe_ingredients - user_ingredients

            recipe_data = {
                "title": title,
                "missing": list(missing),
                "url": url
            }

            if len(missing) == 0:
                exact_match.append(recipe_data)
            elif len(missing) <= 3:
                near_match.append(recipe_data)
        except Exception as e:
            print(f"Error processing {url}: {e}")

    return JSONResponse(content={
        "exact": exact_match,
        "near": near_match
    })

# ✅ 업로드 + YOLO 감지 통합 API
@app.post("/upload-and-detect")
async def upload_and_detect(image: UploadFile = File(...)):
    # 이미지 저장
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"captured_{timestamp}.png"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        content = await image.read()
        f.write(content)

    # YOLO 감지 수행
    results = model.predict(source=file_path, conf=0.7, device=0)
    class_ids = results[0].boxes.cls.tolist()
    class_names = model.names
    detected_names = [class_names[int(i)] for i in class_ids]
    unique_detected = list(set(detected_names))

    return JSONResponse(content={
        "image": filename,
        "detected_objects": detected_names,
        "unique_objects": unique_detected
    })
