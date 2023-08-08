import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Apply custom styles to Streamlit
st.set_page_config(
    page_title="RAS Calculator",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Define custom CSS styles
st.markdown(
    """
    <style>
    .stButton button {
        background-color: #336699;
        color: white;
        font-weight: bold;
        border-radius: 8px;
    }
    .stButton button:hover {
        background-color: #114477;
    }
    .stSidebar {
        background-color: #f0f3f6;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Load your dataset
df = pd.read_excel('2023 CTL Boys Testing (version 1).xlsb (1).xlsx', sheet_name="(ALL)")

# Define the DataFrame statistics
attribute_stats = {
    'Height': (df['Height'].min(), df['Height'].max()),
    'Mass': (df['Mass'].min(), df['Mass'].max()),
    'SVJ': (df['SVJ'].min(), df['SVJ'].max()),
    'RunVJ_L': (df['RunVJ_L'].min(), df['RunVJ_L'].max()),
    'RunVJ_R': (df['RunVJ_R'].min(), df['RunVJ_R'].max()),
    '5m': (df['5m'].min(), df['5m'].max()),
    '10m': (df['10m'].min(), df['10m'].max()),
    '20m': (df['20m'].min(), df['20m'].max()),
    'Agil': (df['Agil'].min(), df['Agil'].max()),
    'YYIR2 Level': (df['YYIR2 Level'].min(), df['YYIR2 Level'].max()),
    'YYIR2 Distance': (df['YYIR2 Distance'].min(), df['YYIR2 Distance'].max())
}


def calculate_ras_score(height, mass, svj, run_vj_l, run_vj_r, sprint_5m, sprint_10m, sprint_20m, agility, yoyo_level, yoyo_distance):
    # Define the weightage criteria
    weightage = {
        'Height': 100,
        'Mass': 50,
        'SVJ': 100,
        'RunVJ_L': 50,
        'RunVJ_R': 50,
        '5m': 50,
        '10m': 50,
        '20m': 100,
        'Agil': 200,
        'YYIR2 Level': 150,
        'YYIR2 Distance': 100,
    }

    # Calculate the RAS score
    ras_score = (
        (height - attribute_stats['Height'][0]) / (attribute_stats['Height'][1] - attribute_stats['Height'][0]) * weightage['Height'] +
        (mass - attribute_stats['Mass'][0]) / (attribute_stats['Mass'][1] - attribute_stats['Mass'][0]) * weightage['Mass'] +
        (svj - attribute_stats['SVJ'][0]) / (attribute_stats['SVJ'][1] - attribute_stats['SVJ'][0]) * weightage['SVJ'] +
        (run_vj_l - attribute_stats['RunVJ_L'][0]) / (attribute_stats['RunVJ_L'][1] - attribute_stats['RunVJ_L'][0]) * weightage['RunVJ_L'] +
        (run_vj_r - attribute_stats['RunVJ_R'][0]) / (attribute_stats['RunVJ_R'][1] - attribute_stats['RunVJ_R'][0]) * weightage['RunVJ_R'] +
        ((sprint_5m + sprint_10m) - attribute_stats['5m'][0]) / (attribute_stats['5m'][1] - attribute_stats['5m'][0]) * weightage['5m'] +
        (sprint_20m - attribute_stats['20m'][0]) / (attribute_stats['20m'][1] - attribute_stats['20m'][0]) * weightage['20m'] +
        (agility - attribute_stats['Agil'][0]) / (attribute_stats['Agil'][1] - attribute_stats['Agil'][0]) * weightage['Agil'] +
        (yoyo_level - attribute_stats['YYIR2 Level'][0]) / (attribute_stats['YYIR2 Level'][1] - attribute_stats['YYIR2 Level'][0]) * weightage['YYIR2 Level'] +
        (yoyo_distance - attribute_stats['YYIR2 Distance'][0]) / (attribute_stats['YYIR2 Distance'][1] - attribute_stats['YYIR2 Distance'][0]) * weightage['YYIR2 Distance']
    )/100

    return round(ras_score,2)


def load_view():
    # User input for each feature
    col20, col21 = st.columns(2)
    with col20:
        st.title("RAS Calculator")
        st.write("Enter the values for each feature to calculate the RAS score.")
        with st.form(key='ras_form'):
            col1, col2, col3, col4, col5 = st.columns(5)
            height = col1.number_input("Height (cm)", min_value=1, max_value=220, value=172, step=1)  # Updated min_value, value, and step
            mass = col2.number_input("Mass (kg)", min_value=40, max_value=150, value=69, step=1)  # Updated min_value, value, and step
            svj = col3.number_input("SVJ", min_value=1, max_value=100, value=75, step=1)  # Updated min_value, value, and step
            run_vj_l = col4.number_input("RunVJ_L", min_value=10, max_value=450, value=96, step=1)  # Updated min_value, value, and step
            run_vj_r = col5.number_input("RunVJ_R", min_value=10, max_value=450, value=84, step=1)  # Updated min_value, value, and step

            col1, col2, col3 = st.columns(3)
            sprint_5m = col3.number_input("5m Sprint (s)", min_value=0.0, max_value=10.0, value=0.971, step=0.01)
            sprint_10m = col1.number_input("10m Sprint (s)", min_value=0.0, max_value=10.0, value=1.702, step=0.01)
            sprint_20m = col2.number_input("20m Sprint (s)", min_value=0.0, max_value=10.0, value=2.857, step=0.01)

            col1, col2, col3 = st.columns(3)
            agility = col3.number_input("Agility", min_value=0.0, max_value=20.0, value=8.0, step=0.1)
            yoyo_level = col1.number_input("YYIR2 Level", min_value=0.0, max_value=40.0, value=20.4, step=0.1)
            yoyo_distance = col2.number_input("YYIR2 Distance (m)", min_value=160, max_value=2000, value=600, step=10)

            submit_button = st.form_submit_button(label='Calculate RAS Score')

    with col21:
        st.title("RAS Score")
        # Calculate RAS score if the submit button is pressed
        if submit_button:

            # st.write("Values submitted:")
            # st.write(f"Height: {height}")
            # st.write(f"Mass: {mass}")
            # st.write(f"SVJ: {svj}")
            # st.write(f"RunVJ_L: {run_vj_l}")
            # st.write(f"RunVJ_R: {run_vj_r}")
            # st.write(f"5m Sprint: {sprint_5m}")
            # st.write(f"10m Sprint: {sprint_10m}")
            # st.write(f"20m Sprint: {sprint_20m}")
            # st.write(f"Agility: {agility}")
            # st.write(f"YYIR2 Level: {yoyo_level}")
            # st.write(f"YYIR2 Distance: {yoyo_distance}")


            # Calculate RAS score
            ras_score = calculate_ras_score(height, mass, svj, run_vj_l, run_vj_r, sprint_5m, sprint_10m, sprint_20m, agility, yoyo_level, yoyo_distance)

            # Display the RAS score plot
            colors = ['#4dab6d', "#72c66e", "#c1da64", "#f6ee54", "#fabd57", "#f36d54", "#ee4d55"]
            values = [10, 8, 7, 6, 5, 4, 3, 1]
            x_axis_vals = [0, 0.44, 0.88, 1.32, 1.76, 2.2, 2.64]
            fig = plt.figure(figsize=(10, 10))
            ax = fig.add_subplot(projection="polar")
            ax.bar(x=x_axis_vals, width=0.5, height=0.5, bottom=2, linewidth=3, edgecolor="white", color=colors, align="edge")

            arrow_idx = np.searchsorted(values[::-1], ras_score)  # Find the index in reversed values list
            arrow_idx = len(values) - arrow_idx  # Get the correct index in the original values list
            if arrow_idx <= 0 or arrow_idx >= len(x_axis_vals):
                if ras_score <= 1:
                    arrow_angle = np.deg2rad(x_axis_vals[0] * 180 / np.pi)  # Convert angle to radians
                else:
                    arrow_angle = np.deg2rad((x_axis_vals[-1] + x_axis_vals[-2]) / 2 * 180 / np.pi)  # Convert angle to radians
            else:
                arrow_angle = np.deg2rad((x_axis_vals[arrow_idx] + x_axis_vals[arrow_idx - 1]) / 2 * 180 / np.pi)  # Convert angle to radians

            arrow_length = 2.0  # Adjust this value to control the arrow length

            plt.annotate(str(ras_score), xytext=(0, 0), xy=(arrow_angle, arrow_length),
                         arrowprops=dict(arrowstyle="wedge, tail_width=0.5", color="black", shrinkA=0),
                         bbox=dict(boxstyle="circle", facecolor="black", linewidth=2.0),
                         fontsize=20, color="white", ha="center", weight="bold")

            plt.title("Performance Gauge Chart", loc="center", pad=20, fontsize=20, color="#ffffff")
            plt.gcf().set_size_inches(15, 25)
            ax.set_axis_off()
            st.pyplot(fig)


def main():
    load_view()


if __name__ == "__main__":
    main()