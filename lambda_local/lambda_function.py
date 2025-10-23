import awswrangler as wr
import pandas as pd
import urllib.parse
import os

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    print(f"Reading s3://{bucket}/{key}")

    # Read CSV
    df = wr.s3.read_csv(f"s3://{bucket}/{key}")
    
    # Clean column names (optional but good practice)
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    # Fill missing grantee names to avoid grouping issues
    df['grantee'] = df['grantee'].fillna('Unknown')

    # Ensure amount_committed is numeric (force invalids to NaN)
    df['amount_committed'] = pd.to_numeric(df['amount_committed'], errors='coerce')

    # Fill NaN with 0 for numeric columns
    df['amount_committed'] = df['amount_committed'].fillna(0)

    # Example aggregation
    top_grantees = (
        df.groupby('grantee')['amount_committed']
        .sum()
        .nlargest(5)
        .to_dict()
    )

    print("Top 5 Grantees by Funding (USD):")
    print(top_grantees)

    return {
        "statusCode": 200,
        "body": f"Processed {len(df)} rows. Top 5: {top_grantees}"
    }
