import streamlit as st
import pandas as pd
import datetime
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Define the coefficients for different machines (example coefficients for lathe machine)
coefficients = {
    'Small Lathe Machine': {
        'Initial Cost': 0.0004056891810690172,
        'Space Occupied': 0.033,
        'Power Rating': 0.275,
        'Time Spent': 0.224,
        'Workpieces': 0.180,
        'Operators': 0.201,
        'Ventilation Cost': 0.006782578466305367,
        'Cleaning Cost': 0.2553865093524714,
        'Waste Management Cost': 0,
        'Toilet Usage Cost': 0.04003480507607149
    },
    'Big Lathe Machine': {
        'Initial Cost': 0.0021354470349066682,
        'Space Occupied': 0.045,
        'Power Rating': 0.224,
        'Time Spent': 5.749638260612507,
        'Workpieces': 0.214,
        'Operators': 0.0201,
        'Ventilation Cost': 0.021944294186857505,
        'Cleaning Cost': 0.06706617721440011,
        'Waste Management Cost': 0.,
        'Toilet Usage Cost': 0.13281861336268186
    },
'Milling Machine': {
        'Initial Cost': 0.0008444683998909656,
        'Space Occupied': 0.37965008701319825,
        'Power Rating': 0.32631605467933955,
        'Time Spent': 406.5041220927978,
        'Workpieces': 4.540691290604314,
        'Operators': -250.80477836446548,
        'Ventilation Cost': -0.06533824398165722,
        'Cleaning Cost': 0.30564880475519285,
        'Waste Management Cost': 0,
        'Toilet Usage Cost': -0.05682205290169007
    },
    'Drilling Machine': {
        'Initial Cost': 0.0008811454118560923,
        'Space Occupied': -1.3291536349971844,
        'Power Rating': 0.34074783975501166,
        'Time Spent': 421.76580196132716,
        'Workpieces': 22.633467305981846,
        'Operators': 74.3906011948468,
        'Ventilation Cost': 0.014096088617983726,
        'Cleaning Cost': -0.05696711576000535,
        'Waste Management Cost': -0.03183167891841876,
        'Toilet Usage Cost': -0.1866917036962925
    },
    'Grounding Machine': {
        'Initial Cost': 0.0010288561910239888,
        'Space Occupied': -1.1066286541216819,
        'Power Rating': 0.26439350427659036,
        'Time Spent': 422.7564015070455,
        'Workpieces': -27.967300562716243,
        'Operators': 25.47044128146337,
        'Ventilation Cost': 0.02776236843792823,
        'Cleaning Cost': -0.44320158037384694,
        'Waste Management Cost': 0,
        'Toilet Usage Cost': -0.08500903366631007
    },
    # Add coefficients for more machines here
    
}

# Function to calculate the price based on selected machine and input values
def calculate_price(machine, data):
    price = sum(coefficients[machine][key] * data[key] for key in coefficients[machine])
    return price

# Capture the time logged in
time_logged_in = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Define the Streamlit interface
st.title("Workshop Machine Price Estimator")
st.write("A simple estimator to determine the price based on machine usage using Multiple Linear Regression.")

# Add customer name input
customer_name = st.text_input("Enter Customer Name", placeholder="John Doe")

# Dropdown for selecting the machine type
machine = st.selectbox("Select Machine Type", list(coefficients.keys()))

# User inputs for the variable values
initial_cost = st.number_input("Initial Cost (₦)", min_value=1000000)
area_occupied = st.number_input("Area Occupied (m²)", min_value=50.0, max_value=500.0)
power_rating = st.number_input("Power Rating (Watts)", min_value=10000, max_value=30000, step=500)
time_spent = st.number_input("Time Spent (minutes)", min_value=60, max_value=720, step=60)
workpieces = st.number_input("Workpieces (units)", min_value=1, max_value=100, step=1)
operators = st.number_input("Operators (persons)", min_value=1, max_value=10, step=1)
ventilation_cost = st.number_input("Ventilation Cost (₦)", min_value=1000, max_value=20000, step=500)
cleaning_cost = st.number_input("Cleaning Cost (₦)", min_value=1000, max_value=20000, step=500)
waste_management_cost = st.number_input("Waste Management Cost (₦)", min_value=1000, max_value=20000, step=500)
toilet_usage_cost = st.number_input("Toilet Usage Cost (₦)", min_value=1000, max_value=10000, step=500)

# Input data for calculation
data = {
    'Initial Cost': initial_cost,
    'Space Occupied': area_occupied,
    'Power Rating': power_rating,
    'Time Spent': time_spent,
    'Workpieces': workpieces,
    'Operators': operators,
    'Ventilation Cost': ventilation_cost,
    'Cleaning Cost': cleaning_cost,
    'Waste Management Cost': waste_management_cost,
    'Toilet Usage Cost': toilet_usage_cost
}

# File path for storing customer history
csv_file = "pricing_history.csv"

# Function to save data to CSV
def save_to_csv(customer_name, machine, price, time_logged_in):
    new_entry = pd.DataFrame([{
        "Customer Name": customer_name,
        "Machine Type": machine,
        "Estimated Price (₦)": price,
        "Time Logged In": time_logged_in
    }])

    # Check if file exists and append accordingly
    if os.path.exists(csv_file):
        existing_data = pd.read_csv(csv_file)
        updated_data = pd.concat([existing_data, new_entry], ignore_index=True)
        updated_data.to_csv(csv_file, index=False)
    else:
        new_entry.to_csv(csv_file, index=False)

# Calculate and display the price
if st.button("Estimate Price"):
    price = calculate_price(machine, data)
    
    # Save to CSV
    save_to_csv(customer_name, machine, price, time_logged_in)
    
    st.success(f"**Customer Name:** {customer_name}")
    st.success(f"**Time Logged In:** {time_logged_in}")
    st.success(f"The estimated price for {machine} usage is: ₦{price:,.2f}")

# Add a button to download the CSV file
if os.path.exists(csv_file):
    with open(csv_file, "rb") as file:
        st.download_button(
            label="Download Pricing History",
            data=file,
            file_name="pricing_history.csv",
            mime="text/csv"
        )
