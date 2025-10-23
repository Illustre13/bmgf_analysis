
# Project Setup and AWS Configuration Guide

This guide walks through setting up your environment for the Gates Foundation dataset analysis project, including Python dependencies, local setup, and AWS configuration as per the video tutorial.

## 1. Python Environment Setup

1. Install Python 3.12+ (or latest stable version).
2. Create a virtual environment (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
3. Install required Python packages:

   ```bash
   pip install pandas numpy matplotlib seaborn plotly geopandas shapely pyproj openpyxl
   ```
4. Confirm installation:

   ```bash
   python -c "import pandas, numpy, matplotlib, seaborn, plotly, geopandas"
   ```

## 2. Data Access

* Place your dataset in the project directory.
* Ensure file extension is `.csv` or `.xlsx`.
* Example code snippet to load data:

```python
import pandas as pd

file_path = 'BMGF Grants.csv'  # or .xlsx

if file_path.endswith('.csv'):
    df = pd.read_csv(file_path)
else:
    df = pd.read_excel(file_path)

print(df.head())
```

## 3. Data Cleaning & EDA Workflow

1. Remove duplicates and handle missing values:

   ```python
   df.drop_duplicates(inplace=True)
   df.fillna('', inplace=True)
   ```
2. Feature Engineering:

   ```python
   df['year_committed'] = pd.to_datetime(df['date_committed']).dt.year
   ```
3. Separate categorical and numerical columns:

   ```python
   categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
   numerical_cols = df.select_dtypes(include=['int64','float64']).columns.tolist()
   ```
4. Visualizations:

   * Bar plots for categorical features (grantee, topic, country)
   * Histograms and boxplots for numerical features (amount_committed, duration_months)
   * Interactive maps using Plotly (Africa & Rwanda)

## 4. AWS CLI and S3 Setup

### Step 1: Create IAM User

1. Go to AWS Console → IAM → Users → Add user.
2. Assign **programmatic access**.
3. Attach **AdministratorAccess** or specific S3 permissions.
4. Save **Access Key ID** and **Secret Access Key**.

### Step 2: Install AWS CLI

```bash
# Check installation
aws --version

# If not installed, follow AWS CLI installation guide
```

### Step 3: Configure AWS CLI

```bash
aws configure
```

Enter:

```
AWS Access Key ID: <Your Access Key>
AWS Secret Access Key: <Your Secret Key>
Default region name: us-east-1
Default output format: json
```

### Step 4: Verify AWS CLI

```bash
aws sts get-caller-identity
aws s3 ls
```

### Step 5: S3 Bucket Setup

1. Create bucket via console or CLI:

```bash
aws s3 mb s3://bmgf-analysis
```

2. Upload dataset:

```bash
aws s3 cp BMGF\ Grants.csv s3://bmgf-analysis
```

3. List contents:

```bash
aws s3 ls s3://bmgf-analysis
```

### Notes

* Always use active credentials. Invalid keys will raise `InvalidAccessKeyId` errors.
* Use IAM roles if deploying on AWS EC2 or Lambda.
* Avoid hardcoding secrets in notebooks; use profiles or environment variables.

## 5: S3 Bucket Setup

Create bucket via console or CLI:

aws s3 mb s3://gates-foundation-project-data

Upload dataset:

aws s3 cp gates_projects.csv s3://gates-foundation-project-data/

List contents:

aws s3 ls s3://gates-foundation-project-data/
## 6: AWS Glue Catalog Setup

Go to AWS Console → Glue → Crawlers → Add Crawler.

Set data source to your S3 bucket (s3://gates-foundation-project-data).

Create or select a database in Glue for cataloging.

Configure crawler to run on demand or scheduled.

Run the crawler to create table schema in Glue Data Catalog.

## 7: AWS Athena Querying

    1. Go to AWS Console → Athena.
    2. Select the database created by Glue.
    3. Query your dataset using SQL:

    ```sql
    SELECT grantee_country, SUM(amount_committed) AS total_funding
    FROM gates_projects_table
    GROUP BY grantee_country
    ORDER BY total_funding DESC
    LIMIT 10;   
    ```

    4. Save query results to S3 if needed.

Notes

Always use active credentials. Invalid keys will raise InvalidAccessKeyId errors.

Use IAM roles if deploying on AWS EC2 or Lambda.

Avoid hardcoding secrets in notebooks; use profiles or environment variables.

Glue and Athena allow you to implement a serverless ETL pipeline.

This completes the full setup to go from data access → cleaning → EDA → AWS S3 storage → Glue catalog → Athena queries for your Gates Foundation analysis project.


## EXPLAIN (FORMAT JSON, TYPE DISTRIBUTED) SELECT * FROM "bmgf_glue_db"."bmgf_cleaned_processed_csv" limit 10

---

