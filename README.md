카테고리
프로젝트 제목
프로젝트 정보
팀 소개
프로젝트 소개

시작 가이드
요구사항
설치및 실행
기술스택
화면 구성/API주소
주요기능
아키텍처



# 사용자 보유 식재료 기반 맞춤형 요리 레시피 추천 앱 개발
# **목적**: 폴리텍 하이테크 과정에서 서비스 개발 프로세스를 학습하기 위한 AI 융합 프로젝트 / 4개월
# 팀 : 황제윤(팀장)[기계학사, 디자인석사], 박한진[], 조영상 - 컴퓨터공학
![KakaoTalk_20250423_214455655_05](https://github.com/user-attachments/assets/75eaf153-b252-4a90-b51e-ae34e7377945)

# 프로젝트 소개 : 
바쁜 일상 속 식재료를 효율적으로 활용하지 못하는 사용자 예를 들어, 1인가구나 자취생을 대상으로
보유한 식재료를 기반으로 요리 가능한 음식 메뉴와 레시피를 추천해주고
음식 단가를 고려해 합리적인 선택을 할 수 있도록 가격 정보를 제공하는 서비스 개발

# 시작 가이드

### ⚙️ 설치 및 실행

```bash
# 백엔드 실행 (FastAPI)
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# 프론트엔드 실행 (React)
npm run ys

```
## 🛠️ 기술 스택

| 구분 | 기술 |
|------|------|
| **Frontend** | React, JavaScript, HTML5, CSS3, Axios |
| **Backend** | Python 3.10, FastAPI, Uvicorn |
| **Database** | Oracle DB |
| **AI 모델** | YOLOv8 (Ultralytics), OpenCV |
| **API 연동** | KAMIS 농산물 가격 정보 API |
| **환경 구성** | Visual Studio Code, Oracle SQL Developer |
| **버전 관리** | Git, GitHub |

# 화면 구성/API주소
![image](https://github.com/user-attachments/assets/a9f16f22-bafa-4a9b-9319-a8acebf30342)
![image](https://github.com/user-attachments/assets/e9da8b12-406c-46c1-9d6d-455e462f62c7)
![image](https://github.com/user-attachments/assets/1065654e-d266-4d50-972e-19bd561917c2)
![image](https://github.com/user-attachments/assets/54ffdb19-3bbf-4488-ab73-b9e89fb5eb09)
![image](https://github.com/user-attachments/assets/5040f288-9d12-490b-911c-8d45b5e24e1a)


# 주요 기능 및 역할 분담
 ### 👨‍💻 조영상 (전체 시스템 연동 및 핵심 기능 개발 총괄)
- **React 기반 프론트엔드 구현 및 백엔드 연동 전체 담당**
  - 화면 구성 (홈, 추천 결과, 디테일 등)
  - 사용자 입력값(보유 재료) 처리 및 카메라로 촬영한 이미지 저장 기능 구현
  - Axios를 활용해 FastAPI와 비동기 통신 처리
- **FastAPI 백엔드 설계 및 데이터 처리 흐름 구성**
  - AI 모델과의 연결 및 예측 결과 반환 API 구현
  - Oracle DB 연동 및 SQL 쿼리 처리 (cx_Oracle 활용)
  - 식재료 가격 정보 API(KAMIS) 연동 및 레시피 결과 통합
- **추천 알고리즘 로직 구현**
  - 보유 재료 기반으로 가능한 레시피 우선 추천
  - 일부 재료 부족 시 유사도 기반 레시피 제안 기능 포함

---

### 🎨 황제윤
- UI 디자인 기획 및 사용자 경험 흐름 초안 설계
- 서비스 전체 컨셉 및 기획 주도
- AI모델 학습!!!
- 데이터베이스 구조 정의 및 초기 더미 데이터 구성 보조
- 레시피 및 식재료 데이터 수집

### 🛠️ 박한진
- 가격 계싼
- 

# 아키텍처 및 디렉토리 구조
디렉토리 구조
아키텍처
![image](https://github.com/user-attachments/assets/9598558d-7a36-4ec1-8fa3-6d03d1345c55)

# 향후 개선 사항

