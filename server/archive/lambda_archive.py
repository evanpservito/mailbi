import pandas as pd
import boto3
import psycopg2
from io import BytesIO
from datetime import datetime, timedelta

def get_secret(secret_name, region_name="us-west-1"):
    import json
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)
    response = client.get_secret_value(SecretId=secret_name)
    secret = response.get('SecretString') 
    return json.loads(secret) if secret else {}

def get_connection(): 
    secret_name = "rds!db-af844c39-6473-4450-838d-1643edeb8332"
    creds = get_secret(secret_name)

    return psycopg2.connect(
        host="mailbi-dev.cdcqwic8gvhl.us-west-1.rds.amazonaws.com",
        port=5432,
        dbname="mailbidev",
        user="postgres",
        password=creds["password"]
    )

def archive_table_data(conn, table_name, cutoff, s3_client, bucket_name):
    if table_name == "packages":
        query = "SELECT * FROM packages WHERE is_collected = TRUE AND record_date < %s"
        delete_query = "DELETE FROM packages WHERE is_collected = TRUE AND record_date < %s"
    elif table_name == "messages":
        query = "SELECT * FROM messages WHERE created_at < %s"
        delete_query = "DELETE FROM messages WHERE created_at < %s"
    else:
        return 0, None
    
    df = pd.read_sql(query, conn, params=(cutoff,))
    
    if df.empty:
        return 0, None
    
    buffer = BytesIO()
    df.to_parquet(buffer, engine="pyarrow", index=False)
    buffer.seek(0)

    key = f"{table_name}/{datetime.utcnow():%Y/%m/%d}/{table_name}.parquet"
    s3_client.upload_fileobj(buffer, bucket_name, key)

    with conn.cursor() as cur:
        cur.execute(delete_query, (cutoff,))
        conn.commit()
    
    return len(df), key

def lambda_handler(event, context):
    try:
        cutoff = datetime.utcnow() - timedelta(days=14)
        
        conn = get_connection()
        s3 = boto3.client("s3")
        bucket_name = "mailbi-archive"
        
        packages_rows, packages_key = archive_table_data(conn, "packages", cutoff, s3, bucket_name)
        messages_rows, messages_key = archive_table_data(conn, "messages", cutoff, s3, bucket_name)
        
        total_rows = packages_rows + messages_rows
        
        conn.close()
        
        if total_rows == 0:
            print("No data to archive.")
            return "No data to archive."
        
        print(f"Archived and deleted {total_rows} total rows.")
        print(f"Packages: {packages_rows} rows -> {packages_key}")
        print(f"Messages: {messages_rows} rows -> {messages_key}")
        
        return f"Archived and deleted {total_rows} total rows."
        
    except Exception as e:
        print(f"Error during archiving: {str(e)}")
        raise e
