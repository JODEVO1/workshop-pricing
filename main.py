import datetime
import os

import pandas as pd
import streamlit as st

# Define the coefficients for different machines (example coefficients for lathe machine)
coefficients = {
    "Small Lathe Machine": {
        "Initial Cost": -0.000012,
        "Space Occupied": 232.917649,
        "Power Rating": 33.378031,
        "Time Spent": 19.707472,
        "Machine fee": 673.339524,
        "Cost of Repairs": -0.000311,
    },
    "Big Lathe Machine": {
        "Initial Cost": -0.000012,
        "Space Occupied": 232.917649,
        "Power Rating": 33.378031,
        "Time Spent": 19.707472,
        "Machine fee": 3307.525969,
        "Cost of Repairs": -0.000311,
    },
    "Milling Machine": {
        "Initial Cost": -0.000012,
        "Space Occupied": 232.917649,
        "Power Rating": 33.378031,
        "Time Spent": 19.707472,
        "Machine fee": 2006.527801,
        "Cost of Repairs": -0.000311,
    },
    "Drilling Machine": {
        "Initial Cost": -0.000012,
        "Space Occupied": 232.917649,
        "Power Rating": 33.378031,
        "Time Spent": 19.707472,
        "Machine fee": -1015.412413,
        "Cost of Repairs": -0.000311,
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
st.write(
    "A simple estimator to determine the price based on machine usage using Multiple Linear Regression."
)

# Add customer name input
customer_name = st.text_input("Enter Customer Name", placeholder="John Doe")

# Dropdown for selecting the machine type
machine = st.selectbox("Select Machine Type", list(coefficients.keys()))

# User inputs for the variable values
initial_cost = st.number_input("Initial Cost (₦)", min_value=1000000, step=100000)
area_occupied = st.number_input("Area Occupied (m²)", min_value=1.0, max_value=500.0)
power_rating = st.number_input(
    "Power Rating (Watts)", min_value=2000, max_value=30000, step=100
)
time_spent = st.number_input(
    "Time Spent (minutes)", min_value=60, max_value=720, step=60
)

# Input data for calculation
data = {
    "Initial Cost": initial_cost,
    "Space Occupied": area_occupied,
    "Power Rating": power_rating,
    "Time Spent": time_spent,
    "Machine fee": coefficients[machine]["Machine fee"],
    "Cost of Repairs": 1,  # Add a default value or create an input for this
}

# File path for storing customer history
csv_file = "pricing_history.csv"


# Function to save data to CSV
def save_to_csv(customer_name, machine, price, time_logged_in):
    new_entry = pd.DataFrame(
        [
            {
                "Customer Name": customer_name,
                "Machine Type": machine,
                "Estimated Price (₦)": price,
                "Time Logged In": time_logged_in,
            }
        ]
    )

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
            mime="text/csv",
        )
