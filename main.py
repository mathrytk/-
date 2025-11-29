import streamlit as st
import math
import random
import pandas as pd
import plotly.express as px

# 1. 페이지 기본 설정 (가장 윗줄에 있어야 함)
st.set_page_config(page_title="수학 & 통계 도구상자", page_icon="🧮", layout="wide")

# 2. 사이드바: 앱 모드 선택
st.sidebar.title("메뉴 선택")
app_mode = st.sidebar.radio(
    "원하는 기능을 선택하세요:", 
    ["계산기", "확률 시뮬레이터", "연도별 세계인구분석"]
)

# ==========================================
# [기능 1] 계산기 (Calculator)
# ==========================================
if app_mode == "계산기":
    st.title("🧮 다기능 계산기")
    st.markdown("연산 종류를 먼저 선택하면, 입력해야 할 숫자의 설명이 자동으로 바뀝니다.")
    st.divider()

    # Step 1: 연산 선택
    col_mode, _ = st.columns([1, 1])
    with col_mode:
        operation = st.selectbox(
            "어떤 연산을 하시겠습니까?",
            ("덧셈 (+)", "뺄셈 (-)", "곱셈 (*)", "나눗셈 (/)", 
             "나머지 연산 (%)", "거듭제곱 (^)", "로그 (log)")
        )

    # Step 2: 입력 라벨 동적 설정
    if "거듭제곱" in operation:
        label1 = "밑 (Base)"
        label2 = "지수 (Exponent)"
        help_text = "밑을 지수만큼 거듭제곱합니다."
    elif "로그" in operation:
        label1 = "진수 (Value)"
        label2 = "밑 (Base)"
        help_text = "주어진 밑에 대한 진수의 로그값을 구합니다."
    elif "나눗셈" in operation or "나머지" in operation:
        label1 = "나눠지는 수 (피제수)"
        label2 = "나누는 수 (제수)"
        help_text = "나눗셈 혹은 나머지 연산을 수행합니다."
    else:
        label1 = "첫 번째 숫자"
        label2 = "두 번째 숫자"
        help_text = "기본적인 사칙연산을 수행합니다."

    st.info(f"💡 현재 모드: {help_text}")

    # Step 3: 숫자 입력
    col1, col2 = st.columns(2)
    with col1:
        num1 = st.number_input(label1, value=0.0, format="%f")
    with col2:
        num2 = st.number_input(label2, value=0.0, format="%f")

    # Step 4: 계산 실행 및 결과
    st.divider()
    if st.button("계산하기", type="primary"):
        result = None
        error = None
        symbol = ""

        if "덧셈" in operation:
            result = num1 + num2
            symbol = "+"
        elif "뺄셈" in operation:
            result = num1 - num2
            symbol = "-"
        elif "곱셈" in operation:
            result = num1 * num2
            symbol = "×"
        elif "나눗셈" in operation:
            if num2 == 0:
                error = "0으로 나눌 수 없습니다."
            else:
                result = num1 / num2
                symbol = "÷"
        elif "나머지" in operation:
            if num2 == 0:
                error = "0으로 나눌 수 없습니다."
            else:
                result = num1 % num2
                symbol = "%"
        elif "거듭제곱" in operation:
            result = num1 ** num2
            symbol = "^"
        elif "로그" in operation:
            if num1 <= 0:
                error = "진수는 0보다 커야 합니다."
            elif num2 <= 0 or num2 == 1:
                error = "밑은 1이 아닌 양수여야 합니다."
            else:
                result = math.log(num1, num2)
                symbol = "log"

        # 결과 출력
        if error:
            st.error(f"오류 발생: {error}")
        else:
            st.success(f"계산 결과: {result}")
            
            if "로그" in operation:
                st.latex(f"\\log_{{{num2}}} ({num1}) = {result}")
            elif "거듭제곱" in operation:
                st.latex(f"{num1}^{{{num2}}} = {result}")
            else:
                st.code(f"{num1} {symbol} {num2} = {result}")

# ==========================================
# [기능 2] 확률 시뮬레이터 (Probability Simulator)
# ==========================================
elif app_mode == "확률 시뮬레이터":
    st.title("🎲 확률 시뮬레이터")
    st.markdown("동전 던지기나 주사위 굴리기를 수없이 반복했을 때, 어떤 결과가 나오는지 확인해보세요.")
    st.divider()

    # Step 1: 시뮬레이션 설정
    col_sim1, col_sim2 = st.columns(2)
    
    with col_sim1:
        sim_type = st.radio("시뮬레이션 종류", ["동전 던지기", "주사위 굴리기"])
    
    with col_sim2:
        trials = st.number_input("시행 횟수 (예: 100, 1000)", min_value=1, max_value=100000, value=100, step=10)

    # Step 2: 시뮬레이션 실행
    if st.button("시뮬레이션 시작", type="primary"):
        results = []
        
        # 로딩 표시
        with st.spinner(f'{trials}번 시행 중입니다...'):
            if sim_type == "동전 던지기":
                outcomes = ["앞면", "뒷면"]
                results = random.choices(outcomes, k=trials)
                color_map = {"앞면": "#FF9999", "뒷면": "#9999FF"} 
                
            elif sim_type == "주사위 굴리기":
                outcomes = [1, 2, 3, 4, 5, 6]
                results = random.choices(outcomes, k=trials)
                color_map = None 

        # Step 3: 결과 데이터 처리
        df = pd.DataFrame(results, columns=["결과"])
        count_df = df["결과"].value_counts().reset_index()
        count_df.columns = ["결과", "횟수"] 
        count_df = count_df.sort_values(by="결과")

        # Step 4: 시각화 (Plotly)
        st.subheader("📊 결과 분석")
        
        res_col1, res_col2 = st.columns([1, 2])
        
        with res_col1:
            st.write("**결과 요약표**")
            st.dataframe(count_df, hide_index=True, use_container_width=True)
            if sim_type == "동전 던지기":
                st.info(f"이론적으로는 각각 약 {trials/2:.0f}번씩 나와야 합니다.")
            else:
                st.info(f"이론적으로는 각각 약 {trials/6:.0f}번씩 나와야 합니다.")

        with res_col2:
            st.write("**결과 그래프**")
            fig = px.bar(
                count_df, 
                x="결과", 
                y="횟수", 
                text="횟수",
                title=f"{sim_type} {trials}회 결과",
                color="결과" if sim_type == "동전 던지기" else None,
                color_discrete_map=color_map if sim_type == "동전 던지기" else None
            )
            if sim_type == "주사위 굴리기":
                fig.update_xaxes(type='category')
                
            st.plotly_chart(fig, use_container_width=True)

# ==========================================
# [기능 3] 연도별 세계인구분석 (World Population Analysis)
# ==========================================
elif app_mode == "연도별 세계인구분석":
    st.title("🌍 연도별 세계 인구 분석")
    st.markdown("선택한 연도의 전 세계 인구 분포를 지도에서 확인하세요.")
    st.divider()

    # 데이터 캐싱: 매번 다시 생성하지 않도록 저장
    @st.cache_data
    def get_population_data():
        # Plotly 내장 Gapminder 데이터 사용 (기본 2007년까지 있음)
        base_df = px.data.gapminder()
        
        # 필요한 국가 코드와 2007년 기준 인구 추출
        countries = base_df[base_df['year'] == 2007][['iso_alpha', 'country', 'pop', 'continent']].copy()
        
        # 요청된 연도 리스트
        target_years = [1970, 1980, 2000, 2010, 2015, 2020, 2022]
        
        all_data = []
        
        # 인구 데이터 생성 로직 (2007년 데이터를 기준으로 증감률 적용 시뮬레이션)
        for year in target_years:
            temp_df = countries.copy()
            temp_df['year'] = year
            
            # 연도별 대략적인 성장률 가중치 (단순 가정)
            if year == 1970: factor = 0.55
            elif year == 1980: factor = 0.68
            elif year == 2000: factor = 0.90
            elif year == 2010: factor = 1.04
            elif year == 2015: factor = 1.10
            elif year == 2020: factor = 1.15
            elif year == 2022: factor = 1.18
            else: factor = 1.0
            
            # 인구 수 조정
            temp_df['pop'] = (temp_df['pop'] * factor).astype(int)
            all_data.append(temp_df)
            
        final_df = pd.concat(all_data)
        
        # 인구수 구간(Bin) 설정 함수
        def categorize_population(pop):
            if pop < 10_000_000: return "01. 1천만 미만"
            elif pop < 50_000_000: return "02. 1천만 ~ 5천만"
            elif pop < 100_000_000: return "03. 5천만 ~ 1억"
            elif pop < 500_000_000: return "04. 1억 ~ 5억"
            elif pop < 1_000_000_000: return "05. 5억 ~ 10억"
            else: return "06. 10억 이상"

        final_df['인구 구간'] = final_df['pop'].apply(categorize_population)
        
        return final_df

    # 데이터 로드
    df_pop = get_population_data()

    # Step 1: 연도 선택 드롭박스
    col_filter, _ = st.columns([1, 2])
    with col_filter:
        years_list = sorted(df_pop['year'].unique())
        selected_year = st.selectbox("연도를 선택하세요:", years_list, index=len(years_list)-1)

    # Step 2: 선택된 연도 데이터 필터링
    current_df = df_pop[df_pop['year'] == selected_year]
    
    # 총 인구수 계산 (표시용)
    total_pop_display = f"{current_df['pop'].sum():,}"
    st.info(f"📊 {selected_year}년 전 세계 추산 인구 합계: 약 {total_pop_display}명 (시각화용 데모 데이터)")

    # Step 3: 세계 지도 시각화 (Choropleth Map)
    st.subheader(f"🗺️ {selected_year}년 세계 인구 지도")
    
    # 구간별 색상 지정
    color_discrete_map = {
        "01. 1천만 미만": "#d1e7dd", 
        "02. 1천만 ~ 5천만": "#a3cfbb",
        "03. 5천만 ~ 1억": "#75b798",
        "04. 1억 ~ 5억": "#198754",
        "05. 5억 ~ 10억": "#0d6efd", 
        "06. 10억 이상": "#dc3545" 
    }

    # Plotly 지도 생성
    fig = px.choropleth(
        current_df,
        locations="iso_alpha",      # 국가 코드
        color="인구 구간",           # 색상 기준
        hover_name="country",       # 호버 시 국가명
        hover_data={"pop": ":,","iso_alpha":False, "인구 구간":False},
        color_discrete_map=color_discrete_map,
        category_orders={"인구 구간": sorted(current_df['인구 구간'].unique())},
        projection="natural earth",
        title=f"{selected_year}년 국가별 인구 분포"
    )

    fig.update_layout(
        margin={"r":0,"t":40,"l":0,"b":0},
        geo=dict(showframe=False, showcoastlines=True, coastlinecolor="RebeccaPurple"),
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

    with st.expander("🌍 국가별 상세 데이터 보기"):
        st.dataframe(
            current_df[['country', 'pop', '인구 구간']].sort_values(by='pop', ascending=False),
            use_container_width=True
        )
