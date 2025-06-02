import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib.patches import Circle
import matplotlib.patches as mpatches

# 페이지 설정
st.set_page_config(page_title="🌟 Life Tracker", layout="wide")

# 커스텀 CSS로 배경과 스타일링
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    .stApp {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    h1 {
        text-align: center;
        font-size: 3rem;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# 데이터 준비
data = {
    '날짜': ['2025-01-01', '2025-01-02', '2025-01-03'],
    '수면시간': [4, 6, 5],
    '공부시간': [5, 3, 6],
    '운동시간': [0, 0, 0],
    '기분': ['좋음', '보통', '나쁨']
}
df = pd.DataFrame(data)

# 메인 타이틀
st.markdown("# 🌟 Life Tracker Dashboard")

# 3개 컬럼으로 레이아웃
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # 기분 분포 도넛 차트
    fig1, ax1 = plt.subplots(figsize=(10, 8), facecolor='none')
    
    mood_counts = df['기분'].value_counts()
    colors = ['#FF6B9D', '#45B7D1', '#96CEB4']  # 핑크, 블루, 민트
    
    # 도넛 차트 생성
    wedges, texts, autotexts = ax1.pie(mood_counts.values, 
                                      labels=mood_counts.index,
                                      colors=colors,
                                      autopct='%1.0f%%',
                                      startangle=90,
                                      pctdistance=0.85,
                                      wedgeprops=dict(width=0.5, edgecolor='white', linewidth=3))
    
    # 가운데 원 추가 (도넛 효과)
    centre_circle = Circle((0,0), 0.50, fc='white', alpha=0.8)
    ax1.add_artist(centre_circle)
    
    # 스타일링
    ax1.set_title('😊 기분 분포', fontsize=24, fontweight='bold', pad=30, color='#2C3E50')
    
    # 텍스트 스타일링
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(14)
        autotext.set_fontweight('bold')
    
    for text in texts:
        text.set_fontsize(16)
        text.set_fontweight('bold')
        text.set_color('#2C3E50')
    
    ax1.set_facecolor('none')
    fig1.patch.set_alpha(0.0)
    
    st.pyplot(fig1)

# 시간 사용 패턴 차트
st.markdown("## ⏰ 시간 사용 패턴")

col1, col2 = st.columns(2)

with col1:
    # 수면시간 트렌드
    fig2, ax2 = plt.subplots(figsize=(8, 6), facecolor='none')
    
    dates = pd.to_datetime(df['날짜'])
    sleep_hours = df['수면시간']
    
    # 그라데이션 라인 차트
    ax2.plot(dates, sleep_hours, color='#FF6B9D', linewidth=4, marker='o', 
             markersize=12, markerfacecolor='white', markeredgecolor='#FF6B9D', 
             markeredgewidth=3)
    
    # 배경 그라데이션
    ax2.fill_between(dates, sleep_hours, alpha=0.3, color='#FF6B9D')
    
    ax2.set_title('💤 수면시간 변화', fontsize=18, fontweight='bold', color='#2C3E50', pad=20)
    ax2.set_ylabel('시간', fontsize=14, color='#2C3E50')
    ax2.grid(True, alpha=0.3)
    ax2.set_facecolor('none')
    
    # 축 스타일링
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_color('#2C3E50')
    ax2.spines['bottom'].set_color('#2C3E50')
    
    fig2.patch.set_alpha(0.0)
    st.pyplot(fig2)

with col2:
    # 공부시간 바 차트
    fig3, ax3 = plt.subplots(figsize=(8, 6), facecolor='none')
    
    study_hours = df['공부시간']
    
    # 그라데이션 바 차트
    bars = ax3.bar(range(len(dates)), study_hours, 
                   color=['#45B7D1', '#4ECDC4', '#44A08D'], 
                   alpha=0.8, edgecolor='white', linewidth=2)
    
    # 바 위에 값 표시
    for i, v in enumerate(study_hours):
        ax3.text(i, v + 0.1, str(v) + 'h', ha='center', va='bottom', 
                fontweight='bold', fontsize=12, color='#2C3E50')
    
    ax3.set_title('📚 공부시간 분포', fontsize=18, fontweight='bold', color='#2C3E50', pad=20)
    ax3.set_ylabel('시간', fontsize=14, color='#2C3E50')
    ax3.set_xticks(range(len(dates)))
    ax3.set_xticklabels([d.strftime('%m/%d') for d in dates])
    ax3.grid(True, alpha=0.3, axis='y')
    ax3.set_facecolor('none')
    
    # 축 스타일링
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    ax3.spines['left'].set_color('#2C3E50')
    ax3.spines['bottom'].set_color('#2C3E50')
    
    fig3.patch.set_alpha(0.0)
    st.pyplot(fig3)

# 종합 히트맵
st.markdown("## 🔥 종합 활동 히트맵")

# 히트맵용 데이터 준비
heatmap_data = df[['수면시간', '공부시간', '운동시간']].T
heatmap_data.columns = [f"Day {i+1}" for i in range(len(df))]

fig4, ax4 = plt.subplots(figsize=(12, 6), facecolor='none')

# 커스텀 컬러맵
cmap = sns.blend_palette(['#FF6B9D', '#45B7D1', '#96CEB4'], as_cmap=True)

# 히트맵 생성
sns.heatmap(heatmap_data, annot=True, fmt='d', cmap=cmap, 
            cbar_kws={'label': '시간 (hours)'}, ax=ax4,
            linewidths=2, linecolor='white', square=True)

ax4.set_title('📊 일별 활동 패턴', fontsize=20, fontweight='bold', color='#2C3E50', pad=20)
ax4.set_ylabel('활동 유형', fontsize=14, color='#2C3E50')
ax4.set_xlabel('날짜', fontsize=14, color='#2C3E50')

# 축 레이블 스타일링
ax4.tick_params(colors='#2C3E50')
ax4.set_facecolor('none')

fig4.patch.set_alpha(0.0)
st.pyplot(fig4)

# 통계 요약
st.markdown("## 📈 주요 통계")

col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_sleep = df['수면시간'].mean()
    st.metric("평균 수면시간", f"{avg_sleep:.1f}시간", delta=f"{avg_sleep-6:.1f}h")

with col2:
    avg_study = df['공부시간'].mean()
    st.metric("평균 공부시간", f"{avg_study:.1f}시간", delta=f"{avg_study-4:.1f}h")

with col3:
    total_exercise = df['운동시간'].sum()
    st.metric("총 운동시간", f"{total_exercise}시간", delta="운동 필요!")

with col4:
    good_mood_ratio = (df['기분'] == '좋음').sum() / len(df) * 100
    st.metric("좋은 기분 비율", f"{good_mood_ratio:.0f}%", delta=f"{good_mood_ratio-50:.0f}%")

# 추천사항
st.markdown("## 💡 개선 제안")
st.info("🌙 수면시간을 7-8시간으로 늘려보세요!")
st.warning("🏃‍♂️ 운동시간을 추가해보시는 것은 어떨까요?")
st.success("📚 꾸준한 공부 패턴이 좋습니다!")
