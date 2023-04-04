# --- Import libraries ---
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# --- set page configuration ---
st.set_page_config(page_title = 'College Dashboard', page_icon = ':school:')

# --- read in data
df = pd.read_csv('data.csv', index_col=0)

# --- set side bar configuration & table filtering backend ---

with st.sidebar:
    # ---filter config---
    st.header("Filter Options:")

    cols_of_choice = st.multiselect(
        'Select the columns to appear:',
        options = list(df.columns),
        default = ['College Name', 'Total Enrollment', 'Graduation Rate','College Type']
    )

    search_cols = st.multiselect(
        'Select the search criteria, type the desired value(s) and press enter to filter',
        options = df.columns.tolist(),
    )

    for col in search_cols:

        if col not in cols_of_choice:
            cols_of_choice.append(col)

        if col not in ['College Name','State', 'State abbreviation','College Type','Degree Length']:
            
            # set search options for quantitative, continuous columns
            search_type = st.selectbox(
            f'{col}  filter type:',
            options = ['max', 'min', 'within range', 'greater than','lesser than','equal to']
            )

            if search_type == 'greater than' or search_type == 'lesser than':
                val = st.number_input(f"Value to compare the {col} values to:", value = int(df[col].mean()))
                if search_type == 'greater than': df = df[df[col] > val]
                else:df = df[df[col] < val]

            elif search_type == 'max' or search_type == 'min':
                if search_type == 'max': val = df[col].max()
                else: val = df[col].min()
                df = df[df[col] == val]

            elif search_type == 'within range':
                min_val = st.number_input(f"Minimum value for {col}:", value = int(df[col].min()))
                max_val = st.number_input(f"Maximum value for {col}:", value = int(df[col].max()))
                df = df[(df[col] > min_val) & (df[col] < max_val)]
                
            elif search_type == 'equal to':
                val = st.number_input(f"Value to compare the {col} values to:", value = int(df[col].mean()))
                df = df[df[col] == val]

        # set search options for discrete columns
        elif col == 'College Name':
            schools = st.multiselect(f"Select the values to include for {col}s:",options = df[col].unique())
            df = df[df['College Name'].isin(schools)]
        else: 
            options = st.multiselect(f"Select the values to include for {col}:",options = df[col].unique())
            df = df.query(f'{col} == @options')
    
    # --- visualization config ---
    st.header('Visualization Options:')
    y_val = st.selectbox(
            'Select a metric to visualize:',
            options = [col for col in df.columns.tolist() if col not in ['College Name','State','State abbreviation', 'College Type', 'Degree Length']]
        )
    
    vis_type = st.radio(
        'Select a visualization type:',
        ('Bar Graph', 'Pie Chart')
    )
    st.write('More visualization types coming soon!')


# --- Main body configuration ---
top_part = st.container()
bottom_part = st.container()

with top_part:
    
    st.header(':closed_book: College Dashboard :blue_book:')
    st.write('Use the sidebar on the left to change the dashboard and visualization options.')
    st.dataframe(df[cols_of_choice].set_index('College Name'))

with bottom_part:

    st.header(':chart_with_upwards_trend: Visualization :chart_with_downwards_trend:')
    st.write(f'{vis_type} of {y_val}')
    fig = plt.figure()

    if vis_type == 'Bar Graph':
        try: sns.barplot(data = df, x = 'College Name', y = y_val)
        except ValueError: st.write('Missing values for visualization...')
        if len(df) > 10: plt.xticks(rotation = 90)
        else: plt.xticks(rotation = 45)

    elif vis_type == 'Pie Chart':
        try: plt.pie(df[y_val].values.tolist(), labels = df['College Name'].values.tolist())
        except ValueError: st.write('Missing values for visualization...')

    try:st.pyplot(fig)
    except ValueError: st.write('Missing values for visualization...')
    
    st.markdown('''See the following links for data sources: [US College tuition diversity & pay](https://www.kaggle.com/datasets/jessemostipak/college-tuition-diversity-and-pay) , 
                [US College statistical data](https://www.kaggle.com/datasets/yashgpt/us-college-data?resource=download)''')