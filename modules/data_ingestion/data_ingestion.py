import pandas as pd
import requests
import streamlit as st

# Example: CDC Wonder open data, MIMIC demo CSV, etc.
REPUTABLE_SOURCES = [
    # Real world, but for demo: CDC Wonder, openICPSR, NHS Digital, etc.
    "https://raw.githubusercontent.com/datablist/sample-csv-files/main/files/people/people-100.csv"
]

def download_public_data(url):
    try:
        response = requests.get(url, timeout=8)
        response.raise_for_status()
        data = pd.read_csv(pd.compat.StringIO(response.text))
        st.success(f"Fetched data from: {url}")
        return data
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")
        return None

def sanitize_data(df):
    # Example: Drop columns with too many missing values, enforce dtypes, basic range checks
    if df is None or df.empty:
        st.warning("No data to sanitize.")
        return None
    df = df.dropna(axis=1, thresh=int(0.75 * len(df)))
    # (Add enterprise-level validation here: range checks, outlier filtering, label noise checks)
    return df

def data_ingestion_ui():
    st.header("Enterprise Data Ingestion (Demo)")
    url = st.selectbox("Choose trusted public data source", REPUTABLE_SOURCES)
    if st.button("Download & Preview Data"):
        data = download_public_data(url)
        clean_data = sanitize_data(data)
        if clean_data is not None:
            st.write("Preview of sanitized data:")
            st.dataframe(clean_data.head(20))
            # Optionally: Save for later ML training, or export
            st.download_button(
                "Download Cleaned Data (CSV)",
                clean_data.to_csv(index=False).encode("utf-8"),
                "clean_data.csv"
            )
