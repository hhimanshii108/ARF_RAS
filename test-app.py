import streamlit as st
import pandas as pd

# Sample data
data = {
    'Full Name': ['Alice', 'Bob', 'Charlie'],
    'Height': [170, 180, 160],
    'Mass': [65, 75, 70],
    'SVJ': [30, 35, 28],
    'AbsRunVJ_L': [5, 6, 4],
    'AbsRunVJ_R': [5, 6, 4],
    '5m': [2, 3, 2.5],
    '10m': [4, 5, 4.2],
    '20m': [7, 8, 6],
    'YYIR2 Level': [9, 8, 10],
    'YYIR2 Distance': [100, 110, 95],
    'Agil': [12, 15, 10],
    'RAS Score': [80, 90, 85]
}

# Sample style data
style_data = {
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
    'Agil': 'font-size: 14px;',
    'RAS Score': 'font-size: 14px;'
}

# Streamlit app
def main():
    st.title('Sortable and Styled DataFrame in Streamlit')

    # Sample DataFrame
    filtered_df = pd.DataFrame(data)

    # Sorting
    sort_column = st.selectbox('Sort by:', filtered_df.columns)
    sort_order = st.radio('Sort order:', ['Ascending', 'Descending'])

    ascending = True if sort_order == 'Ascending' else False

    sorted_df = filtered_df.sort_values(by=sort_column, ascending=ascending)

    # Apply additional styles to the sorted DataFrame
    styled_sorted_df = sorted_df.style
    for col, style in style_data.items():
        styled_sorted_df = styled_sorted_df.applymap(lambda _: style if col in styled_sorted_df.columns else '', subset=col)
    
    # Apply background gradients
    cols_bg = ['Height', 'Mass', 'SVJ', 'AbsRunVJ_L', 'AbsRunVJ_R', 'YYIR2 Level', 'YYIR2 Distance', 'Agil', 'RAS Score']
    styled_sorted_df = styled_sorted_df.background_gradient(subset=cols_bg, cmap="RdYlGn")

    cols_bg_r = ['5m', '10m', '20m']
    styled_sorted_df = styled_sorted_df.background_gradient(subset=cols_bg_r, cmap="RdYlGn_r")

    # Display the styled and sorted DataFrame
    st.write('**Filtered Players:**')
    st.table(styled_sorted_df)

if __name__ == '__main__':
    main()





