import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib.patches import Circle
import matplotlib.patches as mpatches
import matplotlib.font_manager as fm
import os

# 페이지 설정
st.set_page_config(page_title="🌟 라이프 트래커", layout="wide")

# 로컬 나눔고딕 폰트 설정 (GitHub Streamlit용)
@st.cache_resource
def setup_korean_font():
    """로컬 나눔고딕 폰트를 등록하고 설정"""
    try:
        # 현재 파일 위치 기준 폰트 경로
        current_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
        font_path = os.path.join(current_dir, 'fonts', 'NanumGothic.ttf')
        
        # 폰트 파일 존재 확인
        if os.path.exists(font_path):
            # matplotlib 폰트 매니저에 폰트 추가
            fm.fontManager.addfont(font_path)
            
            # 나눔고딕을 기본 폰트로 설정
            plt.rcParams['font.family'] = ['NanumGothic', 'sans-serif']
            plt.rcParams['font.size'] = 10
            plt.rcParams['axes.labelsize'] = 12
            plt.rcParams['axes.titlesize'] = 14
            plt.rcParams['xtick.labelsize'] = 10
            plt.rcParams['ytick.labelsize'] = 10
            plt.rcParams['legend.fontsize'] = 10
            plt.rcParams['figure.titlesize'] = 16
            
            # 한글 관련 설정
            plt.rcParams['axes.unicode_minus'] = False
            
            # 선명도 향상을 위한 DPI 설정
            plt.rcParams['figure.dpi'] = 100
            plt.rcParams['savefig.dpi'] = 100
            
            return True
            
        else:
            st.error(f"❌ 폰트 파일을 찾을 수 없습니다: {font_path}")
            # 폴백 설정
            plt.rcParams['font.family'] = ['DejaVu Sans', 'sans-serif']
            plt.rcParams['axes.unicode_minus'] = False
            return False
            
    except Exception as e:
        st.error(f"⚠️ 폰트 설정 오류: {e}")
        plt.rcParams['font.family'] = ['DejaVu Sans', 'sans-serif']
        plt.rcParams['axes.unicode_minus'] = False
        return False

# 폰트 설정 실행
font_loaded = setup_korean_font()

# 커스텀 CSS로 깔끔한 흰색 배경과 선명한 텍스트
st.markdown("""
<style>
    .main {
        background-color: white;
        color: #2C3E50;
    }
    .stApp {
        background-color: white;
    }
    /* 제목들을 매우 선명하고 굵게 */
    h1 {
        color: #2C3E50 !important;
        font-weight: 900 !important;
        font-size: 3.5rem !important;
        text-align: center !important;
        margin-bottom: 2rem !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1) !important;
        -webkit-font-smoothing: antialiased !important;
        -moz-osx-font-smoothing: grayscale !important;
    }
    h2 {
        color: #2C3E50 !important;
        font-weight: 800 !important;
        font-size: 2.2rem !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1) !important;
        -webkit-font-smoothing: antialiased !important;
        -moz-osx-font-smoothing: grayscale !important;
    }
    h3 {
        color: #2C3E50 !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
        -webkit-font-smoothing: antialiased !important;
        -moz-osx-font-smoothing: grayscale !important;
    }
    .metric-container {
        background-color: #F8F9FA;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    /* 모든 텍스트 선명도 향상 */
    * {
        -webkit-font-smoothing: antialiased !important;
        -moz-osx-font-smoothing: grayscale !important;
        text-rendering: optimizeLegibility !important;
    }
    /* Streamlit 기본 제목 스타일 오버라이드 */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        font-family: 'NanumGothic', sans-serif !important;
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

# 메인 타이틀 - HTML로 더 선명하게
st.markdown("""
<h1 style='
    text-align: center; 
    color: #2C3E50; 
    font-weight: 900; 
    font-size: 3.5rem; 
    margin-bottom: 2rem;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    font-family: NanumGothic, sans-serif;
'>🌟 라이프 트래커 대시보드</h1>
""", unsafe_allow_html=True)

if not font_loaded:
    st.warning("⚠️ 나눔고딕 폰트를 로드할 수 없어 기본 폰트를 사용합니다. fonts/NanumGothic.ttf 파일을 확인해주세요.")

# 3개 컬럼으로 레이아웃
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # 기분 분포 도넛 차트
    fig1, ax1 = plt.subplots(figsize=(10, 8), facecolor='white', dpi=100)
    
    mood_counts = df['기분'].value_counts()
    # 파스텔 톤 컬러 (선명하게)
    colors = ['#FF9AA2', '#B5EAD7', '#A8E6CF']  # 더 선명한 파스텔
    
    # 도넛 차트 생성
    wedges, texts, autotexts = ax1.pie(mood_counts.values, 
                                      labels=mood_counts.index,
                                      colors=colors,
                                      autopct='%1.0f%%',
                                      startangle=90,
                                      pctdistance=0.85,
                                      wedgeprops=dict(width=0.5, edgecolor='white', linewidth=3),
                                      textprops={'fontweight': 'bold', 'fontsize': 14})
    
    # 가운데 원 추가 (도넛 효과)
    centre_circle = Circle((0,0), 0.50, fc='white', alpha=1)
    ax1.add_artist(centre_circle)
    
    # 제목 설정 (선명하게)
    ax1.set_title('😊 기분 분포', fontsize=26, fontweight='bold', pad=30, color='#2C3E50')
    
    # 텍스트 스타일링 (선명도 향상)
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(16)
        autotext.set_fontweight('bold')
    
    for text in texts:
        text.set_fontsize(18)
        text.set_fontweight('bold')
        text.set_color('#2C3E50')
    
    ax1.set_facecolor('white')
    fig1.patch.set_facecolor('white')
    
    st.pyplot(fig1, use_container_width=True)

# 시간 사용 패턴 차트 - HTML로 더 선명하게
st.markdown("""
<h2 style='
    color: #2C3E50; 
    font-weight: 800; 
    font-size: 2.2rem; 
    margin-top: 2rem; 
    margin-bottom: 1rem;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    font-family: NanumGothic, sans-serif;
'>⏰ 시간 사용 패턴</h2>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # 수면시간 트렌드
    fig2, ax2 = plt.subplots(figsize=(8, 6), facecolor='white', dpi=100)
    
    dates = pd.to_datetime(df['날짜'])
    sleep_hours = df['수면시간']
    
    # 선명한 파스텔 라인 차트
    ax2.plot(dates, sleep_hours, color='#FF6B9D', linewidth=5, marker='o', 
             markersize=15, markerfacecolor='white', markeredgecolor='#FF6B9D', 
             markeredgewidth=4)
    
    # 배경 그라데이션
    ax2.fill_between(dates, sleep_hours, alpha=0.3, color='#FF6B9D')
    
    ax2.set_title('수면시간 변화', fontsize=20, fontweight='bold', color='#2C3E50', pad=20)
    ax2.set_ylabel('시간', fontsize=16, color='#2C3E50', fontweight='bold')
    ax2.grid(True, alpha=0.3, color='#E8E8E8', linewidth=1)
    ax2.set_facecolor('white')
    
    # 축 스타일링 (선명하게)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_color('#CCCCCC')
    ax2.spines['bottom'].set_color('#CCCCCC')
    ax2.tick_params(colors='#666666', labelsize=12)
    
    fig2.patch.set_facecolor('white')
    st.pyplot(fig2, use_container_width=True)

with col2:
    # 공부시간 바 차트
    fig3, ax3 = plt.subplots(figsize=(8, 6), facecolor='white', dpi=100)
    
    study_hours = df['공부시간']
    
    # 선명한 파스텔 바 차트
    bars = ax3.bar(range(len(dates)), study_hours, 
                   color=['#45B7D1', '#96CEB4', '#FFEAA7'], 
                   alpha=0.9, edgecolor='white', linewidth=3)
    
    # 바 위에 값 표시 (선명하게)
    for i, v in enumerate(study_hours):
        ax3.text(i, v + 0.1, str(v) + '시간', ha='center', va='bottom', 
                fontweight='bold', fontsize=14, color='#2C3E50')
    
    ax3.set_title('📚 공부시간 분포', fontsize=20, fontweight='bold', color='#2C3E50', pad=20)
    ax3.set_ylabel('시간', fontsize=16, color='#2C3E50', fontweight='bold')
    ax3.set_xticks(range(len(dates)))
    ax3.set_xticklabels([d.strftime('%m/%d') for d in dates], fontsize=12, fontweight='bold')
    ax3.grid(True, alpha=0.3, axis='y', color='#E8E8E8', linewidth=1)
    ax3.set_facecolor('white')
    
    # 축 스타일링 (선명하게)
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    ax3.spines['left'].set_color('#CCCCCC')
    ax3.spines['bottom'].set_color('#CCCCCC')
    ax3.tick_params(colors='#666666', labelsize=12)
    
    fig3.patch.set_facecolor('white')
    st.pyplot(fig3, use_container_width=True)

# 종합 히트맵 - HTML로 더 선명하게
st.markdown("""
<h2 style='
    color: #2C3E50; 
    font-weight: 800; 
    font-size: 2.2rem; 
    margin-top: 2rem; 
    margin-bottom: 1rem;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    font-family: NanumGothic, sans-serif;
'>🔥 종합 활동 히트맵</h2>
""", unsafe_allow_html=True)

# 히트맵용 데이터 준비
heatmap_data = df[['수면시간', '공부시간', '운동시간']].T
heatmap_data.columns = [f"{i+1}일차" for i in range(len(df))]

fig4, ax4 = plt.subplots(figsize=(12, 6), facecolor='white', dpi=100)

# 선명한 파스텔 컬러맵
colors = ['#FFFFFF', '#FFE4E6', '#FFB8BB', '#FF8A90']
cmap = sns.blend_palette(colors, as_cmap=True)

# 히트맵 생성 (선명한 설정)
sns.heatmap(heatmap_data, annot=True, fmt='d', cmap=cmap, 
            cbar_kws={'label': '시간 (hours)'}, ax=ax4,
            linewidths=3, linecolor='white', square=True,
            annot_kws={'fontsize': 14, 'fontweight': 'bold'})

ax4.set_title(' 일별 활동 패턴', fontsize=22, fontweight='bold', color='#2C3E50', pad=20)
ax4.set_ylabel('활동 유형', fontsize=16, color='#2C3E50', fontweight='bold')
ax4.set_xlabel('날짜', fontsize=16, color='#2C3E50', fontweight='bold')

# 축 레이블 스타일링 (선명하게)
ax4.tick_params(colors='#2C3E50', labelsize=12)
ax4.set_facecolor('white')

fig4.patch.set_facecolor('white')
st.pyplot(fig4, use_container_width=True)

# 통계 요약 - 2x2 레이아웃으로 변경
st.markdown("""
<h2 style='
    color: #2C3E50; 
    font-weight: 800; 
    font-size: 2.2rem; 
    margin-top: 2rem; 
    margin-bottom: 1rem;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    font-family: NanumGothic, sans-serif;
'>📈 주요 통계</h2>
""", unsafe_allow_html=True)

# 2x2 그리드 레이아웃
row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)

with row1_col1:
    avg_sleep = df['수면시간'].mean()
    delta_sleep = f"{avg_sleep-6:.1f}시간" if avg_sleep >= 6 else f"{avg_sleep-6:.1f}시간"
    st.markdown(f"""
    <div style='
        background-color: #F8F9FA; 
        padding: 1.5rem; 
        border-radius: 15px; 
        margin: 0.5rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border: 2px solid #E9ECEF;
        text-align: center;
    '>
        <h3 style='
            color: #2C3E50; 
            font-weight: bold; 
            margin-bottom: 0.5rem;
            font-family: NanumGothic, sans-serif;
            font-size: 1.1rem;
        '>평균 수면시간</h3>
        <p style='
            color: #2C3E50; 
            font-size: 2rem; 
            font-weight: 900; 
            margin: 0.5rem 0;
            font-family: NanumGothic, sans-serif;
        '>{avg_sleep:.1f}시간</p>
        <p style='
            color: #666; 
            font-size: 0.9rem; 
            margin: 0;
            font-family: NanumGothic, sans-serif;
            font-weight: bold;
        '>기준 대비: {delta_sleep}</p>
    </div>
    """, unsafe_allow_html=True)

with row1_col2:
    avg_study = df['공부시간'].mean()
    delta_study = f"{avg_study-4:.1f}시간" if avg_study >= 4 else f"{avg_study-4:.1f}시간"
    st.markdown(f"""
    <div style='
        background-color: #F8F9FA; 
        padding: 1.5rem; 
        border-radius: 15px; 
        margin: 0.5rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border: 2px solid #E9ECEF;
        text-align: center;
    '>
        <h3 style='
            color: #2C3E50; 
            font-weight: bold; 
            margin-bottom: 0.5rem;
            font-family: NanumGothic, sans-serif;
            font-size: 1.1rem;
        '>평균 공부시간</h3>
        <p style='
            color: #2C3E50; 
            font-size: 2rem; 
            font-weight: 900; 
            margin: 0.5rem 0;
            font-family: NanumGothic, sans-serif;
        '>{avg_study:.1f}시간</p>
        <p style='
            color: #666; 
            font-size: 0.9rem; 
            margin: 0;
            font-family: NanumGothic, sans-serif;
            font-weight: bold;
        '>기준 대비: {delta_study}</p>
    </div>
    """, unsafe_allow_html=True)

with row2_col1:
    total_exercise = df['운동시간'].sum()
    st.markdown(f"""
    <div style='
        background-color: #F8F9FA; 
        padding: 1.5rem; 
        border-radius: 15px; 
        margin: 0.5rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border: 2px solid #E9ECEF;
        text-align: center;
    '>
        <h3 style='
            color: #2C3E50; 
            font-weight: bold; 
            margin-bottom: 0.5rem;
            font-family: NanumGothic, sans-serif;
            font-size: 1.1rem;
        '>총 운동시간</h3>
        <p style='
            color: #2C3E50; 
            font-size: 2rem; 
            font-weight: 900; 
            margin: 0.5rem 0;
            font-family: NanumGothic, sans-serif;
        '>{total_exercise}시간</p>
        <p style='
            color: #FF6B6B; 
            font-size: 0.9rem; 
            margin: 0;
            font-family: NanumGothic, sans-serif;
            font-weight: bold;
        '>운동 필요!</p>
    </div>
    """, unsafe_allow_html=True)

with row2_col2:
    good_mood_ratio = (df['기분'] == '좋음').sum() / len(df) * 100
    delta_mood = f"{good_mood_ratio-50:.0f}%" if good_mood_ratio >= 50 else f"{good_mood_ratio-50:.0f}%"
    st.markdown(f"""
    <div style='
        background-color: #F8F9FA; 
        padding: 1.5rem; 
        border-radius: 15px; 
        margin: 0.5rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border: 2px solid #E9ECEF;
        text-align: center;
    '>
        <h3 style='
            color: #2C3E50; 
            font-weight: bold; 
            margin-bottom: 0.5rem;
            font-family: NanumGothic, sans-serif;
            font-size: 1.1rem;
        '>좋은 기분 비율</h3>
        <p style='
            color: #2C3E50; 
            font-size: 2rem; 
            font-weight: 900; 
            margin: 0.5rem 0;
            font-family: NanumGothic, sans-serif;
        '>{good_mood_ratio:.0f}%</p>
        <p style='
            color: #666; 
            font-size: 0.9rem; 
            margin: 0;
            font-family: NanumGothic, sans-serif;
            font-weight: bold;
        '>기준 대비: {delta_mood}</p>
    </div>
    """, unsafe_allow_html=True)

# 추천사항 - HTML로 더 선명하게
st.markdown("""
<h2 style='
    color: #2C3E50; 
    font-weight: 800; 
    font-size: 2.2rem; 
    margin-top: 2rem; 
    margin-bottom: 1rem;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    font-family: NanumGothic, sans-serif;
'>💡 개선 제안</h2>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style='
        background-color: #E3F2FD; 
        padding: 1.5rem; 
        border-radius: 15px; 
        margin: 0.5rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border: 2px solid #BBDEFB;
        text-align: center;
    '>
        <p style='
            color: #1A1A1A; 
            font-size: 1.1rem; 
            font-weight: bold; 
            margin: 0;
            font-family: NanumGothic, sans-serif;
        '>🌙 수면시간을 7-8시간으로 늘려보세요!</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='
        background-color: #FFF3E0; 
        padding: 1.5rem; 
        border-radius: 15px; 
        margin: 0.5rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border: 2px solid #FFCC80;
        text-align: center;
    '>
        <p style='
            color: #1A1A1A; 
            font-size: 1.1rem; 
            font-weight: bold; 
            margin: 0;
            font-family: NanumGothic, sans-serif;
        '>🏃‍♂️ 운동시간을 추가해보시는 것은 어떨까요?</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='
        background-color: #E8F5E8; 
        padding: 1.5rem; 
        border-radius: 15px; 
        margin: 0.5rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border: 2px solid #A5D6A7;
        text-align: center;
    '>
        <p style='
            color: #1A1A1A; 
            font-size: 1.1rem; 
            font-weight: bold; 
            margin: 0;
            font-family: NanumGothic, sans-serif;
        '>📚 꾸준한 공부 패턴이 좋습니다!</p>
    </div>
    """, unsafe_allow_html=True)


