import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib

st.set_page_config(
    page_title="카페인이 헤모글로빈에 주는 영향 분석",
    page_icon="☕",
    layout="centered"
)
st.markdown("<div style='max-width: 900px; margin: auto;'>", unsafe_allow_html=True)
st.title("💉 헤모글로빈 농도 변화 분석")

uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요", type=["xlsx"])

if uploaded_file:
    excel_file = pd.ExcelFile(uploaded_file)
    data_frames = {}
    for sheet in excel_file.sheet_names:
        df = excel_file.parse(sheet, header=5)
        df = df.rename(columns=lambda x: str(x).strip())
        df['회차'] = sheet.split()[-1]
        data_frames[sheet] = df

    data = pd.concat(data_frames.values(), ignore_index=True)

    data = data[['이름', '헤모글로빈 농도 측정 값', '실험 전 \n카페인 섭취 여부', '실험 후 \n카페인 섭취 여부', '철분제 섭취 여부\n(4월 9일 부터)', '회차']]
    data.columns = ['이름', '헤모글로빈', '실험전 카페인', '실험후 카페인', '철분제 섭취', '회차']

    data['이름'] = data['이름'].astype(str)
    data['헤모글로빈'] = pd.to_numeric(data['헤모글로빈'], errors='coerce')

    tab1, tab2 = st.tabs(["📈 개인별 변화", "📊 조건별 평균"])

    with tab1:
        st.header("📌 학생별 헤모글로빈 농도 변화 추이")
        selected_name = st.selectbox("학생을 선택하세요:", sorted(data['이름'].dropna().unique()))
        student_data = data[data['이름'] == selected_name].sort_values('회차')

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=student_data['회차'],
            y=student_data['헤모글로빈'],
            mode='lines+markers+text',
            line=dict(color='royalblue', width=2),
            marker=dict(size=6),
            text=[f"{y:.2f}" for y in student_data['헤모글로빈']],
            textposition="top center",
            name=f"{selected_name}"
        ))
        fig.update_layout(
            title=f"{selected_name}님의 헤모글로빈 농도 변화",
            xaxis_title="측정 회차",
            yaxis_title="헤모글로빈 농도 (g/dL)",
            height=300,
            margin=dict(l=20, r=20, t=40, b=20),
            template='plotly_white',
            font=dict(size=12)
        )
        st.plotly_chart(fig, use_container_width=True)

        latest = student_data.iloc[-1]
        st.markdown("### 📝 실험 정보")
        col1, col2, col3 = st.columns(3)
        col1.metric("실험 전 카페인", latest['실험전 카페인'])
        col2.metric("실험 후 카페인", latest['실험후 카페인'])
        col3.metric("철분제 섭취", latest['철분제 섭취'])

    with tab2:
        st.header("⚙️ 조건별 평균 헤모글로빈 농도")
        col1, col2, col3 = st.columns(3)
        selected_pre = col1.selectbox("실험 전 카페인", ['O', 'X'])
        selected_post = col2.selectbox("실험 후 카페인", ['O', 'X'])
        selected_iron = col3.selectbox("철분제 섭취", ['O', 'X'])

        filtered = data[
            (data['실험전 카페인'] == selected_pre) &
            (data['실험후 카페인'] == selected_post) &
            (data['철분제 섭취'] == selected_iron)
        ]

        avg_data = filtered.groupby('회차')['헤모글로빈'].mean().reset_index()

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=avg_data['회차'],
            y=avg_data['헤모글로빈'],
            mode='lines+markers+text',
            line=dict(color='royalblue', width=2),
            marker=dict(size=6),
            text=[f"{y:.2f}" for y in avg_data['헤모글로빈']],
            textposition="top center",
            name="평균 헤모글로빈"
        ))
        fig2.update_layout(
            title="조건별 평균 헤모글로빈 농도 변화",
            xaxis_title="측정 회차",
            yaxis_title="평균 헤모글로빈 농도 (g/dL)",
            height=300,
            margin=dict(l=20, r=20, t=40, b=20),
            template='plotly_white',
            font=dict(size=12)
        )
        st.plotly_chart(fig2, use_container_width=True)

else:
    st.info("좌측 상단에서 엑셀 파일(.xlsx)을 업로드해주세요.")

st.markdown("</div>", unsafe_allow_html=True)
