import psycopg2

def get_connection():
    return psycopg2.connect(
        host="127.0.0.1",
        port=5432,
        dbname="mailbidev",
        user="root",
        password="root"
    )

def update_stores(event):
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
            
            store_id = body["store_id"]
            updates = []
            params = []
            
            if "name" in body:
                updates.append("name = %s")
                params.append(body["name"])
            
            if "address" in body:
                updates.append("address = %s")
                params.append(body["address"])
            
            if "phone" in body:
                updates.append("phone = %s")
                params.append(body["phone"])
            
            if not updates:
                return {"updated_count": 0}
            
            params.append(store_id)
            query = f"UPDATE stores SET {', '.join(updates)} WHERE id = %s"
            cur.execute(query, params)
            
            return {"updated_count": cur.rowcount}

def update_mailboxes(event):
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
            
            mailbox_id = body["mailbox_id"]
            updates = []
            params = []
            
            if "mailbox_name" in body:
                updates.append("mailbox_name = %s")
                params.append(body["mailbox_name"])
            
            if "sms_bool" in body:
                updates.append("sms_bool = %s")
                params.append(body["sms_bool"])
            
            if not updates:
                return {"updated_count": 0}
            
            params.append(mailbox_id)
            query = f"UPDATE mailboxes SET {', '.join(updates)} WHERE id = %s"
            cur.execute(query, params)
            
            return {"updated_count": cur.rowcount}

def update_customers(event):
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
            
            customer_id = body["customer_id"]
            updates = []
            params = []
            
            if "mailbox_id" in body:
                updates.append("mailbox_id = %s")
                params.append(body["mailbox_id"])
            
            if "first_name" in body:
                updates.append("first_name = %s")
                params.append(body["first_name"])
            
            if "middle_name" in body:
                updates.append("middle_name = %s")
                params.append(body.get("middle_name"))
            
            if "last_name" in body:
                updates.append("last_name = %s")
                params.append(body["last_name"])
            
            if "phone" in body:
                updates.append("phone = %s")
                params.append(body["phone"])
            
            if "email" in body:
                updates.append("email = %s")
                params.append(body.get("email"))
            
            if not updates:
                return {"updated_count": 0}
            
            params.append(customer_id)
            query = f"UPDATE customers SET {', '.join(updates)} WHERE id = %s"
            cur.execute(query, params)
            
            return {"updated_count": cur.rowcount}

def update_packages(event):
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
            
            tracking_num = body["tracking_num"]
            updates = []
            params = []
            
            if "record_date" in body:
                updates.append("record_date = %s")
                params.append(body["record_date"])
            
            if "mailbox_id" in body:
                updates.append("mailbox_id = %s")
                params.append(body["mailbox_id"])
            
            if "customer_id" in body:
                updates.append("customer_id = %s")
                params.append(body["customer_id"])
            
            if "carrier" in body:
                updates.append("carrier = %s")
                params.append(body.get("carrier"))
            
            if "pckg_type" in body:
                updates.append("pckg_type = %s")
                params.append(body.get("pckg_type"))
            
            if "pickup_date" in body:
                updates.append("pickup_date = %s")
                params.append(body.get("pickup_date"))
            
            if "sms_date" in body:
                updates.append("sms_date = %s")
                params.append(body.get("sms_date"))
            
            if "is_collected" in body:
                updates.append("is_collected = %s")
                params.append(body["is_collected"])
            
            if not updates:
                return {"updated_count": 0}
            
            params.append(tracking_num)
            query = f"UPDATE packages SET {', '.join(updates)} WHERE tracking_num = %s"
            cur.execute(query, params)
            
            return {"updated_count": cur.rowcount}

def update_accounts(event):
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
            
            account_id = body["account_id"]
            updates = []
            params = []
            
            if "email" in body:
                updates.append("email = %s")
                params.append(body.get("email"))
            
            if not updates:
                return {"updated_count": 0}
            
            params.append(account_id)
            query = f"UPDATE accounts SET {', '.join(updates)} WHERE id = %s"
            cur.execute(query, params)
            
            return {"updated_count": cur.rowcount}
