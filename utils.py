import numpy as np
import plotly.figure_factory as ff
import plotly.express as px
import streamlit as st


def display_dataframe(dataframe, column):
    column.write("### Details of the data")
    column.dataframe(dataframe)


def display_basic_statistics(dataframe, column):
    column.write("### Basic Statistics")
    column.write(dataframe.describe())


def display_stats(dataframe):
    col1, col2 = st.columns(2)
    display_dataframe(dataframe, col1)
    display_basic_statistics(dataframe, col2)


def display_diagrams(dataframe):
    # selecting numeric inputs
    numeric_data = dataframe.select_dtypes(include=np.number)
    display_correlation(numeric_data)


def display_correlation(dataframe, column):
    correlation_matrix = dataframe.corr()

    column.write("### Correlation Heatmap")
    fig = px.imshow(correlation_matrix, text_auto=True, width=1200, height=768)
    column.plotly_chart(fig, use_container_width=True)


def display_user_choice(dataframe):
    numeric_data = dataframe.select_dtypes(include=np.number)
    col1, col2 = st.columns(2)
    col1.write('### Parameter wise dist plot')
    param1 = col1.selectbox(
        '# Select the parameter',
        numeric_data.columns
    )
    data_param1 = dataframe[param1]
    hist_data = [data_param1]
    group_labels = [param1]
    fig = ff.create_distplot(
        hist_data, group_labels=group_labels, bin_size=[.2]
    )

    col1.plotly_chart(fig, use_container_width=True)
    display_correlation(numeric_data, col2)
