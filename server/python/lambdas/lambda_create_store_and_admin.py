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
                    """
                    INSERT INTO stores (name, address, phone, admin_id)
                    VALUES (%s, %s, %s, NULL)
                    RETURNING id
                    """,
                    (body["name"], body.get("address"), body.get("phone"))
                )
                store_id = cur.fetchone()[0]

                cur.execute(
                    """
                    INSERT INTO accounts (cognito_sub, store_id, email, role)
                    VALUES (%s, %s, %s, 'admin')
                    RETURNING id
                    """,
                    (body["cognito_sub"], store_id, body["email"])
                )
                admin_id = cur.fetchone()[0]

                cur.execute(
                    """
                    UPDATE stores
                    SET admin_id = %s
                    WHERE id = %s
                    """,
                    (admin_id, store_id)
                )

            conn.commit()
            
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'success': True,
                'store_id': store_id,
                'admin_id': admin_id
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
