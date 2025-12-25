"""
This streamlit application generates a large dataset
containing random numbers and visualizes the data.
"""

# Standard Imports
import time

# Third-party Imports
import streamlit as st

# Local Application Imports
from src.utils import get_logger, simulate_large_dataset

logger = get_logger()

if __name__ == "__main__":

    st.title("Streamlit Data Visualization")

    with st.spinner("Loading large dataset..."):

        start = time.time()

        # Generate dataset
        logger.info("Generating large dataset...")
        df = simulate_large_dataset()
        logger.info("Dataset loaded successfully")

        load_time = time.time() - start

    st.success(f"Dataset loaded successfully in {load_time:.2f} seconds")

    # Show dataset preview
    st.subheader("📄 Dataset Preview")
    st.dataframe(df.head())

    # Select column to plot
    column = st.selectbox("Select a column to plot:", df.columns)

    st.subheader(f"📈 Line Chart of {column}")
    st.line_chart(df[column])

    st.subheader(f"📊 Bar Chart of {column}")
    st.bar_chart(df[column])
