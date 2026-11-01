import pandas as pd
import streamlit as st  # <-- YEH LINE CHHUTI HUI THI JISSE NAMEERRORDiscovered

st.set_page_config(
    page_title="E-Commerce Data Cleaner", page_icon="🛒", layout="wide"
)

st.title("🛒 Relational E-Commerce Data Cleansing Pipeline")
st.write(
    "Dynamically execute the ETL pipeline, handle structural missingness, and enforce business constraints."
)

# File uploader widget
uploaded_file = st.file_uploader(
    "Choose a raw CSV file downloaded from the Kaggle dataset source",
    type=["csv"],
)

if uploaded_file is not None:
    # Load the data only when the file is present
    df_raw = pd.read_csv(uploaded_file)
    df_clean = df_raw.copy()

    # Layout: Two columns to compare Before vs After metrics
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("❌ Raw Data Profile")
        st.metric(label="Total Rows Ingested", value=df_raw.shape[0])

        # Missing values profile
        raw_missing = df_raw.isnull().sum()
        if raw_missing.sum() > 0:
            st.write("**Missing Value Footprints:**")
            st.dataframe(raw_missing[raw_missing > 0])
        else:
            st.success("No missing values found!")

        # Pricing check
        if "price" in df_raw.columns:
            raw_invalid_prices = df_raw[df_raw["price"] <= 0].shape[0]
            st.metric(label="Anomalous Prices (<= $0)", value=raw_invalid_prices)

        st.write("**Raw Data Sample Preview:**")
        st.dataframe(df_raw.head(5))

    # --- EXECUTE CLEANING PIPELINES ---
    # Pipeline 1: Date standardization
    if "order_date" in df_clean.columns:
        df_clean["order_date"] = pd.to_datetime(
            df_clean["order_date"].astype(str).str.strip(), errors="coerce"
        )

    # Pipeline 2: Drop duplicates
    initial_rows = df_clean.shape[0]
    df_clean.drop_duplicates(inplace=True)
    duplicate_rows_removed = initial_rows - df_clean.shape[0]

    # Pipeline 3: Conditional missing value logic for ship_date
    if "ship_date" in df_clean.columns:
        df_clean["ship_date"] = df_clean["ship_date"].fillna("Not Shipped")

    # Pipeline 4: Categorical mode imputation for country
    if "country" in df_clean.columns:
        country_mode = df_clean["country"].mode()[0]
        df_clean["country"] = df_clean["country"].fillna(country_mode)

    # Pipeline 5: Enforce financial constraints
    if "price" in df_clean.columns:
        df_clean = df_clean[df_clean["price"] > 0]

    with col2:
        st.subheader("✨ Cleaned Production Data")
        st.metric(
            label="Total Cleaned Rows",
            value=df_clean.shape[0],
            delta=f"-{df_raw.shape[0] - df_clean.shape[0]} rows managed",
        )

        st.write("**Cleaned Missing Value Audit:**")
        clean_missing = df_clean.isnull().sum()
        st.dataframe(clean_missing)

        st.metric(label="Exact Duplicates Purged", value=duplicate_rows_removed)

        st.write("**Cleaned Production Preview:**")
        st.dataframe(df_clean.head(5))

    # Download button for the fully processed file
    st.markdown("---")
    st.subheader("📥 Export Final Cleaned Dataset")
    csv_buffer = df_clean.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download ecommerce_final_clean.csv",
        data=csv_buffer,
        file_name="ecommerce_final_clean.csv",
        mime="text/csv",
    )

else:
    # Safe fallback message for visitors who haven't uploaded the data yet
    st.info(
        "💡 Please upload the raw 'dirty_ecommerce_data.csv' file from the Kaggle dataset referenced in the README to execute the cleaning pipeline metrics dynamically."
    )
