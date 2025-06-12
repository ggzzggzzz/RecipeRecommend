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


label_map = {
    'tomato': '토마토',
    'potato': '감자',
    'onion': '양파',
    'cucumber': '오이',
}


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


""" 데이터베이스에서 가져오기 전에 하드코딩으로 재료넣기

# 사용자 보유 재료
user_ingredients = {
    "닭다리살", "밥", "양파", "파", "마늘", "계란", "소주", "간장", "후추",
    "설탕", "소금", "물", "올리브오일", "올리고당", "버터", "케찹", "전분가루",
    "맛술", "물엿", "짜파게티", "다시다", "소고기 등심", "돈까스소스", "양송이 버섯"
}
"""
# 데이터베이스에서 식재료 가져오기
def get_user_ingredients(user_id: str) -> set:
    cursor.execute("""
        SELECT I.NAME
        FROM USERS U
        JOIN USER_INGREDIENTS UI ON U.USER_NO = UI.USER_NO
        JOIN INGREDIENTS_MASTER I ON UI.INGREDIENT_ID = I.INGREDIENT_ID
        WHERE U.USER_ID = :1
    """, (user_id,))
    rows = cursor.fetchall()
    return set(row[0] for row in rows)

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

#사용자가 식재료 입력 했을때 디비에 저장하는 로직
@app.post("/add-ingredient")
def add_ingredient(user_id: str = Form(...), name: str = Form(...)):
    name = name.strip()  # ✅ 공백 제거

    try:
        # 🔍 디버깅용 출력
        print(f"\n[디버깅] 입력된 식재료 이름: '{name}'")

        cursor.execute("SELECT NAME FROM INGREDIENTS_MASTER")
        all_ingredients = [r[0] for r in cursor.fetchall()]
        print("[디버깅] INGREDIENTS_MASTER 테이블 내 식재료 목록:")
        for ing in all_ingredients:
            print(f"  - '{ing}' (길이: {len(ing)})")

        # 유저 번호 가져오기
        cursor.execute("SELECT USER_NO FROM USERS WHERE USER_ID = :1", (user_id,))
        user_row = cursor.fetchone()
        if not user_row:
            raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")
        user_no = user_row[0]

        # 식재료 마스터에 존재하는지 확인
        cursor.execute("SELECT INGREDIENT_ID FROM INGREDIENTS_MASTER WHERE NAME = :1", (name,))
        ing_row = cursor.fetchone()
        if not ing_row:
            raise HTTPException(status_code=400, detail=f"'{name}'은(는) 등록된 식재료가 아닙니다.")

        ingredient_id = ing_row[0]

        # 중복 아니면 user_ingredients에 삽입
        cursor.execute("""
            SELECT 1 FROM USER_INGREDIENTS WHERE USER_NO = :1 AND INGREDIENT_ID = :2
        """, (user_no, ingredient_id))
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO USER_INGREDIENTS (USER_NO, INGREDIENT_ID) VALUES (:1, :2)
            """, (user_no, ingredient_id))
            conn.commit()

        return {"message": f"{name} 등록 완료!"}

    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    

#로그인했을때 인풋스크린에 보유식재료 자동추가
@app.get("/user-ingredients")
def get_user_ingredients(user_id: str):
    try:
        # 유저 번호 가져오기
        cursor.execute("SELECT USER_NO FROM USERS WHERE USER_ID = :1", (user_id,))
        user_row = cursor.fetchone()
        if not user_row:
            raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")
        user_no = user_row[0]

        # 해당 사용자의 보유 식재료 조회
        cursor.execute("""
            SELECT I.NAME
            FROM USER_INGREDIENTS UI
            JOIN INGREDIENTS_MASTER I ON UI.INGREDIENT_ID = I.INGREDIENT_ID
            WHERE UI.USER_NO = :1
        """, (user_no,))
        rows = cursor.fetchall()
        names = [r[0] for r in rows]

        return {"ingredients": names}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#인풋 화면에서 식재료 삭제하면 데이터베이스에서도 삭제되도록 하기
@app.post("/remove-ingredient")
def remove_ingredient(user_id: str = Form(...), name: str = Form(...)):
    try:
        # 유저 번호 조회
        cursor.execute("SELECT USER_NO FROM USERS WHERE USER_ID = :1", (user_id,))
        user_row = cursor.fetchone()
        if not user_row:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
        user_no = user_row[0]

        # 식재료 ID 조회
        cursor.execute("SELECT INGREDIENT_ID FROM INGREDIENTS_MASTER WHERE NAME = :1", (name,))
        ing_row = cursor.fetchone()
        if not ing_row:
            raise HTTPException(status_code=404, detail="식재료를 찾을 수 없습니다.")
        ingredient_id = ing_row[0]

        # USER_INGREDIENTS에서 삭제
        cursor.execute("""
            DELETE FROM USER_INGREDIENTS 
            WHERE USER_NO = :1 AND INGREDIENT_ID = :2
        """, (user_no, ingredient_id))
        conn.commit()

        return {"message": f"{name} 삭제 완료!"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))



""" 하드코딩된 재료데이터를 가지고 추천하던 알고리즘

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
    """

#레시피에 들어가는 재료와 사용자의 재료를 비교하여 추천하는 로직
@app.get("/recommend-from-db")
def recommend_recipes(user_id: str):
    try:
        # 사용자 번호 조회
        cursor.execute("SELECT USER_NO FROM USERS WHERE USER_ID = :1", (user_id,))
        user_row = cursor.fetchone()
        if not user_row:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
        user_no = user_row[0]

        # 사용자 보유 식재료 이름 목록 조회
        cursor.execute("""
            SELECT I.NAME
            FROM USER_INGREDIENTS UI
            JOIN INGREDIENTS_MASTER I ON UI.INGREDIENT_ID = I.INGREDIENT_ID
            WHERE UI.USER_NO = :1
        """, (user_no,))
        user_ingredients = [row[0] for row in cursor.fetchall()]
        if not user_ingredients:
            return {"recommended": []}

        # 모든 레시피 조회
        cursor.execute("""
            SELECT RM.RECIPE_ID, RM.NAME, RM.DESCRIPTION, RM.IMAGE_URL, RM.RECIPE_URL,
                   IM.NAME
            FROM RECIPES_MASTER RM
            JOIN RECIPE_INGREDIENTS RI ON RM.RECIPE_ID = RI.RECIPE_ID
            JOIN INGREDIENTS_MASTER IM ON RI.INGREDIENT_ID = IM.INGREDIENT_ID
        """)
        rows = cursor.fetchall()

        # 레시피별로 그룹화
        from collections import defaultdict
        recipe_dict = defaultdict(lambda: {
            "title": "",
            "description": "",
            "image_url": "",
            "url": "",
            "ingredients": set()
        })

        for recipe_id, title, desc, img_url, link, ingredient_name in rows:
            recipe = recipe_dict[recipe_id]
            recipe["title"] = title
            recipe["description"] = desc
            recipe["image_url"] = img_url
            recipe["url"] = link
            recipe["ingredients"].add(ingredient_name)

        # 사용자 재료가 모두 포함된 레시피만 필터링
        recommended = []
        for recipe_id, recipe in recipe_dict.items():
            recipe_ingredients = recipe["ingredients"]

            # 모든 사용자 재료가 일부 포함되는지 확인 (LIKE 유사 비교)
            is_all_matched = all(
                any(user_ing in ing for ing in recipe_ingredients)
                for user_ing in user_ingredients
            )

            if is_all_matched:
                recommended.append({
                    "recipe_id": recipe_id,
                    "title": recipe["title"],
                    "description": recipe["description"],
                    "image_url": recipe["image_url"],
                    "url": recipe["url"]
                })

        return {"recommended": recommended}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))







@app.get("/recommend")
def get_recommendations(user_id: str):
    try:
        user_ingredients = get_user_ingredients(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"식재료 조회 실패: {str(e)}")

    urls = [
        "https://www.10000recipe.com/recipe/6906510",  # 치킨데리야끼덮밥
        "https://www.10000recipe.com/recipe/7038639",  # 찹스테이크
        "https://www.10000recipe.com/recipe/7038158",  # 간짜파게티
        "https://www.10000recipe.com/recipe/6955624",  # 토마토 양파 샐러드
        "https://www.10000recipe.com/recipe/6904655",  # 초간단 토마토 양파 스프
        "https://www.10000recipe.com/recipe/6903806",  # 토마토 양파 스튜
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

#레시피디테일정보 디비에서 가져오는 코드
@app.get("/recipe-detail")
def get_recipe_detail(recipe_id: int):
    # 레시피 정보
    cursor.execute("""
        SELECT NAME, DESCRIPTION, IMAGE_URL, RECIPE_URL
        FROM RECIPES_MASTER
        WHERE RECIPE_ID = :1
    """, (recipe_id,))
    recipe = cursor.fetchone()
    if not recipe:
        raise HTTPException(status_code=404, detail="레시피가 존재하지 않습니다.")

    # ✅ 레시피 이름 등 변수명 구분
    recipe_name, description, image_url, recipe_url = recipe

    # 식재료 정보 + 가격
    cursor.execute("""
        SELECT 
            im.NAME,
            ri.IS_MAIN,
            NVL(ri.QTY, 0),
            NVL(ri.QTY_TEXT, ''),
            NVL(ri.UNIT, ''),
            ip.PRICE,
            ip.QTY,
            ip.UNIT
        FROM RECIPE_INGREDIENTS ri
        JOIN INGREDIENTS_MASTER im ON ri.INGREDIENT_ID = im.INGREDIENT_ID
        LEFT JOIN INGREDIENT_PRICE ip ON ip.INGREDIENT_ID = im.INGREDIENT_ID AND ip.UNIT = ri.UNIT
        WHERE ri.RECIPE_ID = :1
    """, (recipe_id,))

    ingredients = []
    total_price = 0

    # ✅ 식재료 이름도 별도 변수로 분리
    for ingredient_name, is_main, qty, qty_text, unit, price, price_qty, price_unit in cursor.fetchall():
        if price is not None and price_qty != 0:
            calculated_price = round(price * (qty / price_qty), 1)
            total_price += calculated_price
        else:
            calculated_price = None
        ingredients.append({
            "name": ingredient_name,
            "is_main": is_main == 'Y',
            "qty": qty,
            "qty_text": qty_text,
            "unit": unit,
            "price": calculated_price
        })

    return {
        "name": recipe_name,
        "description": description,
        "image_url": image_url,
        "recipe_url": recipe_url,
        "ingredients": ingredients,
        "total_price": round(total_price, 1)
    }




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
    results = model.predict(source=file_path, conf=0.7 , device=0)
    class_ids = results[0].boxes.cls.tolist()
    class_names = model.names
    detected_english = [class_names[int(i)] for i in class_ids]

       # ✅ 한글 매핑 적용
    detected_korean = [label_map.get(name, name) for name in detected_english]
    unique_detected = list(set(detected_korean))

    return JSONResponse(content={
        "image": filename,
        "detected_objects": detected_korean,
        "unique_objects": unique_detected
    })
