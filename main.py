import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from evaluator import NutritionalEvaluator
import plotly.express as px

# Custom theme for the app
st.set_page_config(layout="wide", page_title="NutriVision", page_icon="🥗")
st.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Path to the CSV file
file_path = 'Dataset2.csv'

# Initialize the NutritionalEvaluator with the dataset
evaluator = NutritionalEvaluator(file_path)

# Streamlit app title
st.markdown('<h1 style="font-size: 48px;">🥗 NutriVision: Transforming Dietary Habits</h1>', unsafe_allow_html=True)

# Sidebar for category selection and product search
with st.sidebar:
    # Custom font size for markdown text in sidebar
    st.markdown('<p style="font-size: 25px;">📚 Select a Category and Search for Products</p>', unsafe_allow_html=True)
    categories = evaluator.data['Category'].unique().tolist()
    selected_category = st.selectbox('Category:', categories)
    user_input = st.text_input("🔍 Search for a Product").lower()

# Displaying products based on selected category and user search input
filtered_data = evaluator.data[evaluator.data['Category'] == selected_category]
if user_input:
    # Filter product names based on user input
    product_names = [name for name in filtered_data['Name of the Product'].tolist() if user_input in name.lower()]
else:
    # If no input is given, display all products in the selected category
    product_names = filtered_data['Name of the Product'].tolist()

selected_product = st.selectbox('Select a Product:', product_names)
# Function to plot and display the bar chart in Streamlit
def display_score_bar(score):
    fig, ax = plt.subplots(figsize=(20, 2))
    cmap = plt.get_cmap('RdYlGn')
    norm = plt.Normalize(-100, 100)
    plt.barh([0], score, color=cmap(norm(score)), edgecolor='black')
    plt.xlim(-100, 100)
    plt.axvline(0, color='grey', linewidth=0.8)
    plt.yticks([])
    plt.xticks(np.arange(-100, 101, 25))
    plt.xlabel('Score', fontsize=12)
    plt.title('Nutritional Score', fontsize=14)
    plt.grid(axis='x', linestyle='--', alpha=0.6)
    return fig

# Displaying products based on selected category
filtered_data = evaluator.data[evaluator.data['Category'] == selected_category]
product_names = filtered_data['Name of the Product'].tolist()


# Display the selected product's nutritional evaluation
if selected_product:
    product_data = filtered_data[filtered_data['Name of the Product'] == selected_product].iloc[0]
    score = evaluator.calculate_score(product_data['Protein(g)'], product_data['Dietary Fiber(g)'], product_data['Sugars(g)'],
                                      product_data['Added Sugars(g)'], product_data['Cholesterol(g)'], product_data['Sodium(g)'],
                                      product_data['Total Fat(g)'], product_data['Saturated Fat(g)'], product_data['Trans Fat(g)'])
    evaluation = evaluator.evaluate_product(score)
    nutrients = ['Protein(g)', 'Dietary Fiber(g)', 'Sugars(g)', 'Added Sugars(g)', 'Cholesterol(g)', 'Sodium(g)', 'Total Fat(g)', 'Saturated Fat(g)', 'Trans Fat(g)']
    quantities = [product_data[nutrient] for nutrient in nutrients]
    st.markdown(f"<p class='big-font'>Evaluation: {evaluation}</p>", unsafe_allow_html=True)
    
    # Display the bar chart
    fig = display_score_bar(score)
    st.pyplot(fig)

    # Create two columns for the pie chart and the scatter plot
    col1,col2 = st.columns(2)

    # Pie Chart for Nutrient Distribution
    with col1:
        # Create a pie chart with Plotly for nutrient distribution
        filtered_nutrients = {nutrient: product_data[nutrient] for nutrient in nutrients if product_data[nutrient] > 0}
        if filtered_nutrients:
            fig = px.pie(names=filtered_nutrients.keys(), values=filtered_nutrients.values(),
                        title=f'Nutrient Distribution in {selected_product}', hole=0.4)
            fig.update_layout(width=720, height=800)  # Adjust size for column layout
            st.plotly_chart(fig)
        else:
            st.markdown("<p class='big-font'>No nutrient data available for the selected product.</p>", unsafe_allow_html=True)


# Scatter Plot for Protein vs. Fat Comparison
    with col2:
        # Create the Protein vs. Fat Comparison Chart for the selected category with adjusted size
        fig = px.scatter(filtered_data, x='Total Fat(g)', y='Protein(g)', hover_data=['Name of the Product'],
                        title=f'Protein vs. Fat in {selected_category} Products',
                        labels={'Total Fat(g)': 'Total Fat (g)', 'Protein(g)': 'Protein (g)'})
        fig.update_layout(width=720, height=800)  # Adjust size for column layout
        st.plotly_chart(fig)

