import streamlit as st

# 페이지 설정 - 반드시 최상단에 위치해야 함
st.set_page_config(page_title="🌟 라이프 트래커", layout="wide")

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib.patches import Circle
import matplotlib.patches as mpatches
import matplotlib.font_manager as fm
import os

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
            plt.rcParams['axes.titlesize'] = 12
            plt.rcParams['xtick.labelsize'] = 10
            plt.rcParams['ytick.labelsize'] = 10
            plt.rcParams['legend.fontsize'] = 10
            plt.rcParams['figure.titlesize'] = 14
            
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
    h2 {
        color: #2C3E50 !important;
        font-weight: 800 !important;
        font-size: 2.0rem !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1) !important;
        -webkit-font-smoothing: antialiased !important;
        -moz-osx-font-smoothing: grayscale !important;
    }
    h3 {
        color: #2C3E50 !important;
        font-weight: 700 !important;
        font-size: 1.6rem !important;
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

# 데이터 준비 - CSV 파일에서 읽기
@st.cache_data
def load_lifestyle_data():
    """CSV 파일에서 라이프스타일 데이터 로드"""
    try:
        import pandas as pd
        df = pd.read_csv('./data/lifestyle_100_utf8.csv')
        st.success(f"✅ CSV 파일을 성공적으로 읽었습니다!")
        return df
    except FileNotFoundError:
        st.error("❌ lifestyle_100_utf8.csv 파일을 찾을 수 없습니다. 파일이 업로드되었는지 확인해주세요.")
        return None
    except Exception as e:
        st.error(f"❌ CSV 파일 읽기 오류: {e}")
        return None

# 데이터 로드
df = load_lifestyle_data()

if df is None:
    st.stop()  # 데이터가 없으면 여기서 중단

# 데이터 기본 정보 표시
st.info(f"📊 **{len(df)}일간의 라이프스타일 데이터 분석** | 기간: {df['날짜'].iloc[0]} ~ {df['날짜'].iloc[-1]}")

# 데이터 품질 체크 및 인사이트
col1, col2 = st.columns(2)
with col1:
    # 기본 통계
    avg_sleep = df['수면시간'].mean()
    avg_study = df['공부시간'].mean()
    avg_exercise = df['운동시간'].mean()
    
    st.markdown("### 📈 전체 기간 평균")
    st.write(f"• 수면: **{avg_sleep:.1f}시간/일** {'✅ 충분' if avg_sleep >= 7 else '⚠️ 부족'}")
    st.write(f"• 공부: **{avg_study:.1f}시간/일** {'✅ 꾸준함' if avg_study >= 3 else '📚 더 필요'}")
    st.write(f"• 운동: **{avg_exercise:.1f}시간/일** {'✅ 활발' if avg_exercise >= 1 else '🏃‍♂️ 더 필요'}")

with col2:
    # 기분 분석
    mood_counts = df['기분'].value_counts()
    good_ratio = (mood_counts.get('좋음', 0) / len(df)) * 100
    
    st.markdown("### 😊 기분 분석")
    st.write(f"• 좋은 날: **{mood_counts.get('좋음', 0)}일** ({good_ratio:.1f}%)")
    st.write(f"• 보통인 날: **{mood_counts.get('보통', 0)}일** ({(mood_counts.get('보통', 0)/len(df)*100):.1f}%)")
    st.write(f"• 나쁜 날: **{mood_counts.get('나쁨', 0)}일** ({(mood_counts.get('나쁨', 0)/len(df)*100):.1f}%)")
    
    if good_ratio >= 50:
        st.success("🌟 전반적으로 긍정적인 라이프스타일!")
    elif good_ratio >= 30:
        st.warning("💪 개선의 여지가 있습니다!")
    else:
        st.error("🚨 라이프스타일 개선이 필요합니다!")

# 최근 30일 데이터 선택 (차트용)
chart_days = min(30, len(df))
recent_df = df.tail(chart_days).copy()
recent_df = recent_df.reset_index(drop=True)

# 메인 타이틀 - 크기를 줄이고 더 진하게
st.markdown("""
<h2 style='
    text-align: center; 
    color: #000000; 
    font-weight: 900; 
    font-size: 2.8rem; 
    margin-bottom: 2rem;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    font-family: NanumGothic, sans-serif;
'>🌟 라이프 트래커 </h2>
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
    
    # 도넛 차트 생성 - 33% 텍스트 크기 증가
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
    
    # 제목 설정 (더 진하고 선명하게)
    ax1.set_title('😊 기분 분포', fontsize=26, fontweight='bold', pad=30, color='#000000')
    
    # 텍스트 스타일링 (퍼센트 숫자 더 크고 진하게)
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(22)  # 16→22로 증가
        autotext.set_fontweight('black')  # 더 굵게
    
    for text in texts:
        text.set_fontsize(18)
        text.set_fontweight('bold')
        text.set_color('#000000')
    
    ax1.set_facecolor('white')
    fig1.patch.set_facecolor('white')
    
    st.pyplot(fig1, use_container_width=True)

# 시간 사용 패턴 차트 - 더 진한 색상
st.markdown("""
<h3 style='
    color: #000000; 
    font-weight: 900; 
    font-size: 2.0rem; 
    margin-top: 2rem; 
    margin-bottom: 1rem;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    font-family: NanumGothic, sans-serif;
'>⏰ 시간 사용 패턴</h3>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # 수면시간 트렌드 - 인사이트 강화
    fig2, ax2 = plt.subplots(figsize=(8, 6), facecolor='white', dpi=100)
    
    x_positions = list(range(len(recent_df)))
    sleep_hours = recent_df['수면시간']
    
    # 트렌드 라인 추가
    z = np.polyfit(x_positions, sleep_hours, 1)
    p = np.poly1d(z)
    trend_line = p(x_positions)
    
    # 수면시간 라인 차트
    ax2.plot(x_positions, sleep_hours, color='#FF6B9D', linewidth=3, marker='o', 
             markersize=6, markerfacecolor='white', markeredgecolor='#FF6B9D', 
             markeredgewidth=2, label='실제 수면시간')
    
    # 트렌드 라인
    ax2.plot(x_positions, trend_line, color='#FF1493', linewidth=2, linestyle='--', 
             alpha=0.8, label=f'트렌드 {"↗️증가" if z[0] > 0 else "↘️감소" if z[0] < 0 else "→평행"}')
    
    # 권장 수면시간 기준선
    ax2.axhline(y=7, color='#32CD32', linestyle=':', linewidth=2, alpha=0.7, label='권장 7시간')
    
    # 배경 그라데이션
    ax2.fill_between(x_positions, sleep_hours, alpha=0.2, color='#FF6B9D')
    
    # 수면 부족 구간 하이라이트
    insufficient_sleep = sleep_hours < 6
    if insufficient_sleep.any():
        ax2.fill_between(x_positions, 0, 6, where=insufficient_sleep, 
                        color='#FFB6C1', alpha=0.3, label='수면 부족 구간')
    
    ax2.set_title(f'수면시간 변화 (최근 {len(recent_df)}일)', fontsize=20, fontweight='bold', color='#000000', pad=20)
    ax2.set_ylabel('시간(시간)', fontsize=18, color='#000000', fontweight='bold')
    
    # X축 라벨을 범주화
    if len(recent_df) >= 30:
        tick_positions = [0, 9, 19, 29]
        tick_labels = ['1일차', '10일차', '20일차', '30일차']
    elif len(recent_df) >= 10:
        tick_positions = [0, len(recent_df)//2, len(recent_df)-1]
        tick_labels = ['시작', '중간', '최근']
    else:
        tick_positions = list(range(len(recent_df)))
        tick_labels = [f'{i+1}일차' for i in range(len(recent_df))]
    
    ax2.set_xticks(tick_positions)
    ax2.set_xticklabels(tick_labels, fontsize=14, fontweight='bold')
    ax2.set_xlabel('기간', fontsize=18, color='#000000', fontweight='bold')
    
    ax2.grid(True, alpha=0.3, color='#E8E8E8', linewidth=1)
    ax2.set_facecolor('white')
    ax2.legend(loc='upper right', fontsize=10)
    
    # 축 스타일링
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_color('#CCCCCC')
    ax2.spines['bottom'].set_color('#CCCCCC')
    ax2.tick_params(colors='#666666', labelsize=12)
    ax2.tick_params(axis='y', labelsize=14)
    
    fig2.patch.set_facecolor('white')
    st.pyplot(fig2, use_container_width=True)

with col2:
    # 공부시간 바 차트 - 인사이트 강화
    fig3, ax3 = plt.subplots(figsize=(8, 6), facecolor='white', dpi=100)
    
    study_hours = recent_df['공부시간']
    x_positions = list(range(len(recent_df)))
    
    # 공부시간에 따른 색상 구분
    colors = []
    for hour in study_hours:
        if hour >= 5:
            colors.append('#32CD32')  # 많이 공부한 날 - 초록
        elif hour >= 3:
            colors.append('#FFD700')  # 적당히 공부한 날 - 노랑
        else:
            colors.append('#FF6B6B')  # 적게 공부한 날 - 빨강
    
    bars = ax3.bar(x_positions, study_hours, color=colors, alpha=0.8, 
                   edgecolor='white', linewidth=1)
    
    # 평균선 추가
    avg_line = study_hours.mean()
    ax3.axhline(y=avg_line, color='#FF4500', linestyle='--', linewidth=2, 
                alpha=0.8, label=f'평균 {avg_line:.1f}시간')
    
    # 목표선 추가 (4시간)
    ax3.axhline(y=4, color='#4169E1', linestyle=':', linewidth=2, 
                alpha=0.7, label='목표 4시간')
    
    # 값 표시 최적화
    if len(study_hours) <= 15:
        # 데이터가 적으면 모든 바에 표시
        for i, v in enumerate(study_hours):
            ax3.text(i, v + 0.1, str(v) + 'h', ha='center', va='bottom', 
                    fontweight='bold', fontsize=9, color='#000000')
    else:
        # 데이터가 많으면 최고값들만 표시
        max_indices = study_hours.nlargest(5).index
        for i in max_indices:
            v = study_hours.iloc[i]
            ax3.text(i, v + 0.1, str(v) + 'h', ha='center', va='bottom', 
                    fontweight='bold', fontsize=9, color='#000000')
    
    ax3.set_title(f'📚 공부시간 분포 (최근 {len(recent_df)}일)', fontsize=20, fontweight='bold', color='#000000', pad=20)
    ax3.set_ylabel('시간(시간)', fontsize=18, color='#000000', fontweight='bold')
    
    # X축 라벨 설정
    if len(recent_df) >= 30:
        tick_positions = [0, 9, 19, 29]
        tick_labels = ['1일차', '10일차', '20일차', '30일차']
    elif len(recent_df) >= 10:
        tick_positions = [0, len(recent_df)//2, len(recent_df)-1]
        tick_labels = ['시작', '중간', '최근']
    else:
        tick_positions = list(range(len(recent_df)))
        tick_labels = [f'{i+1}일차' for i in range(len(recent_df))]
    
    ax3.set_xticks(tick_positions)
    ax3.set_xticklabels(tick_labels, fontsize=14, fontweight='bold')
    ax3.set_xlabel('기간', fontsize=18, color='#000000', fontweight='bold')
    
    ax3.grid(True, alpha=0.3, axis='y', color='#E8E8E8', linewidth=1)
    ax3.set_facecolor('white')
    ax3.legend(loc='upper right', fontsize=10)
    
    # 축 스타일링
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    ax3.spines['left'].set_color('#CCCCCC')
    ax3.spines['bottom'].set_color('#CCCCCC')
    ax3.tick_params(colors='#666666', labelsize=12)
    ax3.tick_params(axis='y', labelsize=14)
    
    fig3.patch.set_facecolor('white')
    st.pyplot(fig3, use_container_width=True)

# 종합 히트맵 - 더 진한 색상
st.markdown("""
<h3 style='
    color: #000000; 
    font-weight: 900; 
    font-size: 2.0rem; 
    margin-top: 2rem; 
    margin-bottom: 1rem;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    font-family: NanumGothic, sans-serif;
'>🔥 종합 활동 히트맵</h3>
""", unsafe_allow_html=True)

# 히트맵용 데이터 준비 (최근 30일)
heatmap_data = recent_df[['수면시간', '공부시간', '운동시간']].T
heatmap_data.columns = [f"{i+1}일" for i in range(len(recent_df))]

fig4, ax4 = plt.subplots(figsize=(12, 6), facecolor='white', dpi=100)

# 선명한 파스텔 컬러맵
colors = ['#FFFFFF', '#FFE4E6', '#FFB8BB', '#FF8A90']
cmap = sns.blend_palette(colors, as_cmap=True)

# 히트맵 생성 (선명한 설정)
sns.heatmap(heatmap_data, annot=True, fmt='d', cmap=cmap, 
            cbar_kws={'label': '시간 (hours)'}, ax=ax4,
            linewidths=3, linecolor='white', square=True,
            annot_kws={'fontsize': 14, 'fontweight': 'bold'})

ax4.set_title('📊 일별 활동 패턴 (최근 30일)', fontsize=22, fontweight='bold', color='#000000', pad=20)
ax4.set_ylabel('활동 유형', fontsize=16, color='#000000', fontweight='bold')
ax4.set_xlabel('날짜', fontsize=16, color='#000000', fontweight='bold')

# 축 레이블 스타일링 (더 진하게)
ax4.tick_params(colors='#000000', labelsize=12)
ax4.set_facecolor('white')

fig4.patch.set_facecolor('white')
st.pyplot(fig4, use_container_width=True)

# 히트맵 인사이트
col1, col2, col3 = st.columns(3)
with col1:
    best_sleep_day = recent_df.loc[recent_df['수면시간'].idxmax()]
    st.info(f"🌙 **최고 수면일**: {best_sleep_day['수면시간']}시간 (기분: {best_sleep_day['기분']})")

with col2:
    best_study_day = recent_df.loc[recent_df['공부시간'].idxmax()]
    st.info(f"📚 **최고 공부일**: {best_study_day['공부시간']}시간 (기분: {best_study_day['기분']})")

with col3:
    if recent_df['운동시간'].max() > 0:
        best_exercise_day = recent_df.loc[recent_df['운동시간'].idxmax()]
        st.info(f"🏃‍♂️ **최고 운동일**: {best_exercise_day['운동시간']}시간 (기분: {best_exercise_day['기분']})")
    else:
        st.warning("🚨 **운동 기록 없음**: 운동 시작을 권장합니다!")

# 상관관계 분석 및 인사이트
st.markdown("---")
st.markdown("## 🔍 행동 패턴 분석")

# 기분과 다른 변수들의 관계 분석
mood_analysis = df.groupby('기분')[['수면시간', '공부시간', '운동시간']].mean()

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 😊 기분별 평균 활동시간")
    
    # 기분별 데이터 시각화
    fig5, ax5 = plt.subplots(figsize=(10, 6), facecolor='white', dpi=100)
    
    moods = mood_analysis.index
    x_pos = np.arange(len(moods))
    width = 0.25
    
    # 각 활동별 바 그래프
    bars1 = ax5.bar(x_pos - width, mood_analysis['수면시간'], width, 
                    label='수면시간', color='#FF6B9D', alpha=0.8)
    bars2 = ax5.bar(x_pos, mood_analysis['공부시간'], width,
                    label='공부시간', color='#45B7D1', alpha=0.8)
    bars3 = ax5.bar(x_pos + width, mood_analysis['운동시간'], width,
                    label='운동시간', color='#32CD32', alpha=0.8)
    
    # 값 표시
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            ax5.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{height:.1f}h', ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    ax5.set_title('기분별 평균 활동시간 비교', fontsize=16, fontweight='bold', color='#000000')
    ax5.set_ylabel('시간(시간)', fontsize=14, color='#000000', fontweight='bold')
    ax5.set_xlabel('기분', fontsize=14, color='#000000', fontweight='bold')
    ax5.set_xticks(x_pos)
    ax5.set_xticklabels(moods, fontsize=12, fontweight='bold')
    ax5.legend(fontsize=11)
    ax5.grid(True, alpha=0.3, axis='y')
    
    # 축 스타일링
    ax5.spines['top'].set_visible(False)
    ax5.spines['right'].set_visible(False)
    ax5.set_facecolor('white')
    
    fig5.patch.set_facecolor('white')
    st.pyplot(fig5, use_container_width=True)

with col2:
    st.markdown("### 📊 핵심 인사이트")
    
    # 기분과 수면시간 관계
    good_mood_sleep = mood_analysis.loc['좋음', '수면시간'] if '좋음' in mood_analysis.index else 0
    bad_mood_sleep = mood_analysis.loc['나쁨', '수면시간'] if '나쁨' in mood_analysis.index else 0
    
    if good_mood_sleep > bad_mood_sleep:
        st.success(f"✅ **수면-기분 상관관계**: 좋은 기분일 때 평균 {good_mood_sleep:.1f}시간 수면")
    else:
        st.warning("⚠️ **수면 패턴 주의**: 수면시간과 기분의 관계를 점검해보세요")
    
    # 운동과 기분 관계
    good_mood_exercise = mood_analysis.loc['좋음', '운동시간'] if '좋음' in mood_analysis.index else 0
    bad_mood_exercise = mood_analysis.loc['나쁨', '운동시간'] if '나쁨' in mood_analysis.index else 0
    
    if good_mood_exercise > bad_mood_exercise:
        st.success(f"✅ **운동-기분 상관관계**: 좋은 기분일 때 평균 {good_mood_exercise:.1f}시간 운동")
    else:
        st.info("💡 **운동 효과**: 운동이 기분 개선에 도움될 수 있습니다")
    
    # 최적 조합 찾기
    best_combination = df[df['기분'] == '좋음']
    if not best_combination.empty:
        optimal_sleep = best_combination['수면시간'].mean()
        optimal_study = best_combination['공부시간'].mean()
        optimal_exercise = best_combination['운동시간'].mean()
        
        st.markdown("### 🎯 최적 라이프스타일 조합")
        st.markdown(f"**좋은 기분을 위한 황금 비율:**")
        st.markdown(f"• 수면: **{optimal_sleep:.1f}시간**")
        st.markdown(f"• 공부: **{optimal_study:.1f}시간**")
        st.markdown(f"• 운동: **{optimal_exercise:.1f}시간**")
    
    # 개선 우선순위
    st.markdown("### 🚀 개선 우선순위")
    
    priorities = []
    if avg_sleep < 7:
        priorities.append("🌙 수면시간 늘리기")
    if avg_exercise < 1:
        priorities.append("🏃‍♂️ 운동 시작하기")
    if good_ratio < 50:
        priorities.append("😊 스트레스 관리")
    
    if priorities:
        for i, priority in enumerate(priorities, 1):
            st.markdown(f"{i}. {priority}")
    else:
        st.success("🎉 현재 라이프스타일이 양호합니다!")

# 통계 요약 - 더 진한 색상
st.markdown("""
<h3 style='
    color: #000000; 
    font-weight: 900; 
    font-size: 2.0rem; 
    margin-top: 2rem; 
    margin-bottom: 1rem;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    font-family: NanumGothic, sans-serif;
'>📈 주요 통계</h3>
""", unsafe_allow_html=True)

# 2x2 그리드 레이아웃
row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)

with row1_col1:
    avg_sleep = df['수면시간'].mean()
    delta_sleep = f"{avg_sleep-6:.1f}시간" if avg_sleep >= 6 else f"{avg_sleep-6:.1f}시간"
    delta_color = "#0066CC" if avg_sleep >= 6 else "#FF3333"  # 파란색 또는 빨간색
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
            color: #000000; 
            font-weight: 900; 
            margin-bottom: 0.5rem;
            font-family: NanumGothic, sans-serif;
            font-size: 1.0rem;
        '>평균 수면시간</h3>
        <p style='
            color: #000000; 
            font-size: 1.2rem; 
            font-weight: 900; 
            margin: 0.5rem 0;
            font-family: NanumGothic, sans-serif;
        '>{avg_sleep:.1f}시간</p>
        <p style='
            color: {delta_color}; 
            font-size: 0.9rem; 
            margin: 0;
            font-family: NanumGothic, sans-serif;
            font-weight: 900;
        '>기준 대비: {delta_sleep}</p>
    </div>
    """, unsafe_allow_html=True)

with row1_col2:
    avg_study = df['공부시간'].mean()
    delta_study = f"{avg_study-4:.1f}시간" if avg_study >= 4 else f"{avg_study-4:.1f}시간"
    delta_color = "#0066CC" if avg_study >= 4 else "#FF3333"  # 파란색 또는 빨간색
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
            color: #000000; 
            font-weight: 900; 
            margin-bottom: 0.5rem;
            font-family: NanumGothic, sans-serif;
            font-size: 1.0rem;
        '>평균 공부시간</h3>
        <p style='
            color: #000000; 
            font-size: 1.2rem; 
            font-weight: 900; 
            margin: 0.5rem 0;
            font-family: NanumGothic, sans-serif;
        '>{avg_study:.1f}시간</p>
        <p style='
            color: {delta_color}; 
            font-size: 0.9rem; 
            margin: 0;
            font-family: NanumGothic, sans-serif;
            font-weight: 900;
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
            color: #000000; 
            font-weight: 900; 
            margin-bottom: 0.5rem;
            font-family: NanumGothic, sans-serif;
            font-size: 1.0rem;
        '>총 운동시간</h3>
        <p style='
            color: #000000; 
            font-size: 1.2rem; 
            font-weight: 900; 
            margin: 0.5rem 0;
            font-family: NanumGothic, sans-serif;
        '>{total_exercise}시간</p>
        <p style='
            color: #FF3333; 
            font-size: 0.9rem; 
            margin: 0;
            font-family: NanumGothic, sans-serif;
            font-weight: 900;
        '>운동 필요!</p>
    </div>
    """, unsafe_allow_html=True)

with row2_col2:
    good_mood_ratio = (df['기분'] == '좋음').sum() / len(df) * 100
    delta_mood = f"{good_mood_ratio-50:.0f}%" if good_mood_ratio >= 50 else f"{good_mood_ratio-50:.0f}%"
    delta_color = "#0066CC" if good_mood_ratio >= 50 else "#FF3333"  # 파란색 또는 빨간색
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
            color: #000000; 
            font-weight: 900; 
            margin-bottom: 0.5rem;
            font-family: NanumGothic, sans-serif;
            font-size: 1.0rem;
        '>좋은 기분 비율</h3>
        <p style='
            color: #000000; 
            font-size: 1.2rem; 
            font-weight: 900; 
            margin: 0.5rem 0;
            font-family: NanumGothic, sans-serif;
        '>{good_mood_ratio:.0f}%</p>
        <p style='
            color: {delta_color}; 
            font-size: 0.9rem; 
            margin: 0;
            font-family: NanumGothic, sans-serif;
            font-weight: 900;
        '>기준 대비: {delta_mood}</p>
    </div>
    """, unsafe_allow_html=True)

# 추가 통계 정보 표시
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📅 분석 기간", f"{len(df)}일", "100일 데이터")

with col2:
    total_sleep = df['수면시간'].sum()
    st.metric("💤 총 수면시간", f"{total_sleep}시간", f"평균 {total_sleep/len(df):.1f}시간/일")

with col3:
    total_study = df['공부시간'].sum()
    st.metric("📚 총 공부시간", f"{total_study}시간", f"평균 {total_study/len(df):.1f}시간/일")

with col4:
    total_exercise = df['운동시간'].sum()
    st.metric("🏃‍♂️ 총 운동시간", f"{total_exercise}시간", f"평균 {total_exercise/len(df):.1f}시간/일")

# 추천사항 - 더 진한 색상
st.markdown("""
<h3 style='
    color: #000000; 
    font-weight: 900; 
    font-size: 2.0rem; 
    margin-top: 2rem; 
    margin-bottom: 1rem;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    font-family: NanumGothic, sans-serif;
'>💡 개선 제안</h3>
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
            color: #000000; 
            font-size: 1.0rem; 
            font-weight: 900; 
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
            color: #000000; 
            font-size: 1.0rem; 
            font-weight: 900; 
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
            color: #000000; 
            font-size: 1.0rem; 
            font-weight: 900; 
            margin: 0;
            font-family: NanumGothic, sans-serif;
        '>📚 꾸준한 공부 패턴이 좋습니다!</p>
    </div>
    """, unsafe_allow_html=True)
