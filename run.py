import streamlit as st
import pandas as pd

import utils

st.set_page_config(layout='wide')


def main():
    st.title("Data Analyzer")

    # Create a file uploader widget
    uploaded_file = st.file_uploader("Please upload the dataset (preferably in csv or excel format)",
                                     type=["csv", "xlsx"], accept_multiple_files=False)

    # Check if a file has been uploaded

    try:
        if uploaded_file is not None:
            st.success("Here are the details!")

            display_df = None

            if uploaded_file.type == "text/xlsx":
                display_df = pd.read_excel(uploaded_file)

            elif uploaded_file.type == "text/csv":
                display_df = pd.read_csv(uploaded_file)

            if display_df is not None:

                utils.display_stats(display_df)
                display_df.dropna(inplace=True)
                utils.display_user_choice(dataframe=display_df)
            else:
                st.write("Unable to display information from the csv file")
    except Exception:
        st.error("The given file cannot be parsed for analysis. Please use another file.")


if __name__ == "__main__":
    main()
