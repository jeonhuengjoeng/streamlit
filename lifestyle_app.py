import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib.patches import Circle
import matplotlib.patches as mpatches
import platform

# 페이지 설정
st.set_page_config(page_title="🌟 라이프 트래커", layout="wide")

# 로컬 한글 폰트 설정
def set_korean_font():
    import matplotlib.font_manager as fm
    import os
    
    try:
        # 로컬 폰트 파일 경로
        font_path = './fonts/NanumGothic.ttf'
        
        # 폰트 파일이 존재하는지 확인
        if os.path.exists(font_path):
            # 폰트 등록
            fm.fontManager.addfont(font_path)
            
            # 폰트 이름으로 설정 (나눔고딕)
            plt.rcParams['font.family'] = 'NanumGothic'
            print(f"✅ 로컬 한글 폰트 설정 완료: {font_path}")
            
        else:
            print(f"❌ 폰트 파일을 찾을 수 없습니다: {font_path}")
            # 폴백: 시스템 한글 폰트 시도
            korean_fonts = ['Malgun Gothic', 'AppleGothic', 'NanumGothic', 'DejaVu Sans']
            available_fonts = [f.name for f in fm.fontManager.ttflist]
            
            for font in korean_fonts:
                if font in available_fonts:
                    plt.rcParams['font.family'] = font
                    print(f"🔄 시스템 폰트 사용: {font}")
                    break
    
    except Exception as e:
        print(f"⚠️ 폰트 설정 중 오류 발생: {e}")
        plt.rcParams['font.family'] = 'DejaVu Sans'
    
    # 마이너스 기호 깨짐 방지
    plt.rcParams['axes.unicode_minus'] = False
    
    # 한글 폰트 설정 확인
    current_font = plt.rcParams['font.family']
    print(f"📝 현재 사용 중인 폰트: {current_font}")

set_korean_font()

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
    '날짜': ['2025-01-01', '2025-01-02', '2025-01-03'],
    '수면시간': [4, 6, 5],
    '공부시간': [5, 3, 6],
    '운동시간': [0, 0, 0],
    '기분': ['좋음', '보통', '나쁨']
}
df = pd.DataFrame(data)

# 메인 타이틀
st.markdown("# 🌟 라이프 트래커 대시보드")

# 3개 컬럼으로 레이아웃
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # 기분 분포 도넛 차트
    fig1, ax1 = plt.subplots(figsize=(10, 8), facecolor='white')
    
    mood_counts = df['기분'].value_counts()
    # 파스텔 톤 컬러
    colors = ['#FFB3BA', '#BAFFC9', '#BAE1FF']  # 파스텔 핑크, 민트, 블루
    
    # 도넛 차트 생성
    wedges, texts, autotexts = ax1.pie(mood_counts.values, 
                                      labels=mood_counts.index,
                                      colors=colors,
                                      autopct='%1.0f%%',
                                      startangle=90,
                                      pctdistance=0.85,
                                      wedgeprops=dict(width=0.5, edgecolor='white', linewidth=3))
    
    # 가운데 원 추가 (도넛 효과)
    centre_circle = Circle((0,0), 0.50, fc='white', alpha=1)
    ax1.add_artist(centre_circle)
    
    # 스타일링 - 명시적으로 폰트 설정
    ax1.set_title('😊 기분 분포', fontsize=24, fontweight='bold', pad=30, color='#2C3E50', fontfamily='DejaVu Sans')
    
    # 텍스트 스타일링 - 각 텍스트에 폰트 명시
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(14)
        autotext.set_fontweight('bold')
        autotext.set_fontfamily('DejaVu Sans')
    
    for text in texts:
        text.set_fontsize(16)
        text.set_fontweight('bold')
        text.set_color('#2C3E50')
        text.set_fontfamily('DejaVu Sans')
    
    ax1.set_facecolor('white')
    fig1.patch.set_facecolor('white')
    
    st.pyplot(fig1)

# 시간 사용 패턴 차트
st.markdown("## ⏰ 시간 사용 패턴")

col1, col2 = st.columns(2)

with col1:
    # 수면시간 트렌드
    fig2, ax2 = plt.subplots(figsize=(8, 6), facecolor='white')
    
    dates = pd.to_datetime(df['날짜'])
    sleep_hours = df['수면시간']
    
    # 파스텔 라인 차트
    ax2.plot(dates, sleep_hours, color='#FFB3E6', linewidth=4, marker='o', 
             markersize=12, markerfacecolor='white', markeredgecolor='#FFB3E6', 
             markeredgewidth=3)
    
    # 배경 그라데이션
    ax2.fill_between(dates, sleep_hours, alpha=0.3, color='#FFB3E6')
    
    ax2.set_title('💤 수면시간 변화', fontsize=18, fontweight='bold', color='#2C3E50', pad=20, fontfamily='DejaVu Sans')
    ax2.set_ylabel('시간', fontsize=14, color='#2C3E50', fontfamily='DejaVu Sans')
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
    
    study_hours = df['공부시간']
    
    # 파스텔 바 차트
    bars = ax3.bar(range(len(dates)), study_hours, 
                   color=['#B3E5FC', '#C8E6C9', '#F8BBD9'], 
                   alpha=0.8, edgecolor='white', linewidth=2)
    
    # 바 위에 값 표시
    for i, v in enumerate(study_hours):
        ax3.text(i, v + 0.1, str(v) + '시간', ha='center', va='bottom', 
                fontweight='bold', fontsize=12, color='#2C3E50')
    
    ax3.set_title('📚 공부시간 분포', fontsize=18, fontweight='bold', color='#2C3E50', pad=20, fontfamily='DejaVu Sans')
    ax3.set_ylabel('시간', fontsize=14, color='#2C3E50', fontfamily='DejaVu Sans')
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
st.markdown("## 🔥 종합 활동 히트맵")

# 히트맵용 데이터 준비
heatmap_data = df[['수면시간', '공부시간', '운동시간']].T
heatmap_data.columns = [f"{i+1}일차" for i in range(len(df))]

fig4, ax4 = plt.subplots(figsize=(12, 6), facecolor='white')

# 파스텔 컬러맵
colors = ['#FFFFFF', '#FFE4E1', '#FFB6C1', '#FFA0B4']
cmap = sns.blend_palette(colors, as_cmap=True)

# 히트맵 생성
sns.heatmap(heatmap_data, annot=True, fmt='d', cmap=cmap, 
            cbar_kws={'label': '시간 (hours)'}, ax=ax4,
            linewidths=2, linecolor='white', square=True)

ax4.set_title('📊 일별 활동 패턴', fontsize=20, fontweight='bold', color='#2C3E50', pad=20, fontfamily='DejaVu Sans')
ax4.set_ylabel('활동 유형', fontsize=14, color='#2C3E50', fontfamily='DejaVu Sans')
ax4.set_xlabel('날짜', fontsize=14, color='#2C3E50', fontfamily='DejaVu Sans')

# 축 레이블 스타일링
ax4.tick_params(colors='#2C3E50')
ax4.set_facecolor('white')

fig4.patch.set_facecolor('white')
st.pyplot(fig4)

# 통계 요약
st.markdown("## 📈 주요 통계")

col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_sleep = df['수면시간'].mean()
    st.metric("평균 수면시간", f"{avg_sleep:.1f}시간", delta=f"{avg_sleep-6:.1f}시간")

with col2:
    avg_study = df['공부시간'].mean()
    st.metric("평균 공부시간", f"{avg_study:.1f}시간", delta=f"{avg_study-4:.1f}시간")

with col3:
    total_exercise = df['운동시간'].sum()
    st.metric("총 운동시간", f"{total_exercise}시간", delta="운동 필요!")

with col4:
    good_mood_ratio = (df['기분'] == '좋음').sum() / len(df) * 100
    st.metric("좋은 기분 비율", f"{good_mood_ratio:.0f}%", delta=f"{good_mood_ratio-50:.0f}%")

# 추천사항
st.markdown("## 💡 개선 제안")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("🌙 수면시간을 7-8시간으로 늘려보세요!")

with col2:
    st.warning("🏃‍♂️ 운동시간을 추가해보시는 것은 어떨까요?")

with col3:
    st.success("📚 꾸준한 공부 패턴이 좋습니다!")
