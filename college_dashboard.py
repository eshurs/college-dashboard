# --- Import libraries ---
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import io

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
        elif col == 'College Name' or col == 'College Type':
            options = st.multiselect(f"Select the values to include for {col}s:",options = df[col].unique())
            df = df[df[col].isin(options)]
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

# --- Main body configuration ---
top_part = st.container()
middle_part = st.container()
bottom_part = st.container()
with top_part:
    
    st.header(':closed_book: College Dashboard :blue_book:')
    st.subheader('_Use the sidebar on the left to change the dashboard and visualization options._')
    st.dataframe(df[cols_of_choice].set_index('College Name'))

with middle_part:
    
    st.header(':chart_with_upwards_trend: Visualization :chart_with_downwards_trend:')
    st.write(f'{vis_type} of {y_val}')
    fig = plt.figure()

    if vis_type == 'Bar Graph':
        try: sns.barplot(data = df, x = 'College Name', y = y_val)
        except ValueError: st.write('Missing values for visualization...')
        if len(df) > 10: 
            plt.xticks(rotation = 90)
            plt.subplots_adjust(bottom=0.55)
        else: plt.xticks(rotation = 45)

    elif vis_type == 'Pie Chart':
        vals = df[y_val].values.tolist()
        labs = df['College Name'].values.tolist()
        labs = [i + '-'+str(vals[labs.index(i)]) for i in labs]
        try: plt.pie(vals, labels = labs)
        except ValueError: st.write('Missing values for visualization...')

    plt.title(f'{y_val}')
    try:st.pyplot(fig)
    except ValueError: st.write('Missing values for visualization...')
    
    state = st.session_state
    if 'num_figs' not in state:
        state.num_figs = 0
    if 'figs' not in state:
        state.figs = []

    if st.button('Store figure'):
        state.num_figs +=1
        f = io.BytesIO()
        plt.savefig(f, format="png")
        state.figs.append(f)
        st.write(state.num_figs)

    st.subheader('Stored Figures:')

    for img in state.figs:
        st.image(img, output_format= 'PNG', caption = f'Figure {state.figs.index(img)+1}')

    if st.button('Clear figures'):
        del state.num_figs
        del state.figs
    

with bottom_part:
    st.header('Sources')
    st.markdown('See the following links for code and data sources:')
    st.markdown('- [Github repository](https://github.com/eshurs/college-dashboard)')
    st.markdown(' - [US College tuition diversity & pay](https://www.kaggle.com/datasets/jessemostipak/college-tuition-diversity-and-pay)')
    st.markdown('- [US College statistical data](https://www.kaggle.com/datasets/yashgpt/us-college-data?resource=download)') 
