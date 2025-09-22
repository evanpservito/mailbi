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
        if event['httpMethod'] not in ['PATCH', 'PUT']:
            return {
                'statusCode': 405,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Method not allowed'})
            }
        
        body = event['body']
        
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
                
                tracking_num = body["tracking_num"]
                updates = []
                params = []
                
                if "record_date" in body:
                    updates.append("record_date = %s")
                    params.append(body["record_date"])
                
                if "mailbox_name" in body:
                    cur.execute(
                        "SELECT id FROM mailboxes WHERE mailbox_name = %s AND store_id = %s",
                        (body["mailbox_name"], body["store_id"])
                    )
                    mailbox_result = cur.fetchone()
                    if not mailbox_result:
                        return {
                            'statusCode': 400,
                            'headers': {'Content-Type': 'application/json'},
                            'body': json.dumps({
                                'success': False,
                                'error': 'Mailbox not found in this store'
                            })
                        }
                    
                    updates.append("mailbox_id = %s")
                    params.append(mailbox_result[0])
                
                if "customer_first_name" in body and "customer_last_name" in body:
                    if body.get("customer_middle_name"):
                        cur.execute(
                            "SELECT id FROM customers WHERE first_name = %s AND middle_name = %s AND last_name = %s AND store_id = %s",
                            (body["customer_first_name"], body["customer_middle_name"], body["customer_last_name"], body["store_id"])
                        )
                    else:
                        cur.execute(
                            "SELECT id FROM customers WHERE first_name = %s AND last_name = %s AND store_id = %s",
                            (body["customer_first_name"], body["customer_last_name"], body["store_id"])
                        )
                    
                    customer_result = cur.fetchone()
                    if not customer_result:
                        return {
                            'statusCode': 400,
                            'headers': {'Content-Type': 'application/json'},
                            'body': json.dumps({
                                'success': False,
                                'error': 'Customer not found in this store'
                            })
                        }
                    
                    updates.append("customer_id = %s")
                    params.append(customer_result[0])
                
                if "carrier" in body:
                    updates.append("carrier = %s")
                    params.append(body["carrier"])
                
                if "pckg_type" in body:
                    updates.append("pckg_type = %s")
                    params.append(body["pckg_type"])
                
                if "pickup_date" in body:
                    updates.append("pickup_date = %s")
                    params.append(body["pickup_date"])
                
                if "sms_date" in body:
                    updates.append("sms_date = %s")
                    params.append(body["sms_date"])
                
                if "is_collected" in body:
                    updates.append("is_collected = %s")
                    params.append(body["is_collected"])
                
                if not updates:
                    return {
                        'statusCode': 400,
                        'headers': {'Content-Type': 'application/json'},
                        'body': json.dumps({
                            'success': False,
                            'error': 'No fields to update'
                        })
                    }
                
                params.append(tracking_num)
                query = f"UPDATE packages SET {', '.join(updates)} WHERE tracking_num = %s"
                cur.execute(query, params)
                
            conn.commit()
            
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'success': True,
                'updated_count': cur.rowcount
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
