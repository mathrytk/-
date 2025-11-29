import streamlit as st
import math

# 페이지 기본 설정
st.set_page_config(page_title="나만의 똑똑한 계산기", page_icon="🧮")

# 제목 및 설명
st.title("🧮 다기능 웹 계산기")
st.markdown("사칙연산, 나머지, 거듭제곱, 로그 계산을 지원합니다.")

# 사이드바: 연산 모드 선택
st.sidebar.header("연산 설정")
operation = st.sidebar.selectbox(
    "어떤 연산을 하시겠습니까?",
    ("덧셈 (+)", "뺄셈 (-)", "곱셈 (*)", "나눗셈 (/)", 
     "나머지 연산 (%)", "거듭제곱 (^)", "로그 (log)")
)

# 메인 화면: 숫자 입력 (2개의 컬럼으로 나누어 배치)
col1, col2 = st.columns(2)

with col1:
    num1 = st.number_input("첫 번째 숫자 (또는 진수)", value=0.0, format="%f")

with col2:
    num2 = st.number_input("두 번째 숫자 (또는 밑)", value=0.0, format="%f")

# 계산 실행 버튼
if st.button("계산하기"):
    result = None
    error = None

    # 연산 로직
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
        # 로그의 밑 조건(1이 아닌 양수)과 진수 조건(양수) 확인
        if num1 <= 0:
            error = "진수(첫 번째 숫자)는 0보다 커야 합니다."
        elif num2 <= 0 or num2 == 1:
            error = "밑(두 번째 숫자)은 1이 아닌 양수여야 합니다."
        else:
            result = math.log(num1, num2)
            symbol = "log"

    # 결과 출력
    st.divider() # 구분선
    if error:
        st.error(f"오류 발생: {error}")
    else:
        # 로그는 수식 표현이 조금 다르므로 별도 처리
        if "로그" in operation:
            st.success(f"계산 결과: {result}")
            st.latex(f"\\log_{{{num2}}} ({num1}) = {result}")
        else:
            st.success(f"계산 결과: {result}")
            # 수식 예쁘게 보여주기 (LaTeX 활용)
            st.info(f"수식: {num1} {symbol} {num2} = {result}")
