import pandas as pd
from surprise import Dataset, Reader, KNNBasic
import pickle

# Load and preprocess the dataset
df = pd.read_excel(r"C:\Users\manoj\OneDrive - Zoro\Desktop\Work\ResolutionAI.in\Dataset\Dataset for Task 1,2,3\Online Retail.xlsx")
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], format='%d/%m/%Y')
df['CustomerID'] = pd.to_numeric(df['CustomerID'], errors='coerce')

# Initialize lists to store inputs and recommendations
customer_ids = []
dates = []
recommendations = []

while True:
    # Take inputs from the user
    customer_id = input("Enter Customer ID (or 'done' to finish): ")
    if customer_id.lower() == 'done':
        break
    
    date_str = input("Enter Date (dd-mm-yyyy): ")
    date = pd.to_datetime(date_str, format='%d-%m-%Y')
    
    # Filter the dataset based on the user inputs
    filtered_df = df.copy()
    if customer_id:
        filtered_df = filtered_df[filtered_df['CustomerID'] == int(customer_id)]
    if date_str:
        filtered_df = filtered_df[filtered_df['InvoiceDate'].dt.date == date.date()]

    # Train a collaborative filtering model
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(filtered_df[['CustomerID', 'Description', 'Quantity']], reader)
    model = KNNBasic(sim_options={'user_based': False})
    trainset = data.build_full_trainset()
    model.fit(trainset)

    # Generate recommendations based on the filtered dataset
    for item_id in filtered_df['Description'].unique():
        item_inner_id = trainset.to_inner_iid(item_id)
        item_neighbors = model.get_neighbors(item_inner_id, k=5)
        item_neighbors = [trainset.to_raw_iid(inner_id) for inner_id in item_neighbors]
        recommendations.extend(item_neighbors)

    # Print the recommendations
    print("Recommended Item Descriptions:")
    for item_description in set(recommendations):
        print(item_description)
    
    # Append inputs and clear recommendations for the next iteration
    customer_ids.append(int(customer_id))
    dates.append(date)
    recommendations.clear()

# Print all the inputs and recommendations
print("Inputs and Recommendations:")
for i in range(len(customer_ids)):
    print(f"Customer ID: {customer_ids[i]}, Date: {dates[i]}, Recommendations: {set(recommendations)}")

with open("preprocessed_data.pkl", "wb") as f:
    pickle.dump(df, f)