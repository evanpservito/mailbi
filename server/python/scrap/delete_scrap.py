import psycopg2

def get_connection():
    return psycopg2.connect(
        host="127.0.0.1",
        port=5432,
        dbname="mailbidev",
        user="root",
        password="root"
    )

def delete_packages(event):
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
            
            package_ids = body["package_ids"]
            
            query = "DELETE FROM packages WHERE tracking_num = ANY(%s)"
            cur.execute(query, (package_ids,))
            
            return {"deleted_count": cur.rowcount}

def delete_mailboxes(event):
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
            
            mailbox_ids = body["mailbox_ids"]
            
            query = "DELETE FROM mailboxes WHERE id = ANY(%s)"
            cur.execute(query, (mailbox_ids,))
            
            return {"deleted_count": cur.rowcount}

def delete_customers(event):
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
            
            customer_ids = body["customer_ids"]
            
            query = "DELETE FROM customers WHERE id = ANY(%s)"
            cur.execute(query, (customer_ids,))
            
            return {"deleted_count": cur.rowcount}

def delete_accounts(event):
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
            
            account_ids = body["account_ids"]
            
            query = "DELETE FROM accounts WHERE id = ANY(%s) AND role = 'user'"
            cur.execute(query, (account_ids,))
            
            return {"deleted_count": cur.rowcount}

def delete_messages(event):
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
            
            message_ids = body["message_ids"]
            
            query = "DELETE FROM messages WHERE id = ANY(%s)"
            cur.execute(query, (message_ids,))
            
            return {"deleted_count": cur.rowcount}

