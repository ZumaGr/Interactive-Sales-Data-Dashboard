import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the page configuration
st.set_page_config(
    page_title="Sales Data Dashboard",
    layout="wide",
)

# Title of the app
st.title("Interactive Sales Data Dashboard")

# Sidebar for user inputs
st.sidebar.header("Upload your CSV data")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

# Load dataset
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("data/sales_data.csv")

# Display dataset preview
st.subheader("Dataset Preview")
st.dataframe(df)

# Filter by region
regions = df['Region'].unique().tolist()
selected_regions = st.sidebar.multiselect("Select regions", regions, default=regions)

# Filter by product
products = df['Product'].unique().tolist()
selected_products = st.sidebar.multiselect("Select products", products, default=products)

# Filter data based on selections
filtered_df = df[(df['Region'].isin(selected_regions)) & (df['Product'].isin(selected_products))]

# Show summary statistics
st.subheader("Summary Statistics")
st.write(filtered_df.describe())

# Sales over time
st.subheader("Sales Over Time")
filtered_df['OrderDate'] = pd.to_datetime(filtered_df['OrderDate'])
sales_over_time = filtered_df.groupby('OrderDate')['Sales'].sum().reset_index()

plt.figure(figsize=(10, 5))
sns.lineplot(data=sales_over_time, x='OrderDate', y='Sales')
plt.title('Sales Over Time')
plt.xticks(rotation=45)
st.pyplot(plt)

# Sales by Region
st.subheader("Sales by Region")
sales_by_region = filtered_df.groupby('Region')['Sales'].sum().reset_index()

plt.figure(figsize=(10, 5))
sns.barplot(data=sales_by_region, x='Region', y='Sales')
plt.title('Sales by Region')
st.pyplot(plt)

# Sales by Product
st.subheader("Sales by Product")
sales_by_product = filtered_df.groupby('Product')['Sales'].sum().reset_index()

plt.figure(figsize=(10, 5))
sns.barplot(data=sales_by_product, x='Product', y='Sales')
plt.title('Sales by Product')
st.pyplot(plt)
