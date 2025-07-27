import streamlit as st
import pandas as pd
import requests
import os

REPUTABLE_SOURCES = [
    # Small demo (replace with real ED/health data as needed)
    "https://raw.githubusercontent.com/datablist/sample-csv-files/main/files/people/people-100.csv",
    # CDC: US National Notifiable Diseases Surveillance System (NNDSS) (demo sample)
    "https://data.cdc.gov/api/views/x8jf-txib/rows.csv?accessType=DOWNLOAD",
    # OpenICPSR: Synthetic EHR Dataset (hospital records)
    "https://www.openicpsr.org/openicpsr/project/147964/file/download?fileId=601917&type=project",
    # UCI: Heart Disease Data (health ML demo)
    "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data",
    # WHO: COVID-19 Global Data (cleaned)
    "https://covid19.who.int/WHO-COVID-19-global-data.csv",
    # UK NHS: AE Attendances and Emergency Admissions (healthcare)
    "https://files.digital.nhs.uk/assets/AE/A%26E-Attendances-and-Emergency-Admisions-June-2021.csv"
]

TRUSTED_DOMAINS = [
    "githubusercontent.com",
    "cdc.gov",
    "openicpsr.org",
    "ics.uci.edu",
    "who.int",
    "digital.nhs.uk"
]

DATA_DIR = "data"

def is_trusted(url):
    return any(domain in url for domain in TRUSTED_DOMAINS)

def download_public_data(url):
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        # Smart parsing: .csv, .data, or openICPSR custom CSV
        if url.endswith(".csv") or "csv" in url:
            df = pd.read_csv(pd.compat.StringIO(response.text))
        else:
            # fallback: try whitespace or custom parsing
            df = pd.read_csv(pd.compat.StringIO(response.text), delimiter=None, engine="python")
        st.success(f"Fetched data from: {url}")
        return df
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")
        return None

def sanitize_data(df):
    if df is None or df.empty:
        st.warning("No data to sanitize.")
        return None
    df = df.dropna(axis=1, thresh=int(0.75 * len(df)))
    return df

def save_clean_data(df, source_url):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    filename = f"clean_data_{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}.csv"
    full_path = os.path.join(DATA_DIR, filename)
    df.to_csv(full_path, index=False)
    with open(os.path.join(DATA_DIR, "data_ingestion_log.txt"), "a") as logf:
        logf.write(f"{filename}\t{source_url}\t{pd.Timestamp.now()}\n")
    return full_path

def data_ingestion_ui():
    st.header("Enterprise Data Ingestion")
    source = st.selectbox("Choose trusted public data source", REPUTABLE_SOURCES)
    custom_url = st.text_input("Or enter another CSV URL (must be trusted domain)")
    url = custom_url.strip() if custom_url else source

    if url and not is_trusted(url):
        st.error("URL is not on the trusted whitelist. Only approved domains allowed.")
        return

    if st.button("Download & Preview Data"):
        data = download_public_data(url)
        clean_data = sanitize_data(data)
        if clean_data is not None:
            st.write("Preview of sanitized data:")
            st.dataframe(clean_data.head(20))
            save_path = save_clean_data(clean_data, url)
            st.success(f"Cleaned data saved as {os.path.basename(save_path)}")
            st.download_button(
                "Download Cleaned Data (CSV)",
                clean_data.to_csv(index=False).encode("utf-8"),
                os.path.basename(save_path)
            )

    if os.path.exists(DATA_DIR):
        clean_files = [f for f in os.listdir(DATA_DIR) if f.endswith(".csv")]
        if clean_files:
            st.subheader("Available Clean Data Files")
            for f in clean_files:
                st.write(f"- {f}")
