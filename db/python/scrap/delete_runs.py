from delete_scrap import *

sample_packages_delete = {
    "body": {
        "store_id": 2,
        "account_id": 5,
        "current_role": "admin",
        "package_ids": ["ABC123", "123ABC"]
    }
}

print(delete_packages(sample_packages_delete))

sample_mailboxes_delete = {
    "body": {
        "store_id": 2,
        "account_id": 5,
        "current_role": "admin",
        "mailbox_ids": [1, 2]
    }
}

print(delete_mailboxes(sample_mailboxes_delete))

sample_customers_delete = {
    "body": {
        "store_id": 2,
        "account_id": 5,
        "current_role": "admin",
        "customer_ids": [1, 2]
    }
}

print(delete_customers(sample_customers_delete))

sample_accounts_delete = {
    "body": {
        "store_id": 2,
        "account_id": 5,
        "current_role": "admin",
        "account_ids": [6, 7]
    }
}

print(delete_accounts(sample_accounts_delete))

sample_messages_delete = {
    "body": {
        "store_id": 2,
        "account_id": 5,
        "current_role": "admin",
        "message_ids": [1, 2]
    }
}

print(delete_messages(sample_messages_delete))
