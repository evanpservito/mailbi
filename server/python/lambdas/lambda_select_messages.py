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
        if event['httpMethod'] != 'GET':
            return {
                'statusCode': 405,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Method not allowed'})
            }
        
        body = json.loads(event['body'])
        
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
                
                where_conditions = []
                params = []
                
                if "customer_first_name" in body:
                    where_conditions.append("customer_first_name ILIKE %s")
                    params.append(f"%{body['customer_first_name']}%")
                
                if "customer_middle_name" in body:
                    where_conditions.append("customer_middle_name ILIKE %s")
                    params.append(f"%{body['customer_middle_name']}%")
                
                if "customer_last_name" in body:
                    where_conditions.append("customer_last_name ILIKE %s")
                    params.append(f"%{body['customer_last_name']}%")
                
                if "tracking_num" in body:
                    where_conditions.append("tracking_num ILIKE %s")
                    params.append(f"%{body['tracking_num']}%")
                
                where_clause = ""
                if where_conditions:
                    where_clause = "WHERE " + " AND ".join(where_conditions)
                
                query = f"""
                    SELECT 
                        id,
                        store_id,
                        customer_id,
                        customer_first_name,
                        customer_middle_name,
                        customer_last_name,
                        tracking_num,
                        message_text,
                        created_at
                    FROM messages
                    {where_clause}
                    ORDER BY created_at DESC;
                """
                
                cur.execute(query, params)
                columns = [desc[0] for desc in cur.description]
                results = cur.fetchall()
                
                data = [dict(zip(columns, row)) for row in results]
            
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'success': True,
                'data': data,
                'count': len(data)
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
