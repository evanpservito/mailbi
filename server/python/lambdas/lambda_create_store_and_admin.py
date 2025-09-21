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
