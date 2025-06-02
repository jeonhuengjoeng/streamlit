import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="나의 생활패턴 분석기", layout="wide")

st.title("📊 나의 생활패턴 분석기")

uploaded_file = st.file_uploader("./data/lifestyle_100_utf8.csv", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("✅ 데이터 미리보기")
    st.dataframe(df)

    st.subheader("📈 평균 생활 시간")
    avg_sleep = df['수면시간'].mean()
    avg_study = df['공부시간'].mean()
    avg_exercise = df['운동시간'].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("🛌 평균 수면시간", f"{avg_sleep:.1f}시간")
    col2.metric("📚 평균 공부시간", f"{avg_study:.1f}시간")
    col3.metric("💪 평균 운동시간", f"{avg_exercise:.1f}시간")

    st.subheader("📊 활동 시간 그래프")
    fig, ax = plt.subplots()
    df[['수면시간', '공부시간', '운동시간']].plot(kind='bar', ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.subheader("😊 기분 분포")
    mood_counts = df['기분'].value_counts()
    st.bar_chart(mood_counts)
else:
    st.info("⬆ 먼저 CSV 파일을 업로드해주세요!")
