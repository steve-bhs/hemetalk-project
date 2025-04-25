import streamlit as st
from PIL import Image
import pandas as pd
from datetime import datetime
import os
import plotly.express as px

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
# 타임라인 리포트 시각화
st.markdown("---")
st.subheader("📈 나의 Hb 변화 리포트")

if st.button("❌ 모든 기록 초기화하기"):
    if os.path.exists("records.csv"):
        os.remove("records.csv")
        st.success("모든 기록이 초기화되었습니다. 새롭게 시작해보세요!")
        st.stop()
    else:
        st.info("기록 파일이 이미 없습니다.")

if os.path.exists("./records.csv"):
    df = pd.read_csv("./records.csv")
    selected_name = st.selectbox("리포트를 보고 싶은 이름을 선택하세요:", sorted(df["이름"].unique()))

    user_data = df[df["이름"] == selected_name].sort_values("날짜")
    user_data["날짜"] = pd.to_datetime(user_data["날짜"])

    fig = px.line(user_data, x="날짜", y="헤모글로빈", markers=True,
                  title=f"{selected_name}님의 헤모글로빈 변화 추이",
                  labels={"헤모글로빈": "Hb 수치 (g/dL)", "날짜": "측정일"})
    fig.update_traces(line=dict(width=3), marker=dict(size=10))
    fig.update_layout(margin=dict(t=40, b=40), height=400)
    st.plotly_chart(fig, use_container_width=True)

    latest = user_data.iloc[-1]
    st.markdown(f"**📌 가장 최근 측정일:** {latest['날짜'].date()}  |  **Hb:** {latest['헤모글로빈']} g/dL")
    st.markdown(f"**수면:** {latest['수면 시간']}시간 | **식단:** {latest['식단 철+비타민C']} | **카페인 섭취:** {latest['카페인 시간대']}")

    # AI 스타일 분석 요약
    st.markdown("---")
    st.subheader("🧠 AI 분석 요약")

    # 건강 조치 가이드 출력
    st.markdown("---")
    st.subheader("🩺 Hb 수치 기반 건강 조치 가이드")
    hb = latest["헤모글로빈"]
    sex = latest["성별"]
    if (sex == "남성" and hb < 13) or (sex == "여성" and hb < 12):
        st.error("""빈혈이 의심됩니다.

➡ 조치: 병원을 방문하여 혈액 검사와 철분 보충이 필요해요. 8g/dL 미만이면 응급 상황일 수 있습니다.""")
        st.markdown("""
        **생활관리:**
        - 철분이 풍부한 음식 + 비타민 C 과일 함께 섭취
        - 커피/차는 식후 2시간 후
        - 7–8시간 수면, 운동, 금연·절주, 수분 섭취

        **철분제 복용:**
        - 하루 100~200mg 요소철 기준 복용
        - 3개월 이상, 1개월 후 Hb 수치 재확인
        - 비타민 C와 함께, 칼슘 음식은 2시간 간격
        """)
    elif (sex == "남성" and hb >= 13 and hb <= 17) or (sex == "여성" and hb >= 12 and hb <= 15):
        st.success("정상 수치입니다. 건강 상태가 양호해요.")
        st.markdown("""
        **조치:** 연 1회 건강검진에서 체크해주면 충분해요.

        **생활관리:**
        - 철분뿐 아니라 비타민 B12, 엽산, A, C 등도 균형 있게 섭취
        - 규칙적인 수면, 운동, 수분 섭취 유지

        **철분제:** 복용 필요 없음. 식사로 하루 권장량 섭취 (남 8mg, 여 18mg)
        """)
    elif (sex == "남성" and hb > 17) or (sex == "여성" and hb > 15):
        st.warning("""헤모글로빈 수치가 높습니다.

➡ 조치: 운동 직후나 탈수에 의한 일시적 증가일 수 있으나, 지속되면 병원에서 다혈구증 여부를 검사하세요.""")
        st.markdown("""
        **생활관리:**
        - 물 충분히 마셔 혈액을 희석
        - 고단백·고칼로리 식단 조절
        - 흡연, 음주 피하기

        **철분제:** 복용 금지, 정기 모니터링 필요
        """)
    if len(user_data) >= 3:
        trend = user_data["헤모글로빈"].diff().tail(3)
        inc = trend.gt(0).sum()
        dec = trend.lt(0).sum()
        if inc >= 2:
            st.success("최근 3회 측정 결과에서 Hb 수치가 꾸준히 **상승 중**이에요. 식습관과 생활 습관을 잘 유지하고 있군요!")
        elif dec >= 2:
            st.warning("최근 3회 측정 결과에서 Hb 수치가 **감소 중**입니다. 수면, 식단, 카페인 섭취를 다시 점검해보는 것이 좋아요.")
        else:
            st.info("최근 Hb 수치가 큰 변화 없이 **안정적**이에요. 지금처럼 꾸준히 관리해보세요!")
    else:
        st.info("AI 분석은 최근 3회 이상의 기록이 있을 때 제공됩니다. 꾸준히 기록을 남겨주세요!")

    # 생활 요소별 비교 시각화
    st.markdown("---")
    st.subheader("📊 생활습관별 Hb 비교")
    compare_df = user_data.copy()

    if compare_df["식단 철+비타민C"].nunique() > 1:
        fig1 = px.strip(compare_df, x="식단 철+비타민C", y="헤모글로빈",
                        title="식단(철+비타민C 포함 여부)에 따른 Hb 점 분포",
                        labels={"헤모글로빈": "Hb 수치 (g/dL)", "식단 철+비타민C": "식단 여부"})
        fig1.update_traces(marker=dict(size=10, color="#1f77b4"))
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.warning("식단 데이터가 하나의 값만 있어 비교가 어렵습니다.")

    if compare_df["수면 시간"].nunique() > 1:
        compare_df["수면 시간"] = compare_df["수면 시간"].astype(int)
        fig2 = px.strip(compare_df, x="수면 시간", y="헤모글로빈",
                        title="수면 시간에 따른 Hb 점 분포",
                        labels={"헤모글로빈": "Hb 수치 (g/dL)", "수면 시간": "수면 (시간)"})
        fig2.update_traces(marker=dict(size=10, color="#2ca02c"))
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("수면 시간이 한 가지 값만 있어 비교할 수 없습니다.")

    if compare_df["카페인 시간대"].nunique() > 1:
        fig3 = px.strip(compare_df, x="카페인 시간대", y="헤모글로빈",
                        title="카페인 섭취 시점에 따른 Hb 점 분포",
                        labels={"헤모글로빈": "Hb 수치 (g/dL)", "카페인 시간대": "카페인 시점"})
        fig3.update_traces(marker=dict(size=10, color="#d62728"))
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.warning("카페인 섭취 시간대가 한 가지 값만 있어 비교할 수 없습니다.")

else:
    st.info("📂 아직 저장된 기록이 없습니다. 먼저 '기록 저장하기'를 통해 데이터를 입력해주세요!")
