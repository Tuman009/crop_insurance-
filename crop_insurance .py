import streamlit as st

class Farmer:
    def __init__(self, name, crop_type, area, expected_yield):
        self.name = name
        self.crop_type = crop_type
        self.area = area
        self.expected_yield = expected_yield
        self.premium = self.calculate_premium()
        self.actual_yield = None
    
    def calculate_premium(self):
        premium_rate = {
            'wheat': 0.02,
            'rice': 0.015,
            'maize': 0.018,
            'mango': 0.029,
            'potato': 0.012,
            'onion': 0.02,
            'carrot': 0.015,
            'tomato': 0.01,
            'spinach': 0.025,
        }
        if self.crop_type not in premium_rate:
            return "Invalid crop type"
        sum_insured_per_hectare = 20000
        sum_insured = sum_insured_per_hectare * self.area
        government_subsidy = 0.75
        premium = sum_insured * premium_rate[self.crop_type] * (1 - government_subsidy)
        return premium

    def set_actual_yield(self, yield_value):
        self.actual_yield = yield_value

    def calculate_claim(self):
        if self.actual_yield is None:
            return "Actual yield not set"
        if self.actual_yield < self.expected_yield:
            yield_loss = self.expected_yield - self.actual_yield
            sum_insured_per_hectare = 20000
            claim_amount = (yield_loss / self.expected_yield) * sum_insured_per_hectare * self.area
            return claim_amount
        else:
            return 0

# Streamlit UI
st.title("Farmer Insurance Calculator")

# Collecting user input
name = st.text_input("Enter farmer's name:", key='name')
crop_type = st.selectbox("Select crop type:", ['wheat', 'rice', 'maize', 'mango',
                                                'potato', 'onion', 'carrot',
                                                'tomato', 'spinach'], key='crop_type').lower()
area = st.number_input("Enter area of land in hectares:", min_value=0.0, step=0.1, key='area')
expected_yield = st.number_input("Enter expected yield in quintals:", min_value=0.0, step=0.1, key='expected_yield')

# Initialize session state variables
if 'farmer' not in st.session_state:
    st.session_state.farmer = None
if 'actual_yield' not in st.session_state:
    st.session_state.actual_yield = None

# Creating a Farmer instance with user input
if st.button("Calculate Premium"):
    if name and crop_type and area > 0 and expected_yield > 0:
        st.session_state.farmer = Farmer(name=name, crop_type=crop_type, area=area, expected_yield=expected_yield)
        st.session_state.actual_yield = None
        st.write(f"**Farmer:** {st.session_state.farmer.name}")
        st.write(f"**Crop Type:** {st.session_state.farmer.crop_type}")
        st.write(f"**Area:** {st.session_state.farmer.area} hectares")
        st.write(f"**Expected Yield:** {st.session_state.farmer.expected_yield} quintals")
        st.write(f"**Premium:** {st.session_state.farmer.premium:.2f} INR")
    else:
        st.write("Please fill all the required fields correctly.")

# Collecting actual yield after the season and calculating the claim
if st.session_state.farmer:
    actual_yield = st.number_input("Enter actual yield in quintals:", min_value=0.0, step=0.1, key='actual_yield')
    if st.button("Calculate Claim"):
        if actual_yield >= 0:
            st.session_state.farmer.set_actual_yield(actual_yield)
            st.write(f"**Actual Yield:** {st.session_state.farmer.actual_yield} quintals")

            # Calculating and printing the claim amount
            claim_amount = st.session_state.farmer.calculate_claim()
            st.write(f"**Claim Amount:** {claim_amount:.2f} INR")
        else:
            st.write("Please enter a valid actual yield.")
