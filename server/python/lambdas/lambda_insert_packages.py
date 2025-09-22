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

def send_sms_and_track(conn, cur, store_id, customer_id, customer_first_name, customer_middle_name, customer_last_name, tracking_num, mailbox_name, carrier):
    try:
        cur.execute(
            "SELECT phone FROM customers WHERE id = %s",
            (customer_id,)
        )
        phone_result = cur.fetchone()
        if not phone_result:
            return False
        
        phone_number = phone_result[0]
        
        if not phone_number:
            return False
            
        if not phone_number.startswith('+'):
            phone_number = f"+1{phone_number}"
        
        carrier_text = f" (via {carrier})" if carrier else ""
        message_text = f"Hello {customer_first_name}, your package {tracking_num}{carrier_text} has arrived!"
        
        sns_client = boto3.client('sns')
        
        # long_code_phone_number = "+1234567890"  # TODO: replace!
        
        response = sns_client.publish(
            PhoneNumber=phone_number,
            Message=message_text,
            MessageAttributes={
                'AWS.SNS.SMS.SMSType': {
                    'DataType': 'String',
                    'StringValue': 'Transactional'
                },
                # 'AWS.SNS.SMS.SenderID': { # TODO: uncomment!
                #     'DataType': 'String',
                #     'StringValue': long_code_phone_number
                # }
            }
        )
        
        cur.execute(
            "SELECT set_config('app.current_role', 'admin', true)"
        )
        cur.execute(
            "SELECT set_config('app.current_account_id', NULL, true)"
        )
        cur.execute(
            "SELECT set_config('app.current_store_id', %s, true)",
            (str(store_id),)
        )
        
        message_query = """
            INSERT INTO messages (store_id, customer_id, customer_first_name, customer_middle_name, customer_last_name, tracking_num, message_text)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        cur.execute(
            message_query,
            (
                store_id,
                customer_id,
                customer_first_name,
                customer_middle_name,
                customer_last_name,
                tracking_num,
                message_text
            )
        )
        
        sms_update_query = """
            UPDATE packages 
            SET sms_date = CURRENT_DATE 
            WHERE tracking_num = %s
        """
        cur.execute(sms_update_query, (tracking_num,))
        
        return True
        
    except Exception as e:
        print(f"SMS sending failed: {str(e)}")
        return False

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
                    INSERT INTO packages
                    (tracking_num, store_id, mailbox_id, customer_id, carrier, pckg_type)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """

                inserted_count = 0
                sms_sent_count = 0
                for param in body["params"]:
                    if param.get("customer_middle_name"):
                        cur.execute(
                            "SELECT id FROM customers WHERE first_name = %s AND middle_name = %s AND last_name = %s",
                            (param["customer_first_name"], param["customer_middle_name"], param["customer_last_name"])
                        )
                    else:
                        cur.execute(
                            "SELECT id FROM customers WHERE first_name = %s AND last_name = %s",
                            (param["customer_first_name"], param["customer_last_name"])
                        )

                    customer_result = cur.fetchone()
                    if not customer_result:
                        continue
                    
                    customer_id = customer_result[0]

                    cur.execute(
                        "SELECT m.id FROM mailboxes m JOIN customers c ON m.id = c.mailbox_id WHERE m.mailbox_name = %s AND c.id = %s",
                        (param["mailbox_name"], customer_id)
                    )

                    mailbox_result = cur.fetchone()
                    if not mailbox_result:
                        continue
                    
                    mailbox_id = mailbox_result[0]

                    cur.execute(
                        query,
                        (
                            param["tracking_num"],
                            body["store_id"],
                            mailbox_id,
                            customer_id,
                            param.get("carrier"),
                            param.get("pckg_type")
                        )
                    )
                    inserted_count += 1

                    sms_success = send_sms_and_track(
                        conn, cur, 
                        body["store_id"], 
                        customer_id,
                        param["customer_first_name"],
                        param.get("customer_middle_name"),
                        param["customer_last_name"],
                        param["tracking_num"],
                        param["mailbox_name"],
                        param.get("carrier")
                    )
                    
                    if sms_success:
                        sms_sent_count += 1

            conn.commit()
            
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'success': True,
                'inserted_count': inserted_count,
                'sms_sent_count': sms_sent_count
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
