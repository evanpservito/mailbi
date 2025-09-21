import psycopg2

def get_connection():
    return psycopg2.connect(
        host="127.0.0.1",
        port=5432,
        dbname="mailbidev",
        user="root",
        password="root"
    )

def select_packages(event):
    with get_connection() as conn:
        with conn.cursor() as cur:
            body = event["body"]
            
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
            
            return [dict(zip(columns, row)) for row in results]

def select_mailboxes(event):
    with get_connection() as conn:
        with conn.cursor() as cur:
            body = event["body"]
            
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
                SELECT 
                    id,
                    store_id,
                    mailbox_name,
                    sms_bool
                FROM mailboxes
                ORDER BY mailbox_name;
            """
            
            cur.execute(query)
            columns = [desc[0] for desc in cur.description]
            results = cur.fetchall()
            
            return [dict(zip(columns, row)) for row in results]

def select_customers(event):
    with get_connection() as conn:
        with conn.cursor() as cur:
            body = event["body"]
            
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
            
            return [dict(zip(columns, row)) for row in results]

def select_stores(event):
    with get_connection() as conn:
        with conn.cursor() as cur:
            body = event["body"]
            
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
                SELECT 
                    id,
                    name,
                    address,
                    phone,
                    admin_id
                FROM stores
                ORDER BY name;
            """
            
            cur.execute(query)
            columns = [desc[0] for desc in cur.description]
            results = cur.fetchall()
            
            return [dict(zip(columns, row)) for row in results]

def select_accounts(event):
    with get_connection() as conn:
        with conn.cursor() as cur:
            body = event["body"]
            
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
                SELECT 
                    id,
                    cognito_sub,
                    store_id,
                    email,
                    role,
                    created_at
                FROM accounts
                ORDER BY created_at DESC;
            """
            
            cur.execute(query)
            columns = [desc[0] for desc in cur.description]
            results = cur.fetchall()
            
            return [dict(zip(columns, row)) for row in results]

def select_messages(event):
    with get_connection() as conn:
        with conn.cursor() as cur:
            body = event["body"]
            
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
            
            return [dict(zip(columns, row)) for row in results]

    