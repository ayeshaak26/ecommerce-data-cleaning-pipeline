# File uploader widget
uploaded_file = st.file_uploader(
    "Choose a raw CSV file downloaded from the Kaggle dataset source",
    type=["csv"],
)

if uploaded_file is not None:
    # Load the data only when the file is present
    df_raw = pd.read_csv(uploaded_file)
    df_clean = df_raw.copy()

    # (The rest of your Before vs. After metric columns and code blocks run here...)
else:
    # Safe fallback message for visitors who haven't uploaded the data yet
    st.info(
        "💡 Please upload the raw 'dirty_ecommerce_data.csv' file from the Kaggle dataset referenced in the README to execute the cleaning pipeline metrics dynamically."
    )
