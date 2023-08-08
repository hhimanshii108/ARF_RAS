import streamlit as st
import pandas as pd
data = pd.read_excel('2023 CTL Boys Testing (version 1).xlsb (1).xlsx', sheet_name="(ALL)")

data['Full Name'] = data['First Name'] + ' ' + data['Surname']

df = pd.DataFrame(data)
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

# Function to display sorted DataFrame
def display_sorted_dataframe(df, sort_column=None, ascending=True):
    if sort_column:
        df = df.sort_values(by=sort_column, ascending=ascending)
    
    st.dataframe(df.style.highlight_max(axis=0))


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
    data = pd.read_excel('2023 CTL Boys Testing (version 1).xlsb (1).xlsx', sheet_name="(ALL)")

    data['Full Name'] = data['First Name'] + ' ' + data['Surname']

    df = pd.DataFrame(data)

    # Drop rows with NaN values in 'Club' and 'Position' columns
    df = df.dropna(subset=['Club', 'Position'])

    # Add a new column "ALL" to the 'Position' column
    df['Position (ALL)'] = df['Position']

    def filter_by_club_position(df, club, position):
        if position == 'ALL':
            return df[df['Club'] == club]
        return df[(df['Club'] == club) & (df['Position'] == position)]

    # Sidebar options
    clubs = df['Club'].unique()
    positions = df['Position'].unique().tolist()  # Convert to list to avoid modifying the original array
    positions.append('ALL')  # Add 'ALL' option at the end

    # App layout
    st.title('Player Details')

    # First Sidebar
    selected_club = st.sidebar.selectbox('Select Club', clubs)
    selected_position = st.sidebar.selectbox('Select Position', positions)

    # Filter data based on selected club and position
    filtered_df = filter_by_club_position(df, selected_club, selected_position)

    # Second Sidebar
    selected_name = st.sidebar.selectbox('Select Name', ['ALL'] + filtered_df['Full Name'].tolist())

    if selected_name != 'ALL':
        # Display the selected player's details
        selected_player = filtered_df[filtered_df['Full Name'] == selected_name].iloc[0]
        ras = calculate_ras_score(selected_player["Height"], selected_player["Mass"], selected_player["SVJ"],
                                  selected_player["RunVJ_L"], selected_player["RunVJ_R"],
                                  selected_player["5m"], selected_player["10m"], selected_player["20m"],
                                  selected_player["Agil"], selected_player["YYIR2 Level"], selected_player["YYIR2 Distance"])

        # Display the calculated RAS score for the selected player

        # Create a layout with 4 columns
        col1, col2, col3, col4 = st.columns(4)

        # Column 1: Name, Height, Mass
        col1.write(f'Name: {selected_player["Full Name"]}')
        col1.write(f'Height: {selected_player["Height"]}')
        col1.write(f'Mass: {selected_player["Mass"]}')

        # Column 2: SVJ, AbsRunVJ_L, AbsRunVJ_R
        col2.write(f'SVJ: {selected_player["SVJ"]}')
        col2.write(f'AbsRunVJ_L: {selected_player["AbsRunVJ_L"]}')
        col2.write(f'AbsRunVJ_R: {selected_player["AbsRunVJ_R"]}')

        # Column 3: 5m, 10m, 20m
        col3.write(f'5m: {selected_player["5m"]}')
        col3.write(f'10m: {selected_player["10m"]}')
        col3.write(f'20m: {selected_player["20m"]}')

        # Column 4: YOYO Level, YOYO Distance, Agil
        col4.write(f'YOYO Level: {selected_player["YYIR2 Level"]}')
        col4.write(f'YOYO Distance: {selected_player["YYIR2 Distance"]}')
        col4.write(f'Agil: {selected_player["Agil"]}')
        col4.write(f'RAS Score: {ras}', key='ras_score') 
        selected_player_df = pd.DataFrame(selected_player).T

        # Add the RAS Score to the DataFrame
        selected_player_df['RAS Score'] = ras
        st.write('**Selected Player:**')
        # Apply styling and display the DataFrame
        st.table(selected_player_df[['Full Name', 'Height', 'Mass', 'SVJ', 'AbsRunVJ_L', 'AbsRunVJ_R', '5m', '10m', '20m', 'YYIR2 Level', 'YYIR2 Distance', 'Agil', 'RAS Score']].style.set_precision(2).background_gradient().hide_index())
                # Display a table for selected players' details
        #st.table(pd.DataFrame(selected_player).T[['Full Name', 'Height', 'Mass', 'SVJ', 'AbsRunVJ_L', 'AbsRunVJ_R', '5m', '10m', '20m', 'YYIR2 Level', 'YYIR2 Distance', 'Agil','RAS Score']].style.set_precision(2).background_gradient().hide_index())

    else:
        # Display the table for all players
        st.write('**Filtered Players:**')
        filtered_df['RAS Score'] = filtered_df.apply(lambda row: calculate_ras_score(row['Height'], row['Mass'], row['SVJ'],
                                                                   row['RunVJ_L'], row['RunVJ_R'],
                                                                   row['5m'], row['10m'], row['20m'],
                                                                   row['Agil'], row['YYIR2 Level'], row['YYIR2 Distance']), axis=1)

        cell_hover = {
        'selector': 'td:hover',
        'props': [('color', 'black'), ('background-color', '#ffffb3')]
    }
        index_names = {
            'selector': '.index_name',
            'props': 'font-style: italic; color: darkgrey; font-weight:normal;'
        }
        headers = {
            'selector': 'th:not(.index_name)',
            'props': 'background-color: #ffffff; color: black;'
        }
        style_index = {
        'selector': '.index_name',
        'props': 'font-size: 16px; font-weight: bold;'
         }

        # Set styles for the rest of the data cells
        style_data = {
            'Full Name': '',
            'Height': 'font-size: 14px;',
            'Mass': 'font-size: 14px;',
            'SVJ': 'font-size: 14px;',
            'AbsRunVJ_L': 'font-size: 14px;',
            'AbsRunVJ_R': 'font-size: 14px;',
            '5m': 'font-size: 14px;',
            '10m': 'font-size: 14px;',
            '20m': 'font-size: 14px;',
            'YYIR2 Level': 'font-size: 14px;',
            'YYIR2 Distance': 'font-size: 14px;',
            'Agil': 'font-size: 14px;'
        }
        style_header = {
            'selector': 'thead th',
            'props': 'font-size: 18px; font-weight: bold; background-color: #000066; color: white;'
        }

        #df_style=filtered_df[['Full Name', 'Height', 'Mass', 'SVJ', 'AbsRunVJ_L', 'AbsRunVJ_R', '5m', '10m', '20m', 'YYIR2 Level', 'YYIR2 Distance', 'Agil']].style.set_precision(2).background_gradient(cmap="RdYlGn").hide_index()
        
        df_style = filtered_df[['Full Name', 'Height', 'Mass', 'SVJ', 'AbsRunVJ_L', 'AbsRunVJ_R', '5m', '10m', '20m', 'YYIR2 Level', 'YYIR2 Distance', 'Agil' , 'RAS Score']]
        df_style = df_style.style.set_precision(2)

        sort_column = st.selectbox('Sort by:', df_style.columns)
        sort_order = st.radio('Sort order:', ['Ascending', 'Descending'])

        ascending = True if sort_order == 'Ascending' else False

        # Sort the DataFrame
        sorted_df = df_style.data.sort_values(by=sort_column, ascending=ascending)

        # Apply additional styles
        for col, style in style_data.items():
            df_style = df_style.applymap(lambda _: style if col in df_style.columns else '', subset=col)

        # Apply background gradient cmap="RdYlGn" to specific columns
        cols_bg = ['Height', 'Mass', 'SVJ', 'AbsRunVJ_L', 'AbsRunVJ_R', 'YYIR2 Level', 'YYIR2 Distance', 'Agil',  'RAS Score']
        df_style = df_style.background_gradient(subset=cols_bg, cmap="RdYlGn")
        # Apply background gradient cmap="RdYlGn_r" to specific columns
        cols_bg_r = ['5m', '10m', '20m']
        df_style = df_style.background_gradient(subset=cols_bg_r, cmap="RdYlGn_r")

        # Hide the index
        df_style = df_style.hide_index()


        df_style.set_table_styles([style_header, style_index], axis=0)
        for col, style in style_data.items():
            df_style.set_table_styles([{ 'selector': f'.col_heading.col_heading_{col}', 'props': style }], axis=1)

        df_style =df_style.set_table_styles([cell_hover, index_names, headers])

        # Apply additional styles
        for col, style in style_data.items():
            df_style = df_style.applymap(lambda _: style if col in df_style.columns else '', subset=col)

        #st.table(df_style)
        # Apply additional styles to the sorted DataFrame
        styled_sorted_df = sorted_df.style
        for col, style in style_data.items():
            styled_sorted_df = styled_sorted_df.applymap(lambda _: style if col in styled_sorted_df.columns else '', subset=col)
        
        # Apply background gradients
        cols_bg = ['Height', 'Mass', 'SVJ', 'AbsRunVJ_L', 'AbsRunVJ_R', 'YYIR2 Level', 'YYIR2 Distance', 'Agil', 'RAS Score']
        styled_sorted_df = styled_sorted_df.background_gradient(subset=cols_bg, cmap="RdYlGn")

        cols_bg_r = ['5m', '10m', '20m']
        styled_sorted_df = styled_sorted_df.background_gradient(subset=cols_bg_r, cmap="RdYlGn_r")
        styled_sorted_df = styled_sorted_df.set_precision(2)
        # Display the styled and sorted DataFrame
        #st.write('**Filtered Players:**')
        st.table(styled_sorted_df)

        

def main():
    load_view()

if __name__ == "__main__":
    main()
