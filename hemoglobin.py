import streamlit as st

# -------------------------
# 페이지 설정
st.set_page_config(page_title="Hemetalk 홈", page_icon="🩸", layout="centered")

# -------------------------
# 홈 화면 꾸미기
st.markdown("""
    <style>
    .title {
        font-size: 38px;
        color: #D13B3B;
        font-weight: bold;
    }
    .section {
        font-size: 20px;
        color: #444;
    }
    .highlight {
        color: #4682B4;
        font-weight: bold;
    }
    /* 사이드바 메뉴 텍스트 크기와 간격 조정 */
    [data-testid="stSidebar"] ul li {
        font-size: 22px !important;
        margin-bottom: 18px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">❤️ 혈액 건강 헴톡(Hemetalk)</div>', unsafe_allow_html=True)

st.markdown("""
### 🧬 <span class="highlight">헤모글로빈(Hemoglobin)</span>이란?
- 혈액 속 적혈구에 들어있는 단백질로, **산소를 온몸으로 운반**해줘요. 
- 부족하면 **빈혈**, 많으면 **혈액 질환**이 생길 수 있어요.

### 🌡️ <span class="highlight">왜 Hb 수치가 중요할까요?</span>
- Hb는 **건강 상태를 직접적으로 보여주는 지표**예요.
- 피로, 어지럼증, 집중력 저하가 Hb 수치와 관련 있을 수 있어요.

### 💖 <span class="highlight">혈액 건강</span>을 지키는 습관은?
- 규칙적인 **수면과 식사**, 철분과 비타민이 풍부한 음식, 카페인 조절, 운동 등이 중요해요!

> 🩸 **헴톡(Hemetalk)** 은 여러분의 혈액 건강을 지켜주는 똑똑한 AI 친구예요! 
> 지금 왼쪽에서 기능을 선택해보세요 👈
""", unsafe_allow_html=True)

