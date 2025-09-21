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
                
                if "first_name" in body:
                    where_conditions.append("first_name ILIKE %s")
                    params.append(f"%{body['first_name']}%")
                
                if "middle_name" in body:
                    where_conditions.append("middle_name ILIKE %s")
                    params.append(f"%{body['middle_name']}%")
                
                if "last_name" in body:
                    where_conditions.append("last_name ILIKE %s")
                    params.append(f"%{body['last_name']}%")
                
                where_clause = ""
                if where_conditions:
                    where_clause = "WHERE " + " AND ".join(where_conditions)
                
                query = f"""
                    SELECT 
                        id,
                        store_id,
                        mailbox_id,
                        first_name,
                        middle_name,
                        last_name,
                        phone,
                        email
                    FROM customers
                    {where_clause}
                    ORDER BY last_name, first_name;
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
