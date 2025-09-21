from update_scrap import *

sample_stores_update = {
    "body": {
        "store_id": 2,
        "account_id": 5,
        "current_role": "admin",
        "name": "Updated Store Name",
        "address": "Updated Address",
        "phone": "987654321"
    }
}

print(update_stores(sample_stores_update))

sample_mailboxes_update = {
    "body": {
        "store_id": 2,
        "account_id": 5,
        "current_role": "admin",
        "mailbox_id": 1,
        "mailbox_name": "300",
        "sms_bool": False
    }
}

print(update_mailboxes(sample_mailboxes_update))

sample_customers_update = {
    "body": {
        "store_id": 2,
        "account_id": 5,
        "current_role": "admin",
        "customer_id": 1,
        "mailbox_id": 2,
        "first_name": "Updated First",
        "last_name": "Updated Last",
        "phone": "9999999999",
        "email": "updated@email.com"
    }
}

print(update_customers(sample_customers_update))

sample_packages_update = {
    "body": {
        "store_id": 2,
        "account_id": 5,
        "current_role": "admin",
        "tracking_num": "ABC123",
        "record_date": "2024-01-10",
        "mailbox_id": 1,
        "customer_id": 1,
        "carrier": "FEDEX",
        "pckg_type": "B",
        "is_collected": True,
        "pickup_date": "2024-01-15"
    }
}

print(update_packages(sample_packages_update))

sample_accounts_update = {
    "body": {
        "store_id": 2,
        "account_id": 5,
        "current_role": "admin",
        "account_id": 6,
        "email": "updated_account@email.com"
    }
}

print(update_accounts(sample_accounts_update))
