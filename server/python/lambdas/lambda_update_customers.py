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
                
                customer_id = body["customer_id"]
                updates = []
                params = []
                
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
                
                if "first_name" in body:
                    updates.append("first_name = %s")
                    params.append(body["first_name"])
                
                if "middle_name" in body:
                    updates.append("middle_name = %s")
                    params.append(body["middle_name"])
                
                if "last_name" in body:
                    updates.append("last_name = %s")
                    params.append(body["last_name"])
                
                if "phone" in body:
                    updates.append("phone = %s")
                    params.append(body["phone"])
                
                if "email" in body:
                    updates.append("email = %s")
                    params.append(body["email"])
                
                if not updates:
                    return {
                        'statusCode': 400,
                        'headers': {'Content-Type': 'application/json'},
                        'body': json.dumps({
                            'success': False,
                            'error': 'No fields to update'
                        })
                    }
                
                params.append(customer_id)
                query = f"UPDATE customers SET {', '.join(updates)} WHERE id = %s"
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
