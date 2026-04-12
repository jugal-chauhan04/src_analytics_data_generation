# PROJECT CONFIGURATION FILE

from datetime import datetime

# TIMEFRAME FOR DATA GENERATION
START_DATE = datetime(2024, 1, 1).date()
END_DATE = datetime.today().date()

# DATASET SIZES
N_CUSTOMERS = 10
N_PLANS = 9 

# RANDOM SEED
SEED = 44

# EMAIL DOMAIN
DOMAIN = "srcanalytics.com"  

# UPGRADE PROBABILITY
UPGRADE_PROBABILITY = 0.40 

# SUBSCRIPTION DISCOUNT START ID
SUB_DISCOUNT_ID = 401

# CYCLE DAYS
MONTHLY_CYCLE_DAYS = 30
YEARLY_CYCLE_DAYS = 365

# STATIC TABLE  
STATIC_TABLES = {"plans", "products", "discounts"} 

# DYNAMIC TABLES 
DYNAMIC_TABLES = {"customers", "subscriptions", "invoices", "payments", "line_items", "subscription_discounts"}
# DATAFLOWIQ PRODUCTS CATALOG 
PRODUCTS = [
    {"product_id": 1, "product_name": "AutomateSRC", "product_description": "Workflow automation tool"},
    {"product_id": 2, "product_name": "CollabSRC", "product_description": "Team collaboration platform"},
    {"product_id": 3, "product_name": "InsightSRC", "product_description": "Business analytics platform"},
]

# PLANS
PLANS = [
    {"plan_id": 101, "product_id": 1, "plan_name": "Free",    "plan_price": 0,    "recurring": "monthly"},
    {"plan_id": 102, "product_id": 1, "plan_name": "Pro",     "plan_price": 100,  "recurring": "monthly"},
    {"plan_id": 103, "product_id": 1, "plan_name": "Premium", "plan_price": 1000, "recurring": "yearly"},
    {"plan_id": 201, "product_id": 2, "plan_name": "Free",    "plan_price": 0,    "recurring": "monthly"},
    {"plan_id": 202, "product_id": 2, "plan_name": "Pro",     "plan_price": 50,   "recurring": "monthly"},
    {"plan_id": 203, "product_id": 2, "plan_name": "Premium", "plan_price": 400,  "recurring": "yearly"},
    {"plan_id": 301, "product_id": 3, "plan_name": "Free",    "plan_price": 0,    "recurring": "monthly"},
    {"plan_id": 302, "product_id": 3, "plan_name": "Pro",     "plan_price": 200,  "recurring": "monthly"},
    {"plan_id": 303, "product_id": 3, "plan_name": "Premium", "plan_price": 2000, "recurring": "yearly"},
]

DISCOUNTS = [
    {
        "discount_id": 1,
        "discount_code": "WELCOME20",
        "discount_type": "percent",   # percent or fixed
        "discount_value": 20,         # 20% off
        "valid_from": datetime(2022, 1, 1),
        "valid_to": datetime(2024, 12, 31),
        "product_id": None,           # None = applies to all products
        "plan_id": None,              # None = applies to all plans
        "is_recurring": False,        # applies only once
    }
]

# UNIQUE KEYS
# config.py
UNIQUE_KEYS = {
    "customers": "customer_id",
    "subscriptions": "subscription_id",
    "invoices": "invoice_id",
    "line_items": "line_item_id",
    "payments": "payment_id",
    "products": "product_id",
    "plans": "plan_id",
    "discounts": "discount_id",
    "subscription_discounts": "sub_discount_id",
}
