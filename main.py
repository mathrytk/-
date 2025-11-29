import streamlit as st
import math

# 1. Page Configuration
st.set_page_config(page_title="Smart Calculator", page_icon="🧮")

# 2. Title
st.title("🧮 Smart Calculator")
st.markdown("Select an operation first, and the input fields will adapt automatically.")

# 3. Step 1: Select Operation (This determines the input labels)
st.divider()
st.header("Step 1: Select Operation")

operation = st.selectbox(
    "Choose the math operation you want to perform:",
    ("Addition (+)", "Subtraction (-)", "Multiplication (*)", "Division (/)", 
     "Modulo (%)", "Power (^)", "Logarithm (log)")
)

# 4. Logic to determine Input Labels based on the selection
# 연산 종류에 따라 입력창의 제목(label)을 다르게 설정합니다.
if "Power" in operation:
    label1 = "Base (Bottom number)"
    label2 = "Exponent (Power)"
    help_text = "Calculates Base to the power of Exponent."
elif "Logarithm" in operation:
    label1 = "Value (Antilogarithm)"
    label2 = "Base"
    help_text = "Calculates the logarithm of the Value with the given Base."
elif "Division" in operation or "Modulo" in operation:
    label1 = "Dividend (Number to be divided)"
    label2 = "Divisor (Number to divide by)"
    help_text = "Performs division or remainder calculation."
else:
    # Default for Addition, Subtraction, Multiplication
    label1 = "First Number"
    label2 = "Second Number"
    help_text = "Performs basic arithmetic."

# 5. Step 2: Input Numbers (Labels update dynamically)
st.header("Step 2: Enter Numbers")
st.info(f"Current Mode: {help_text}") # Shows a helpful tip based on selection

col1, col2 = st.columns(2)

with col1:
    num1 = st.number_input(label1, value=0.0, format="%f")

with col2:
    num2 = st.number_input(label2, value=0.0, format="%f")

# 6. Step 3: Calculate
st.divider()
if st.button("Calculate Result"):
    result = None
    error = None
    symbol = ""

    # Calculation Logic
    if "Addition" in operation:
        result = num1 + num2
        symbol = "+"
    elif "Subtraction" in operation:
        result = num1 - num2
        symbol = "-"
    elif "Multiplication" in operation:
        result = num1 * num2
        symbol = "×"
    elif "Division" in operation:
        if num2 == 0:
            error = "Cannot divide by zero."
        else:
            result = num1 / num2
            symbol = "÷"
    elif "Modulo" in operation:
        if num2 == 0:
            error = "Cannot divide by zero."
        else:
            result = num1 % num2
            symbol = "%"
    elif "Power" in operation:
        result = num1 ** num2
        symbol = "^"
    elif "Logarithm" in operation:
        if num1 <= 0:
            error = "Value must be positive for Logarithm."
        elif num2 <= 0 or num2 == 1:
            error = "Base must be positive and not 1."
        else:
            result = math.log(num1, num2)
            symbol = "log"

    # Display Output
    if error:
        st.error(f"Error: {error}")
    else:
        st.success(f"Result: {result}")
        
        # Display Equation cleanly
        if "Logarithm" in operation:
            st.latex(f"\\log_{{{num2}}} ({num1}) = {result}")
        elif "Power" in operation:
             st.latex(f"{num1}^{{{num2}}} = {result}")
        else:
            st.info(f"Equation: {num1} {symbol} {num2} = {result}")
