import streamlit as st
from PIL import Image
import pandas as pd
from datetime import datetime
import os

# -------------------------
# 스타일 요소 세팅
st.set_page_config(page_title="혈액 건강 헴톡(Hemetalk)", page_icon="❤️", layout="centered")
st.markdown("""
    <style>
        .main {
            background-color: #F9F9F9;
        }
        .stButton>button {
            background-color: #6A9EFA;
            color: white;
            font-weight: bold;
            border-radius: 10px;
            padding: 10px 24px;
        }
        .title-style {
            font-size: 2.3rem;
            font-weight: bold;
            color: #D13B3B;
        }
        .subtitle-style {
            font-size: 1.3rem;
            color: #555;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------------
# 타이틀과 설명
st.markdown('<div class="title-style">❤️ 혈액 건강 헴톡(Hemetalk)</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-style">간단한 정보를 입력하면 건강 피드백과 맞춤 추천을 드려요!</div>', unsafe_allow_html=True)

# -------------------------
# 사용자 입력
st.header("📝 내 혈액 수치 기록하기")
name = st.text_input("이름을 입력하세요:")
date = st.date_input("측정 날짜를 선택하세요:", value=datetime.today())

col1, col2 = st.columns(2)
with col1:
    gender = st.radio("성별을 선택하세요:", ("남성", "여성"))
    caffeine = st.radio("최근 카페인 섭취 여부:", ("예", "아니오"))
    caffeine_time = st.selectbox("카페인 음료를 언제 드셨나요?", ["식사 전", "식사 직후", "식후 2시간 이상 후", "섭취하지 않음"])

with col2:
    hb_input = st.number_input("헤모글로빈 수치 (g/dL):", min_value=5.0, max_value=20.0, step=0.1)
    diet_quality = st.radio("오늘 식단에 철+비타민C 조합이 있었나요?", ("예", "아니오", "모르겠음"))

sleep_hours = st.slider("어젯밤 수면 시간 (시간 단위)", min_value=0, max_value=12, value=7)

save_path = "./records.csv"

if st.button("기록 저장하기"):
    new_data = pd.DataFrame({
        "이름": [name],
        "날짜": [date.strftime('%Y-%m-%d')],
        "성별": [gender],
        "카페인 섭취": [caffeine],
        "카페인 시간대": [caffeine_time],
        "식단 철+비타민C": [diet_quality],
        "수면 시간": [sleep_hours],
        "헤모글로빈": [hb_input]
    })

    if os.path.exists(save_path):
        df = pd.read_csv(save_path)
        df = pd.concat([df, new_data], ignore_index=True)
    else:
        df = new_data

    df.to_csv(save_path, index=False)
    st.success("✅ 기록이 저장되었습니다!")

# -------------------------
# 분석 및 피드백
st.markdown("---")
st.subheader("\U0001F4AC 피드백 결과")

def is_anemia(gender, hb):
    if gender == "남성":
        return hb < 13
    else:
        return hb < 12

if st.button("결과 확인"):
    if is_anemia(gender, hb_input):
        st.error("⚠️ 빈혈 가능성이 있습니다.")
        st.markdown("**추천 철분제:** (철분 함량 기준)")

        col1, col2 = st.columns(2)
        with col1:
            st.image("https://i.imgur.com/pZuEZn9.png", caption="훼마틴 (철분 30mg)", use_container_width=True)
        with col2:
            st.image("https://i.imgur.com/SZ8kVPd.png", caption="솔가 철분제 (철분 25mg)", use_container_width=True)

        st.markdown("**카페인 적은 음료 추천:** (카페인 함량 기준)")
        col4, col5, col6 = st.columns(3)
        with col4:
            st.image("https://i.imgur.com/Y2rhXFW.png", caption="보리차 (0mg)", use_container_width=True)
        with col5:
            st.image("https://i.imgur.com/qeN0j4d.png", caption="디카페인 커피 (약 3mg)", use_container_width=True)
        with col6:
            st.image("https://i.imgur.com/DU0B24Y.png", caption="두유 (약 2mg)", use_container_width=True)

        if caffeine == "예":
            st.info("카페인 섭취를 줄이는 것이 철분 흡수에 도움이 됩니다. 저카페인 음료로 대체해보세요!")
        else:
            st.success("앞으로도 카페인을 줄이는 습관을 유지해보세요. 철분 흡수에 매우 좋습니다!")

    else:
        st.success("\U0001f44d 정상 범위입니다. 건강을 유지하세요!")
        st.markdown("**추천 건강 습관:** 철분이 풍부한 음식 섭취, 비타민 C와 함께 복용")

        if caffeine == "예":
            st.info("현재 카페인을 섭취 중이시군요. 철분 흡수를 방해할 수 있으니 주의해주세요!")
        else:
            st.success("카페인을 피하고 있는 점이 아주 좋아요! 계속 유지해주세요.")

    # 수면 시간에 따른 피드백
    st.markdown("---")
    st.markdown("**🛏 수면 상태 피드백:**")
    if 7 <= sleep_hours <= 8:
        st.success("하루 7–8시간 규칙적으로 자면 피도 튼튼! 혈액 건강에 딱 좋은 수면이었어요!")
    elif sleep_hours < 6:
        st.warning("수면이 너무 짧으면 몸에 만성 스트레스가 생겨 조혈에 방해될 수 있어요. 조금만 더 자보면 어때요?")
    elif sleep_hours > 9:
        st.warning("너무 과한 수면도 몸의 리듬을 깨뜨릴 수 있어요. 7–8시간 정도로 맞춰보세요!")

    # 식단에 따른 피드백
    st.markdown("---")
    st.markdown("**🥗 오늘의 식단 코칭:**")
    if diet_quality == "예":
        st.success("철 + 비타민 C 조합 식사를 하셨군요! 철분 흡수에 아주 좋아요.")
    elif diet_quality == "아니오":
        st.warning("철분 흡수를 높이려면 시금치, 살코기, 콩, 귤 같은 음식을 함께 드셔보세요!")
    else:
        st.info("혹시 식단에 철분과 비타민 C 조합이 있었는지 확인해보는 것도 도움이 됩니다.")

    # 카페인 섭취 시간에 따른 피드백
    st.markdown("---")
    st.markdown("**☕️ 카페인 섭취 시기 피드백:**")
    if caffeine_time == "식사 전" or caffeine_time == "식사 직후":
        st.warning("식사 직후의 카페인은 철분 흡수를 방해할 수 있어요. 다음엔 식후 2시간 후로 조정해보세요!")
    elif caffeine_time == "식후 2시간 이상 후":
        st.success("카페인을 식후 2시간 이후에 섭취하셨군요! 철분 흡수를 방해하지 않는 좋은 습관입니다.")
    else:
        st.info("오늘은 카페인 섭취를 피하셨군요. 철분 흡수에 좋은 선택입니다!")

    st.markdown("""
    <hr>
    <small>본 피드백은 참고용입니다. 건강 이상이 의심될 경우 전문가의 진료를 권장합니다.</small>
    """, unsafe_allow_html=True)
