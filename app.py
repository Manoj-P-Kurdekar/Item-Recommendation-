import streamlit as st
import pickle
import pandas as pd

# Load the preprocessed data from the pickle file
with open('preprocessed_data.pkl', 'rb') as f:
    preprocessed_data = pickle.load(f)

# Convert 'InvoiceDate' column to datetime with the correct format
preprocessed_data['InvoiceDate'] = pd.to_datetime(preprocessed_data['InvoiceDate'], format='%d-%m-%Y')

# Add a logo at the top-center alignment with a size of 85x105
logo_image = st.image("online_store.png", use_column_width=False, width=85)
st.subheader("Welcome to the Item Recommendation App")

# Set a title for your app
st.title("Item Recommendation")

# Get user inputs for CustomerID and Date
customer_id = st.text_input('Enter CustomerID:')
start_date = pd.to_datetime('2010-01-01').date()  # Set your desired start date here
end_date = pd.to_datetime('2011-12-31').date()  # Set your desired end date here

# Set the default date within the range or let the user choose
default_date = pd.to_datetime('2010-01-01').date()  # You can set a different default date here

date = st.date_input('Enter Date (between 2010-01-01 and 2011-12-31):', 
                     min_value=start_date, max_value=end_date, value=default_date)

# Check if the user-selected date is within the range
if start_date <= date <= end_date:
    # Validate customer_id is a non-empty string containing only digits
    if customer_id.isdigit() and len(customer_id) > 0:
        customer_id = int(customer_id)
        # Filter the preprocessed data based on user inputs
        filtered_data = preprocessed_data[(preprocessed_data['CustomerID'] == customer_id) & (preprocessed_data['InvoiceDate'].dt.date == date)]

        # Display the recommended descriptions
        if not filtered_data.empty:
            st.write(filtered_data['Description'].unique())
        else:
            st.write('No recommendations found.')
    else:
        st.write('Please enter a valid CustomerID (non-empty string containing only digits).')
else:
    st.write('Please select a date within the range 2010-01-01 to 2011-12-31.')
