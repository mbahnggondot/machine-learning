import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
day_df = pd.read_csv('day.csv')
hour_df = pd.read_csv('hour.csv')

# Title of the Dashboard
st.title("Bike Sharing Dashboard")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select a Page", ["Home", "Correlation Heatmap", "Hourly Usage", "Weather Impact"])

# Home Page
if page == "Home":
    st.header("Welcome to the Bike Sharing Dashboard")
    st.write("""
    This dashboard provides insights into bike sharing patterns including:
    - Usage patterns based on time of day.
    - Impact of weather on bike rentals.
    """)
    
# Correlation Heatmap
elif page == "Correlation Heatmap":
    st.header("Correlation Heatmap of Bike Sharing Features")

    # Filter for numeric columns only
    numeric_cols = day_df.select_dtypes(include='number')
    
    # Create heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(numeric_cols.corr(), annot=True, cmap='coolwarm', fmt='.2f')
    st.pyplot(plt)

# Hourly Usage Analysis
elif page == "Hourly Usage":
    st.header("Hourly Bike Usage Pattern")
    
    # Calculate average hourly usage
    average_hourly_usage = hour_df.groupby('hr')['cnt'].mean()

    # Plotting
    plt.figure(figsize=(12, 6))
    sns.lineplot(x=average_hourly_usage.index, y=average_hourly_usage.values, marker='o')
    plt.title('Average Bike Usage Based on Time of Day')
    plt.xlabel('Hour of Day')
    plt.ylabel('Average Number of Rentals')
    plt.xticks(range(0, 24))
    plt.grid(True)
    st.pyplot(plt)
    
    # Display peak hour
    peak_hours = average_hourly_usage.idxmax()
    st.write(f"The hour with the highest bike usage: {peak_hours}:00")

# Weather Impact Analysis
elif page == "Weather Impact":
    st.header("Impact of Weather on Bike Rentals")
    
    # Select plot type
    plot_type = st.radio("Choose plot type:", ["Bar Plot", "Box Plot"])
    
    if plot_type == "Bar Plot":
        # Calculate average rentals per weather condition
        average_usage_weather = day_df.groupby('weathersit')['cnt'].mean()

        # Bar plot
        plt.figure(figsize=(10, 6))
        sns.barplot(x=average_usage_weather.index, y=average_usage_weather.values)
        plt.title('Average Bike Rentals Based on Weather Condition')
        plt.xlabel('Weather Condition')
        plt.ylabel('Average Number of Rentals')
        plt.xticks([0, 1, 2, 3], ['Clear', 'Mist', 'Light Snow/Rain', 'Heavy Rain/Snow'])
        st.pyplot(plt)

    elif plot_type == "Box Plot":
        # Boxplot
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=day_df, x='weathersit', y='cnt')
        plt.title('Impact of Weather on Bike Rentals')
        plt.xlabel('Weather Condition')
        plt.ylabel('Number of Rentals')
        plt.xticks([0, 1, 2, 3], ['Clear', 'Mist', 'Light Snow/Rain', 'Heavy Rain/Snow'])
        st.pyplot(plt)
    
    # Conclusion
    average_usage_weather = day_df.groupby('weathersit')['cnt'].mean()
    most_rentals_weather = average_usage_weather.idxmax()
    st.write(f"Weather condition with the highest number of rentals: {most_rentals_weather}")

