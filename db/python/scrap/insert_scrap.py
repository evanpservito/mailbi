import psycopg2

def get_connection():
    return psycopg2.connect(
        host="127.0.0.1",
        port=5432,
        dbname="mailbidev",
        user="root",
        password="root"
    )

def insert_packages(event):
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
                INSERT INTO packages
                (tracking_num, store_id, mailbox_id, customer_id, carrier, pckg_type)
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            inserted_count = 0
            for param in body["params"]:
                if param.get("customer_middle_name", False):
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

        conn.commit()
        return {"inserted_count": inserted_count}

def insert_customers(event):
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
                INSERT INTO customers (store_id, mailbox_id, first_name, middle_name, last_name, phone, email)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            values = [(body["store_id"], param["mailbox_id"], param["first_name"], param.get("middle_name"), param["last_name"], param["phone"], param.get("email")) for param in body["params"]]

            cur.executemany(query, values)

        conn.commit()
        return {"inserted_count": len(body["params"])}

def create_store_and_admin(event):
    with get_connection() as conn:
        with conn.cursor() as cur:
            body = event["body"]
            
            cur.execute(
                """
                INSERT INTO stores (name, address, phone, admin_id)
                VALUES (%s, %s, %s, NULL)
                RETURNING id
                """,
                (body["name"], body["address"], body["phone"])
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
        return {"store_id": store_id, "admin_id": admin_id}

def insert_mailboxes(event):
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
                INSERT INTO mailboxes (store_id, sms_bool, mailbox_name)
                VALUES (%s, %s, %s)
            """

            values = [(body["store_id"], param["sms_bool"], param["mailbox_name"]) for param in body["params"]]

            cur.executemany(query, values)

        conn.commit()
        return {"inserted_count": len(body["params"])}

def insert_user_accounts(event):
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
                INSERT INTO accounts
                (
                    cognito_sub, store_id, email
                )
                VALUES
                (
                    %s, %s, %s
                )
            """

            values = [(param["cognito_sub"], body["store_id"], param.get("email")) for param in body["params"]]

            cur.executemany(query, values)

        conn.commit()
        return {"inserted_count": len(body["params"])}

def insert_messages(event):
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
                INSERT INTO messages (store_id, customer_id, customer_first_name, customer_middle_name, customer_last_name, tracking_num, message_text)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            sms_update_query = """
                UPDATE packages 
                SET sms_date = CURRENT_DATE 
                WHERE tracking_num = %s
            """

            inserted_count = 0
            for param in body["params"]:
                cur.execute(
                    query,
                    (
                        body["store_id"],
                        param["customer_id"],
                        param["customer_first_name"],
                        param.get("customer_middle_name"),
                        param["customer_last_name"],
                        param["tracking_num"],
                        param["message_text"]
                    )
                )
                
                cur.execute(sms_update_query, (param["tracking_num"],))
                inserted_count += 1

            # !! at this point the Lambda must send a SMS to the customer

        conn.commit()
        return {"inserted_count": inserted_count}