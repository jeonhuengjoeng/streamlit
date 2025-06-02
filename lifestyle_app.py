import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib.patches import Circle
import matplotlib.patches as mpatches
import matplotlib.font_manager as fm

# 페이지 설정
st.set_page_config(page_title="🌟 Life Tracker", layout="wide")

# 한글 폰트 설정
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# 커스텀 CSS로 깔끔한 흰색 배경
st.markdown("""
<style>
    .main {
        background-color: white;
        color: #2C3E50;
    }
    .stApp {
        background-color: white;
    }
    h1 {
        text-align: center;
        font-size: 3rem;
        margin-bottom: 2rem;
        color: #2C3E50;
    }
    .metric-container {
        background-color: #F8F9FA;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# 데이터 준비
data = {
    'date': ['2025-01-01', '2025-01-02', '2025-01-03'],
    'sleep': [4, 6, 5],
    'study': [5, 3, 6],
    'exercise': [0, 0, 0],
    'mood': ['Good', 'Normal', 'Bad']
}
df = pd.DataFrame(data)

# 메인 타이틀
st.markdown("# 🌟 Life Tracker Dashboard")

# 3개 컬럼으로 레이아웃
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # 기분 분포 도넛 차트
    fig1, ax1 = plt.subplots(figsize=(10, 8), facecolor='white')
    
    mood_counts = df['mood'].value_counts()
    # 파스텔 톤 컬러
    colors = ['#FFB3BA', '#BAFFC9', '#BAE1FF']  # 파스텔 핑크, 민트, 블루
    
    # 도넛 차트 생성
    wedges, texts, autotexts = ax1.pie(mood_counts.values, 
                                      labels=['Good', 'Normal', 'Bad'],
                                      colors=colors,
                                      autopct='%1.0f%%',
                                      startangle=90,
                                      pctdistance=0.85,
                                      wedgeprops=dict(width=0.5, edgecolor='white', linewidth=3))
    
    # 가운데 원 추가 (도넛 효과)
    centre_circle = Circle((0,0), 0.50, fc='white', alpha=1)
    ax1.add_artist(centre_circle)
    
    # 스타일링
    ax1.set_title('Mood Distribution', fontsize=24, fontweight='bold', pad=30, color='#2C3E50')
    
    # 텍스트 스타일링
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(14)
        autotext.set_fontweight('bold')
    
    for text in texts:
        text.set_fontsize(16)
        text.set_fontweight('bold')
        text.set_color('#2C3E50')
    
    ax1.set_facecolor('white')
    fig1.patch.set_facecolor('white')
    
    st.pyplot(fig1)

# 시간 사용 패턴 차트
st.markdown("## ⏰ Time Usage Pattern")

col1, col2 = st.columns(2)

with col1:
    # 수면시간 트렌드
    fig2, ax2 = plt.subplots(figsize=(8, 6), facecolor='white')
    
    dates = pd.to_datetime(df['date'])
    sleep_hours = df['sleep']
    
    # 파스텔 라인 차트
    ax2.plot(dates, sleep_hours, color='#FFB3E6', linewidth=4, marker='o', 
             markersize=12, markerfacecolor='white', markeredgecolor='#FFB3E6', 
             markeredgewidth=3)
    
    # 배경 그라데이션
    ax2.fill_between(dates, sleep_hours, alpha=0.3, color='#FFB3E6')
    
    ax2.set_title('Sleep Hours Trend', fontsize=18, fontweight='bold', color='#2C3E50', pad=20)
    ax2.set_ylabel('Hours', fontsize=14, color='#2C3E50')
    ax2.grid(True, alpha=0.3, color='#E8E8E8')
    ax2.set_facecolor('white')
    
    # 축 스타일링
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_color('#CCCCCC')
    ax2.spines['bottom'].set_color('#CCCCCC')
    ax2.tick_params(colors='#666666')
    
    fig2.patch.set_facecolor('white')
    st.pyplot(fig2)

with col2:
    # 공부시간 바 차트
    fig3, ax3 = plt.subplots(figsize=(8, 6), facecolor='white')
    
    study_hours = df['study']
    
    # 파스텔 바 차트
    bars = ax3.bar(range(len(dates)), study_hours, 
                   color=['#B3E5FC', '#C8E6C9', '#F8BBD9'], 
                   alpha=0.8, edgecolor='white', linewidth=2)
    
    # 바 위에 값 표시
    for i, v in enumerate(study_hours):
        ax3.text(i, v + 0.1, str(v) + 'h', ha='center', va='bottom', 
                fontweight='bold', fontsize=12, color='#2C3E50')
    
    ax3.set_title('Study Hours Distribution', fontsize=18, fontweight='bold', color='#2C3E50', pad=20)
    ax3.set_ylabel('Hours', fontsize=14, color='#2C3E50')
    ax3.set_xticks(range(len(dates)))
    ax3.set_xticklabels([d.strftime('%m/%d') for d in dates])
    ax3.grid(True, alpha=0.3, axis='y', color='#E8E8E8')
    ax3.set_facecolor('white')
    
    # 축 스타일링
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    ax3.spines['left'].set_color('#CCCCCC')
    ax3.spines['bottom'].set_color('#CCCCCC')
    ax3.tick_params(colors='#666666')
    
    fig3.patch.set_facecolor('white')
    st.pyplot(fig3)

# 종합 히트맵
st.markdown("## 🔥 Comprehensive Activity Heatmap")

# 히트맵용 데이터 준비
heatmap_data = df[['sleep', 'study', 'exercise']].T
heatmap_data.columns = [f"Day {i+1}" for i in range(len(df))]
heatmap_data.index = ['Sleep', 'Study', 'Exercise']

fig4, ax4 = plt.subplots(figsize=(12, 6), facecolor='white')

# 파스텔 컬러맵
colors = ['#FFFFFF', '#FFE4E1', '#FFB6C1', '#FFA0B4']
cmap = sns.blend_palette(colors, as_cmap=True)

# 히트맵 생성
sns.heatmap(heatmap_data, annot=True, fmt='d', cmap=cmap, 
            cbar_kws={'label': 'Hours'}, ax=ax4,
            linewidths=2, linecolor='white', square=True)

ax4.set_title('Daily Activity Pattern', fontsize=20, fontweight='bold', color='#2C3E50', pad=20)
ax4.set_ylabel('Activity Type', fontsize=14, color='#2C3E50')
ax4.set_xlabel('Date', fontsize=14, color='#2C3E50')

# 축 레이블 스타일링
ax4.tick_params(colors='#2C3E50')
ax4.set_facecolor('white')

fig4.patch.set_facecolor('white')
st.pyplot(fig4)

# 통계 요약
st.markdown("## 📈 Key Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_sleep = df['sleep'].mean()
    st.metric("Average Sleep", f"{avg_sleep:.1f}h", delta=f"{avg_sleep-6:.1f}h")

with col2:
    avg_study = df['study'].mean()
    st.metric("Average Study", f"{avg_study:.1f}h", delta=f"{avg_study-4:.1f}h")

with col3:
    total_exercise = df['exercise'].sum()
    st.metric("Total Exercise", f"{total_exercise}h", delta="Need Exercise!")

with col4:
    good_mood_ratio = (df['mood'] == 'Good').sum() / len(df) * 100
    st.metric("Good Mood Ratio", f"{good_mood_ratio:.0f}%", delta=f"{good_mood_ratio-50:.0f}%")

# 추천사항
st.markdown("## 💡 Improvement Suggestions")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("🌙 Try to get 7-8 hours of sleep!")

with col2:
    st.warning("🏃‍♂️ How about adding some exercise time?")

with col3:
    st.success("📚 Great consistent study pattern!")
