import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

class NutritionalEvaluator:
    def __init__(self, file_path):
        # Initialize with the path to the dataset
        self.file_path = file_path
        self.data = self.load_dataset()
        # Coefficients for different nutritional factors
        self.P_factor = 1  # Protein
        self.F_factor = 1  # Dietary Fiber
        self.S_factor = -1  # Sugars
        self.AS_factor = -1  # Added Sugars
        self.C_factor = -1  # Cholesterol
        self.Na_factor = -1  # Sodium
        self.TF_factor = -1  # Total Fat
        self.SF_factor = -1  # Saturated Fat
        self.TRF_factor = -1  # Trans Fat

    def load_dataset(self):
        # Load the dataset from the provided CSV file
        return pd.read_csv(self.file_path)

    def calculate_score(self, protein, fiber, sugars, added_sugars, cholesterol, sodium, total_fat, saturated_fat, trans_fat):
        # Calculates the nutritional score of a product
        score = (self.P_factor * protein) + (self.F_factor * fiber) + (self.S_factor * sugars) + \
                (self.AS_factor * added_sugars) + (self.C_factor * cholesterol) + (self.Na_factor * sodium) + \
                (self.TF_factor * total_fat) + (self.SF_factor * saturated_fat) + (self.TRF_factor * trans_fat)
        return score

    def evaluate_product(self, score):
        # Evaluates the product based on its nutritional score
        if score > 75:
            return 'Excellent Choice'
        elif score > 25:
            return 'Good Choice'
        elif score > 0:
            return 'Moderate Choice'
        elif score < 0 and score > -25:
            return 'Poor Choice'
        elif score < -25 and score > -75:
            return 'Unhealthy Choice'
        elif score < -75:
            return 'Worst Choice'
        else:
            return 'Bad Choice'

    def display_score_bar(self, score):
        # Displays the nutritional score on a bar chart
        fig, ax = plt.subplots(figsize=(5, 2))
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
    

    def evaluate_all_products(self):
        # Evaluate and display the score for each product in the dataset
        for index, row in self.data.iterrows():
            score = self.calculate_score(row['Protein(g)'], row['Dietary Fiber(g)'], row['Sugars(g)'],
                                         row['Added Sugars(g)'], row['Cholesterol(g)'], row['Sodium(g)'],
                                         row['Total Fat(g)'], row['Saturated Fat(g)'], row['Trans Fat(g)'])
            print(f"Product: {row['Name of the Product']}, Score: {score}, Evaluation: {self.evaluate_product(score)}")
            fig = self.display_score_bar(score)
            plt.show(fig)
            
    
    

