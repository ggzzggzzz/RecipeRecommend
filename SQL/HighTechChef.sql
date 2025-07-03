-- 유저 테이블 생성
CREATE TABLE USERS (
    USER_NO     NUMBER PRIMARY KEY,                         -- 자동 증가 번호
    USER_ID     VARCHAR2(30) NOT NULL UNIQUE,               -- 로그인 ID
    NICKNAME    VARCHAR2(50) NOT NULL,                      -- 닉네임
    EMAIL       VARCHAR2(100) NOT NULL UNIQUE,              -- 이메일
    PASSWORD    VARCHAR2(100) NOT NULL,                     -- 비밀번호
    STATUS      CHAR(1) DEFAULT 'Y' CHECK (STATUS IN ('Y', 'N')), -- 계정 상태 기본값 Y
    REGDATE     DATE DEFAULT SYSDATE,                       -- 가입일 (기본: 현재 시각)
    USER_TYPE   CHAR(1) DEFAULT 'U' CHECK (USER_TYPE IN ('U', 'A')) -- 사용자 유형 기본 U
);

-- 식재료 마스터 테이블 생성
CREATE TABLE INGREDIENTS_MASTER (
    INGREDIENT_ID   NUMBER PRIMARY KEY,          -- 고유 식재료 ID
    NAME            VARCHAR2(200) NOT NULL UNIQUE,  -- 식재료 이름 (중복 불가)
    COUNT           NUMBER DEFAULT 1 NOT NULL       -- 식재료 크롤링 횟수
);

-- 사용자의 보유 식재료 테이블 생성
CREATE TABLE USER_INGREDIENTS (
    USER_NO         NUMBER,
    INGREDIENT_ID   NUMBER,
    REGDATE         DATE DEFAULT SYSDATE,
    PRIMARY KEY (USER_NO, INGREDIENT_ID),
    FOREIGN KEY (USER_NO) REFERENCES USERS(USER_NO),
    FOREIGN KEY (INGREDIENT_ID) REFERENCES INGREDIENTS_MASTER(INGREDIENT_ID)
);

-- 레시피 마스터 테이블 생성
CREATE TABLE RECIPES_MASTER (
    RECIPE_ID     NUMBER PRIMARY KEY,         -- 레시피 고유 ID
    NAME          VARCHAR2(200) NOT NULL,     -- 레시피 이름
    DESCRIPTION   VARCHAR2(3000),             -- 소개글
    IMAGE_URL     VARCHAR2(500),              -- 대표 이미지 경로
    RECIPE_URL    VARCHAR2(500) NOT NULL      -- 레시피 상세 링크
);

-- 식재료 단위당 가격 테이블 (식재료 가격 pool에서 레시피의 재료로 실제로 존재하는 데이터만 추려서(가격계산을 위해) 저장해두는 테이블
CREATE TABLE INGREDIENT_PRICE (
    INGREDIENT_ID   NUMBER,                           -- 식재료 ID
    UNIT            VARCHAR2(20),                     -- 단위 (예: g, 개, ml)
    QTY             NUMBER NOT NULL,                  -- 수량
    PRICE           NUMBER NOT NULL,                  -- 가격 (원 단위)
    STD_DATE        DATE NOT NULL,                    -- 기준일
    PRIMARY KEY (INGREDIENT_ID, UNIT),
    FOREIGN KEY (INGREDIENT_ID) REFERENCES INGREDIENTS_MASTER(INGREDIENT_ID)
);

-- 레시피에 사용되는 식재료 정보 테이블 생성
CREATE TABLE RECIPE_INGREDIENT_DETAIL (
    ID               NUMBER PRIMARY KEY,            -- 고유 식별자 (수동 증가)
    RECIPE_ID        NUMBER NOT NULL,               -- 레시피 ID (FK)
    INGREDIENT_ID    NUMBER NOT NULL,               -- 재료 ID (FK)
    QTY_TEXT         VARCHAR2(100),                 -- 원본 수량 텍스트 (예: 1큰술)
    QTY_VALUE        NUMBER,                        -- 정규화된 수치 값 (예: 1.5)
    QTY_UNIT         VARCHAR2(30),                  -- 정규화된 단위 (예: g, 개)
    PARSE_FLAG       CHAR(1),                       -- 파싱 여부(Y/N/P/M/E 등)
    PARSE_NOTE       VARCHAR2(100),                 -- 파싱 설명

    CONSTRAINT FK_RECIPE FOREIGN KEY (RECIPE_ID)
        REFERENCES RECIPES_MASTER(RECIPE_ID),

    CONSTRAINT FK_INGREDIENT FOREIGN KEY (INGREDIENT_ID)
        REFERENCES INGREDIENTS_MASTER(INGREDIENT_ID)
);