# import streamlit as st

# def load_view():    
#     st.title('About Page')
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
import os

col1, col2 = st.columns(2)
with col1:
    def load_view(): 
        def plot_bar_chart(df, x_column, y_column, ax):
            if df[y_column].dtype == 'object':  # If the y-axis column is categorical
                sns.countplot(x=y_column, data=df, ax=ax)
            else:  # If the y-axis column is numeric
                sns.barplot(x=y_column, y=x_column, data=df, ax=ax)
                #ax.set_xscale('log')  # Set X-axis scale to logarithmic for numeric columns
            min_value = df[y_column].min()*0.95
            max_value = df[y_column].max()*1.01
            ax.set_xlim(min_value, max_value)
            # Add numeric values (x-axis values) on top of each bar
            for i, v in enumerate(df[y_column]):
                ax.text(v, i, str(v), ha='left', va='center', fontsize=10, color='black')

            ax.set_xlabel(y_column)
            ax.set_ylabel(x_column)
            ax.set_title(f'Bar Chart: {y_column} vs {x_column}')
            ax.tick_params(axis='y', rotation=0)
            ax.tick_params(axis='x', colors='black')


            ax.set_xlabel(y_column)
            ax.set_ylabel(x_column)
            ax.set_title(f'Bar Chart: {y_column} vs {x_column}')
            ax.tick_params(axis='y', rotation=0)
            ax.tick_params(axis='x', colors='black')

            ax.set_xlabel(y_column)
            ax.set_ylabel(x_column)
            ax.set_title(f'Bar Chart: {y_column} vs {x_column}')
            ax.tick_params(axis='y', rotation=0)
            ax.tick_params(axis='x', colors='black')

        # Load your dataset
        data = pd.read_excel('2023 CTL Boys Testing (version 1).xlsb (1).xlsx', sheet_name="(ALL)")

        # Add a new column "Full Name" by combining "First Name" and "Surname"
        data['Full Name'] = data['First Name'] + ' ' + data['Surname']

        # Sidebar for column selection
        st.sidebar.header('Column Selection')
        y_column = st.sidebar.selectbox('Choose Y-axis Column', ['Height', 'Mass', 'Reach', 'SVJ', 'AbsRunVJ_L', 'AbsRunVJ_R', '5m', '10m', '20m', 'Agil', 'YYIR2 Level', 'YYIR2 Distance'])

        # Display the selected columns in the main area
        st.title('Top 20 Players by Selected Y-axis Column')
        st.write(f'Selected Y-axis Column: {y_column}')

        # Create a subset and sort by the selected Y-axis column
        subset_data = data[['Full Name', y_column]].sort_values(by=y_column, ascending=False).head(21)
        subset_data = subset_data.dropna()
        #subset_data = subset_data.drop(columns='ID No.')

        # Create the figure and axes using plt.subplots()
        fig, ax = plt.subplots(figsize=(9, 5))

        # Plot the bar chart using the plot_bar_chart function
        plot_bar_chart(subset_data, 'Full Name', y_column, ax)
        
        # Display the plot using Streamlit
        if st.button('Save Chart as Image'):
            # Save the bar chart as an image in the "photos" folder
            if not os.path.exists("photos"):
                os.makedirs("photos")
            file_name = f"photos/bar_chart_{y_column}.png"
            plt.savefig(file_name)
            st.write(f"Bar chart saved as {file_name}")
        
        st.pyplot(fig)
        # subset_data.index=range(1,21)
        df_style=subset_data.style.set_precision(2)
        st.table(df_style)
def main():
    load_view()
