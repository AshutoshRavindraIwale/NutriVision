import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from evaluator import NutritionalEvaluator

# Path to the CSV file
file_path = 'Dataset2.csv'

# Initialize the NutritionalEvaluator with the dataset
evaluator = NutritionalEvaluator(file_path)

# Streamlit app title
st.title('NutriVision: Nutritional Evaluation')

# Function to plot and display the bar chart in Streamlit
def display_score_bar(score):
    fig, ax = plt.subplots(figsize=(10, 2))
    cmap = plt.get_cmap('RdYlGn')
    norm = plt.Normalize(-100, 100)
    plt.barh([0], score, color=cmap(norm(score)), edgecolor='black')
    plt.xlim(-100, 100)
    plt.axvline(0, color='grey', linewidth=0.8)
    plt.yticks([])
    plt.xticks(np.arange(-100, 101, 25))
    plt.xlabel('Score')
    plt.title('Nutritional Score')
    plt.grid(axis='x', linestyle='--', alpha=0.6)
    return fig

# Step 1: Allow users to select a category
categories = evaluator.data['Catergory'].unique().tolist()
selected_category = st.selectbox('Select a Category:', categories)

# Step 2: Allow users to select a product from the chosen category
filtered_data = evaluator.data[evaluator.data['Catergory'] == selected_category]
product_names = filtered_data['Name of the Product'].tolist()
selected_product = st.selectbox('Select a Product:', product_names)

# Display the selected product's nutritional evaluation
if selected_product:
    product_data = filtered_data[filtered_data['Name of the Product'] == selected_product].iloc[0]
    score = evaluator.calculate_score(product_data['Protein(g)'], product_data['Dietary Fiber(g)'], product_data['Sugars(g)'],
                                      product_data['Added Sugars(g)'], product_data['Cholesterol(g)'], product_data['Sodium(g)'],
                                      product_data['Total Fat(g)'], product_data['Saturated Fat(g)'], product_data['Trans Fat(g)'])
    evaluation = evaluator.evaluate_product(score)
    st.write(f"**Evaluation:** {evaluation}")
    
    # Display the bar chart
    fig = display_score_bar(score)
    st.pyplot(fig)


