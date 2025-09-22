import boto3
import psycopg2
import json

def get_secret(secret_name, region_name="us-west-1"):
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

def lambda_handler(event, context):
    try:
        if event['httpMethod'] != 'POST':
            return {
                'statusCode': 405,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Method not allowed'})
            }
        
        body = event['body']
        
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT set_config('app.current_role', %s, true)",
                    (str(body["current_role"]),)
                )
                cur.execute(
                    "SELECT set_config('app.current_account_id', %s, true)",
                    (str(body["account_id"]),)
                )
                cur.execute(
                    "SELECT set_config('app.current_store_id', %s, true)",
                    (str(body["store_id"]),)
                )

                query = """
                    INSERT INTO messages (store_id, customer_id, customer_first_name, customer_middle_name, customer_last_name, tracking_num, message_text)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """

                sms_update_query = """
                    UPDATE packages 
                    SET sms_date = CURRENT_DATE 
                    WHERE tracking_num = %s
                """

                inserted_count = 0
                for param in body["params"]:
                    cur.execute(
                        query,
                        (
                            body["store_id"],
                            param["customer_id"],
                            param["customer_first_name"],
                            param.get("customer_middle_name"),
                            param["customer_last_name"],
                            param["tracking_num"],
                            param["message_text"]
                        )
                    )
                    
                    cur.execute(sms_update_query, (param["tracking_num"],))
                    inserted_count += 1

            conn.commit()
            
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'success': True,
                'inserted_count': inserted_count
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'success': False,
                'error': str(e)
            })
        }
