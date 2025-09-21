from insert_scrap import *

### 
sample_packages = {"body": {
	"store_id" : 2,
	"account_id": 5,
	"current_role": "admin",
	"params": [
		{
			"customer_first_name": "Zion",
            "customer_middle_name": "IsWith",
            "customer_last_name": "Vo",
            "mailbox_name": "100",
            "tracking_num": "ABC123",
            "carrier": "UPS",
            "pckg_type": "A",
		},
		{
			"customer_first_name": "Evan",
            "customer_last_name": "Goat",
            "mailbox_name": "200",
            "tracking_num": "123ABC",
            "carrier": "UPS",
            "pckg_type": "A",
		},
	]
}}

insert_packages(sample_packages)

###
sample_customers = {"body": {
	"store_id" : 2,
	"account_id": 5,
	"current_role": "admin",
	"params": [
		{
            "mailbox_id": 1,
            "first_name": "Zion",
            "middle_name": "IsWith", 
            "last_name": "Vo", 
            "phone": "1234567890", 
            "email": "zioniswithdylan@gmail.com"
		},
		{
            "mailbox_id": 2,
            "first_name": "Evan",
            "middle_name": "IsThe", 
            "last_name": "Goat", 
            "phone": "2222222222", 
            "email": "goatevan@gmail.com"
		},
	]
}}

insert_customers(sample_customers)

###
sample_store = {"body": {
    "name": "choppedhouse",
    "address": "123dylanwithzion",
    "phone": "123456789",
    "email": "dylanwithzion@gmail.com",
    "cognito_sub": "dylaniswithzion123"
}}

create_store_and_admin(sample_store)

###
sample_mailboxes = {"body": {
    "store_id" : 2,
	"account_id": 5,
	"current_role": "admin",
	"params": [
		{
            "sms_bool": True,
            "mailbox_name": "100"
		},
		{
           "sms_bool": True,
           "mailbox_name": "200"
		},
	]
    }
}

insert_mailboxes(sample_mailboxes)

###
sample_accounts = {"body": {
    "store_id" : 2,
	"account_id": 5,
	"current_role": "admin",
	"params": [
		{
            "cognito_sub": "A1B2",
            "email": "account1@gmail.com",
		},
		{
            "cognito_sub": "C3D4",
            "email": "account2@gmail.com",
		}
	]
    }
}

insert_user_accounts(sample_accounts)

###
sample_messages = {"body": {
    "store_id": 2,
    "account_id": 5,
    "current_role": "admin",
    "params": [
        {
            "customer_id": 1,
            "customer_first_name": "Zion",
            "customer_middle_name": "IsWith",
            "customer_last_name": "Vo",
            "tracking_num": "ABC123",
            "message_text": "Your package has arrived! Please pick it up at mailbox 100."
        },
        {
            "customer_id": 2,
            "customer_first_name": "Evan",
            "customer_last_name": "Goat",
            "tracking_num": "123ABC",
            "message_text": "Package ready for pickup at mailbox 200."
        }
    ]
}}

insert_messages(sample_messages)