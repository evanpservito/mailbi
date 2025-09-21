import json
import psycopg2

def get_connection():
    return psycopg2.connect(
        host="127.0.0.1",
        port=5432,
        dbname="mailbidev",
        user="root",
        password="root"
    )

def lambda_handler(event, context):
    try:
        if event['httpMethod'] != 'POST':
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

                query = """
                    INSERT INTO mailboxes (store_id, sms_bool, mailbox_name)
                    VALUES (%s, %s, %s)
                """

                values = [(body["store_id"], param["sms_bool"], param["mailbox_name"]) for param in body["params"]]

                cur.executemany(query, values)

            conn.commit()
            
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'success': True,
                'inserted_count': len(body["params"])
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
