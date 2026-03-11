import streamlit as st
import google.generativeai as genai
import os

# 웹페이지 기본 설정
st.set_page_config(page_title="리뷰 자동 생성 툴", page_icon="📝", layout="wide")

st.title("📝 실전 방문객 리뷰 자동 생성기")
st.markdown("지역명, 매장명, 주력메뉴를 입력하면 **구글 리뷰 10개, 카카오맵 리뷰 10개**를 즉시 생성합니다.")

# 입력 폼
col1, col2, col3 = st.columns(3)
with col1:
    region = st.text_input("📍 지역명", placeholder="예: 연남동")
with col2:
    store_name = st.text_input("🏪 매장명", placeholder="예: 홍길동 식당")
with col3:
    menu = st.text_input("🍽️ 주력메뉴", placeholder="예: 마라탕")

# API 키 가져오기 (Streamlit 클라우드 환경에 맞게 보완)
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    API_KEY = os.environ.get("GEMINI_API_KEY")

if st.button("리뷰 20개 생성하기 (구글 10 + 카맵 10)", type="primary"):
    if not API_KEY:
        st.error("API 키가 설정되지 않았습니다. 스트림릿 Advanced settings의 Secrets에 API 키를 입력해주세요.")
    elif region and store_name and menu:
        with st.spinner('실제 방문객 데이터를 분석하여 리뷰를 작성 중입니다... ⏳'):
            try:
                genai.configure(api_key=API_KEY)
                
                # 오류가 발생했던 모델명을 가장 안정적인 모델로 변경했습니다.
                model = genai.GenerativeModel('gemini-pro')
                
                prompt = f"""
                당신은 식당/매장 방문객처럼 자연스러운 후기를 작성하는 리뷰 생성기입니다.
                
                [입력 정보]
                - 지역명: {region}
                - 매장명: {store_name}
                - 주력메뉴: {menu}
                
                위 정보를 바탕으로 아래 두 가지 플랫폼의 유저 성향에 맞춰 각각 정확히 10개씩, 총 20개의 리뷰를 생성하세요. 
                AI가 쓴 듯한 기계적이고 과장된 표현은 절대 피하고, 실제 한국인 손님이 스마트폰으로 대충 적은 듯한 현실적인 표현을 사용하세요.
                
                1. 구글 리뷰 스타일 (10개)
                - 상세하고 친절한 후기, 매장 분위기나 서비스 등 전반적인 경험을 긍정적으로 평가. 주로 존댓말 사용.
                
                2. 카카오맵 리뷰 스타일 (10개)
                - 매우 솔직하고 직설적, 맛과 가성비 등 핵심만 짚음. 단답형, 음슴체, 반말 위주 ("~함", "맛있음", "그냥 그럼").
                
                결과는 마크다운 형식을 사용하여 구글과 카카오맵 섹션을 나누어 번호를 매겨 깔끔하게 보여주세요.
                """
                
                response = model.generate_content(prompt)
                
                st.success("✨ 리뷰 생성이 완료되었습니다!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
    else:
        st.warning("지역명, 매장명, 주력메뉴를 모두 입력해주세요.")
