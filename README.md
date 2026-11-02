# 🛒 Relational E-Commerce Data Cleansing & ETL Pipeline

An end-to-end Python data engineering pipeline designed to ingest chaotic, dirty transaction data, diagnose structural anomalies, and implement clean conditional data transformations. This project demonstrates advanced data wrangling techniques, handling structural missingness, and categorical data validation.

## 🚀 Key Achievements & Cleaning Metrics
* **Total Records Processed:** 80,000 product transaction entries.
* **Structural NaN Resolution:** Identified 14,453 missing entries in `ship_date` and cross-validated that they corresponded precisely with `pending` or `cancelled` order statuses. Transformed these from empty null values to explicit `'Not Shipped'` labels to maintain database integrity.
* **Categorical Data Imputation:** Handled 400 missing values in the `country` column using statistical mode imputation (`'United States'`) to preserve statistical boundaries without introducing model bias.
* **Data Formatting:** Automatically sanitized trailing/leading whitespaces and coerced non-standard date entries into strict ISO 8601 timestamps (`YYYY-MM-DD`).

---

## 🛠️ Data Cleansing Engineering Workflow

The pipeline runs sequentially through the following automated engineering blocks:

1. **Extraction & Structural Audit:** Automated data profiling via `df.info()` to track column data types and isolate initial missing values.
2. **Temporal Normalization:** Coercion of dynamic string records into concrete `datetime64` data objects using `pd.to_datetime()` with `errors='coerce'` tracking.
3. **Relational Deduplication:** Grouped evaluation across columns to search for, report, and purge full-row duplicates across transaction barriers.
4. **Conditional Inferences & Domain Imputation:** Applied custom row slicing filters to handle domain-specific `NaN` fields (such as logical null values in delivery dates for cancelled carts).
5. **Financial Border Constraint Enforcement:** Built a processing check to identify and isolate data entry errors, such as zero or negative pricing artifacts (`price <= 0`).

---

## 💻 Tech Stack & Tooling
* **Language:** Python 3.13
* **Libraries:** Data Wrangling (Pandas), Mathematical Processing (NumPy)
* **Environment:** Interactive Execution Walkthrough (Jupyter Notebook)

---

## 📁 Repository Map
* `/notebooks`: Contains the clean `ecom_cleaning_analytics.ipynb` master notebook pipeline walkthrough.
* `/data`: Input raw files and output fully processed datasets (`ecommerce_final_clean.csv`).
* `requirements.txt`: Simple documentation file for reproducibility.
