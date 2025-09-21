from select_scrap import *

sample_packages_select = {
    "body": {
        "store_id": 2,
        "account_id": 5,
        "current_role": "user",
        "start_date": "2025-09-01",
        "end_date": "2025-09-31",
        "tracking_num": "123ABC",
        "mailbox_name": "200",
        "customer_first_name": "Evan",
        "is_collected": False
    }
}

print(select_packages(sample_packages_select))

sample_mailboxes_select = {
    "body": {
        "store_id": 2,
        "account_id": 5,
        "current_role": "admin"
    }
}

print(select_mailboxes(sample_mailboxes_select))

sample_customers_select = {
    "body": {
        "store_id": 2,
        "account_id": 5,
        "current_role": "admin",
        "first_name": "Evan",
        "last_name": "Goat"
    }
}

print(select_customers(sample_customers_select))

sample_stores_select = {
    "body": {
        "store_id": 2,
        "account_id": 5,
        "current_role": "admin"
    }
}

print(select_stores(sample_stores_select))

sample_accounts_select = {
    "body": {
        "store_id": 2,
        "account_id": 5,
        "current_role": "admin"
    }
}

print(select_accounts(sample_accounts_select))

sample_messages_select = {
    "body": {
        "store_id": 2,
        "account_id": 5,
        "current_role": "admin",
        "customer_first_name": "Zion",
        "tracking_num": "ABC123"
    }
}

print(select_messages(sample_messages_select))