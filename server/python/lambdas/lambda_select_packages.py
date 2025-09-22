import boto3
import psycopg2
import json
from datetime import date, datetime

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

def convert_dates_to_strings(obj):
    if isinstance(obj, date):
        return obj.isoformat()
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {key: convert_dates_to_strings(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_dates_to_strings(item) for item in obj]
    else:
        return obj

def lambda_handler(event, context):
    try:
        if event['httpMethod'] != 'GET':
            return {
                'statusCode': 405,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Method not allowed'})
            }
        
        body = event['queryStringParameters']
        
        try:
            jwt_cognito_sub = event["requestContext"]["authorizer"]["claims"]["sub"]
        except (KeyError, TypeError):
            return {
                'statusCode': 401,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'success': False,
                    'error': 'Missing or invalid JWT token'
                })
            }
        
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT cognito_sub FROM accounts WHERE id = %s",
                    (body["account_id"],)
                )
                account_result = cur.fetchone()
                if not account_result or account_result[0] != jwt_cognito_sub:
                    return {
                        'statusCode': 403,
                        'headers': {'Content-Type': 'application/json'},
                        'body': json.dumps({
                            'success': False,
                            'error': 'Forbidden: Account does not match authenticated user'
                        })
                    }
                
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
                
                if "start_date" in body and "end_date" in body:
                    where_conditions.append("""
                        CASE 
                            WHEN is_collected = true THEN pickup_date BETWEEN %s AND %s
                            ELSE record_date BETWEEN %s AND %s
                        END
                    """)
                    params.extend([body["start_date"], body["end_date"], body["start_date"], body["end_date"]])
                
                if "tracking_num" in body:
                    where_conditions.append("p.tracking_num ILIKE %s")
                    params.append(f"%{body['tracking_num']}%")
                
                if "mailbox_name" in body:
                    where_conditions.append("m.mailbox_name = %s")
                    params.append(body["mailbox_name"])
                
                if "customer_first_name" in body:
                    where_conditions.append("c.first_name ILIKE %s")
                    params.append(f"%{body['customer_first_name']}%")
                
                if "customer_middle_name" in body:
                    where_conditions.append("c.middle_name ILIKE %s")
                    params.append(f"%{body['customer_middle_name']}%")
                
                if "customer_last_name" in body:
                    where_conditions.append("c.last_name ILIKE %s")
                    params.append(f"%{body['customer_last_name']}%")
                
                if "pickup_date" in body:
                    where_conditions.append("p.pickup_date = %s")
                    params.append(body["pickup_date"])
                
                if "sms_date" in body:
                    where_conditions.append("p.sms_date = %s")
                    params.append(body["sms_date"])
                
                if "is_collected" in body:
                    where_conditions.append("p.is_collected = %s")
                    params.append(body["is_collected"])
                
                if "customer_phone" in body:
                    where_conditions.append("c.phone = %s")
                    params.append(body["customer_phone"])
                
                if "carrier" in body:
                    where_conditions.append("p.carrier ILIKE %s")
                    params.append(f"%{body['carrier']}%")
                
                if "pckg_type" in body:
                    where_conditions.append("p.pckg_type = %s")
                    params.append(body["pckg_type"])
                
                where_clause = ""
                if where_conditions:
                    where_clause = "WHERE " + " AND ".join(where_conditions)
                
                query = f"""
                    SELECT 
                        p.tracking_num,
                        p.record_date,
                        p.mailbox_id,
                        p.customer_id,
                        p.carrier,
                        p.pckg_type,
                        p.pickup_date,
                        p.sms_date,
                        p.is_collected,
                        m.mailbox_name,
                        c.first_name,
                        c.middle_name,
                        c.last_name,
                        c.phone,
                        c.email
                    FROM packages p
                    LEFT JOIN mailboxes m ON p.mailbox_id = m.id
                    LEFT JOIN customers c ON p.customer_id = c.id
                    {where_clause}
                    ORDER BY p.record_date DESC;
                """
                
                cur.execute(query, params)
                columns = [desc[0] for desc in cur.description]
                results = cur.fetchall()
                
                data = [dict(zip(columns, row)) for row in results]
                data = convert_dates_to_strings(data)
            
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
