import numpy as np 
import pandas as pd 
import random
from datetime import timedelta
from faker import Faker 
from dateutil.relativedelta import relativedelta
from extract.config import START_DATE, END_DATE, N_CUSTOMERS, N_PLANS, SEED, DOMAIN, PRODUCTS, PLANS, UPGRADE_PROBABILITY, DISCOUNTS, SUB_DISCOUNT_ID, MONTHLY_CYCLE_DAYS, YEARLY_CYCLE_DAYS

fake = Faker()
 

def generate_customers(n: int = N_CUSTOMERS, start_id: int = 1, domain: str = DOMAIN) -> pd.DataFrame:
    """
    Generate a synthetic dataset of customer name, email, address, and payment method

    Args:
        n(int): Number of customers to generate.
        domain(str): domain name for email address.
    
    Returns:
        pd.DataFrame: DataFrame with customer information.
    """

    names = [fake.name() for _ in range(n)]
    emails = [f"customer_{i}@{domain}" for i in range(start_id, start_id + n)]
    addresses = [fake.address().replace("\n", ",") for _ in range(n)]
    payment_methods = np.random.choice(
        ["Credit", "Debit", "Paypal"], size = n, p = [0.5, 0.3, 0.2]
        )
    customers = pd.DataFrame({
        "customer_id": range(start_id, start_id + n),
        "customer_name": names,
        "customer_email": emails,
        "customer_address": addresses,
        "payment_method": payment_methods
    }
    )

    return customers

def generate_products(products: list = None) -> pd.DataFrame:
    """
    Generate a synthetic dataset of products.

    Args:
        products (list, optional): List of product dictionaries with keys 
                                   'product_id', 'product_name', 'product_description'.
                                   If None, defaults to PRODUCTS from config.py.

    Returns:
        pd.DataFrame: DataFrame with product information.
    """
    if products is None:
        products = PRODUCTS

    return pd.DataFrame(products)

def generate_plans() -> pd.DataFrame:


    """
    Return the static list of subscription plans as a DataFrame.

    Plans are defined in config.py to keep business logic separate
    from generation logic.
    
    Returns:
        pd.DataFrame: DataFrame with plan information.
    """
    return pd.DataFrame(PLANS)

def generate_subscription_row(sub_id, customer_id, plan, start_date, status=None):
    """
    Generate a single subscription record.
    """
    if status is None:
        status = random.choice(["active", "cancelled"])
    
    end_date = None if status == "active" else start_date + timedelta(days=random.randint(60, 720))
    if end_date and end_date > END_DATE:
        end_date = END_DATE
    
    cancel_date = end_date if status == "cancelled" else None
    
    return [
        sub_id,
        customer_id,
        plan.plan_id,
        start_date,
        end_date,
        status,
        cancel_date,
    ]

def choose_new_plan(current_plan, plans):
    """
    Given a current plan, decide whether to cancel, downgrade, or upgrade.
    - Includes Pro -> Free downgrade scenario.
    - Chooses new plan only within the same product_id.
    - Returns (new_plan, status).
    """

    action = random.choices(
        ["upgrade", "downgrade", "churn"],
        weights=[0.4, 0.4, 0.2],  # tweak probabilities as needed
        k=1
    )[0]

    product_id = current_plan.product_id
    current_price = current_plan.plan_price

    if action == "churn":
        return None, "cancelled"

    if action == "upgrade":
        # Upgrade to any higher-priced plan (e.g., Free -> Pro or Pro -> Premium)
        higher_plans = plans[
            (plans["product_id"] == product_id) &
            (plans["plan_price"] > current_price)
        ]
        if not higher_plans.empty:
            return higher_plans.sample(1).iloc[0], "upgraded"

    if action == "downgrade":
        # Downgrade to any lower-priced plan (e.g., Premium -> Pro or Pro -> Free)
        lower_plans = plans[
            (plans["product_id"] == product_id) &
            (plans["plan_price"] < current_price)
        ]
        if not lower_plans.empty:
            return lower_plans.sample(1).iloc[0], "downgraded"

    # Fallback if no valid change found → treat as churn
    return None, "cancelled"


def generate_subscriptions(customers, plans, start_id=100):
    """
    Generate subscription records with realistic lifecycle events.
    Supports:
    - Upgrade (Free -> Pro, Pro -> Premium)
    - Downgrade (Premium -> Pro, Pro -> Free)
    - Cancellation (no new plan)
    """

    subscriptions = []
    sub_id = start_id

    for _, c in customers.iterrows():
        # Initial plan assigned randomly
        plan = plans.sample(1).iloc[0]
        start_date = START_DATE + timedelta(days=random.randint(0, (END_DATE - START_DATE).days))
        row = generate_subscription_row(sub_id, c.customer_id, plan, start_date)
        subscriptions.append(row)
        sub_id += 1

        # Simulate plan change for some users
        if random.random() < UPGRADE_PROBABILITY:
            switch_date = start_date + timedelta(days=random.randint(60, 720))
            if switch_date > END_DATE:
                switch_date = END_DATE

            new_plan, status = choose_new_plan(plan, plans)

            # Update current subscription with the reason for change
            subscriptions[-1][4] = switch_date   # end_date
            subscriptions[-1][5] = status        # upgraded / downgraded / cancelled
            subscriptions[-1][6] = switch_date   # cancel_date (end date)

            # If customer switches plan (not churn), add new subscription
            if new_plan is not None:
                new_row = generate_subscription_row(
                    sub_id,
                    c.customer_id,
                    new_plan,
                    switch_date,
                    status="active"
                )
                subscriptions.append(new_row)
                sub_id += 1

    return pd.DataFrame(
        subscriptions,
        columns=[
            "subscription_id",
            "customer_id",
            "plan_id",
            "start_date",
            "end_date",
            "status",
            "cancel_date",
        ],
    )


def generate_discounts() -> pd.DataFrame:

    """
    Return the static list of discounts as a DataFrame.

    Discounts are defined in config.py to keep data generation flexible.
    
    Returns:
        pd.DataFrame: DataFrame with discount information.
    """
    discounts = pd.DataFrame(DISCOUNTS)

    # Forcing data type
    discounts["valid_from"] = pd.to_datetime(discounts["valid_from"])
    discounts["valid_to"] = pd.to_datetime(discounts["valid_from"])
    return discounts

def generate_subscription_discounts(subscriptions, plans, discounts, start_id = 3000):
    """
    Generate a mapping of subscriptions to applied discounts.

    Args:
        subscriptions (pd.DataFrame): Subscriptions dataset
        plans (pd.DataFrame): Plans dataset
        discounts (pd.DataFrame): Discounts dataset

    Returns:
        pd.DataFrame: Subscription discounts dataset
    """
    rows = []
    sub_discount_id = start_id
    
    # Randomly assign discounts to ~50% of subscriptions
    for _, sub in subscriptions.sample(frac=0.5).iterrows():
        # Fetch the plan
        plan = plans[plans.plan_id == sub.plan_id].iloc[0]
        
        # Skip free plans (no discounts on already free tiers)
        if plan.plan_price == 0:
            continue
        
        # Otherwise assign a random discount
        discount = discounts.sample(1).iloc[0]
        
        rows.append([
            sub_discount_id,
            sub.subscription_id,
            discount.discount_id,
            sub.start_date,
            sub.end_date
        ])
        
        sub_discount_id += 1
    
    return pd.DataFrame(
        rows,
        columns=[
            "sub_discount_id",
            "subscription_id",
            "discount_id",
            "applied_date",
            "expiry_date",
        ],
    )

def create_line_item(line_item_id, invoice_id, plan_id, description, amount, line_type):
    """
    Helper to create a line item record.
    """
    return [line_item_id, invoice_id, plan_id, description, amount, line_type]

def apply_discounts(line_items, line_item_id, invoice_id, plan, invoice_date, sub, discounts, subscription_discounts, cycle_number):
    """
    Check and apply discounts for a given subscription cycle.
    """
    active_discounts = subscription_discounts[subscription_discounts.subscription_id == sub.subscription_id]
    for _, sd in active_discounts.iterrows():
        if sd.applied_date <= invoice_date <= (sd.expiry_date or END_DATE):
            disc = discounts[discounts.discount_id == sd.discount_id].iloc[0]

            # Recurring or first cycle only
            if disc.is_recurring or (not disc.is_recurring and cycle_number == 0):
                if disc.discount_type == "percent":
                    discount = -plan.plan_price * (disc.discount_value / 100)
                else:
                    discount = -disc.discount_value
                line_items.append(
                    create_line_item(line_item_id, invoice_id, None, f"Coupon {disc.discount_code}", discount, "discount")
                )
                line_item_id += 1
    return line_item_id

def generate_payments_invoice(subscriptions, plans, discounts, subscription_discounts, start_invoice_id = 1000, start_pay_id = 5000, start_line_id = 2000):
    """
    Generate invoices, line items, and payments for subscriptions.

    Args:
        subscriptions (pd.DataFrame)
        plans (pd.DataFrame)
        discounts (pd.DataFrame)
        subscription_discounts (pd.DataFrame)

    Returns:
        invoices_df, line_items_df, payments_df
    """
    invoices, line_items, payments = [], [], []
    invoice_id = start_invoice_id
    payment_id = start_pay_id
    line_item_id = start_line_id

    for _, sub in subscriptions.iterrows():
        plan = plans[plans.plan_id == sub.plan_id].iloc[0]

        # Determine billing cycle
        cycle_days = MONTHLY_CYCLE_DAYS if plan.recurring == "monthly" else YEARLY_CYCLE_DAYS

        cycle_number = 0
        while True:
            if plan.recurring == "monthly":
                invoice_date = sub.start_date + relativedelta(months=cycle_number)
            else:
                invoice_date = sub.start_date + relativedelta(years=cycle_number)
            if invoice_date > END_DATE:
                break
            if sub.end_date and invoice_date > sub.end_date:
                break

            # Base plan line item
            line_items.append(
                create_line_item(line_item_id, invoice_id, plan.plan_id, f"{plan.plan_name} Plan", plan.plan_price, "charge")
            )
            line_item_id += 1

            # Discounts
            if plan.plan_price > 0:
                line_item_id = apply_discounts(
                    line_items, line_item_id, invoice_id, plan, invoice_date, sub, discounts, subscription_discounts, cycle_number
                )

            # Total for this invoice
            total = sum(li[4] for li in line_items if li[1] == invoice_id)
            status = None
            # Payment logic
            if plan.plan_price == 0.0:
                # Free plan - always considered successful, no retries needed
                status = "success"
                payments.append([payment_id, invoice_id, invoice_date + timedelta(days=1), 0.0, "success", "N/A"])
            else:
                status = np.random.choice(["success", "failed", "pending"], p=[0.7, 0.2, 0.1])
                amount_paid = total if status == "success" else 0
                payments.append([
                    payment_id,
                    invoice_id,
                    invoice_date + timedelta(days=1),
                    amount_paid,
                    status,
                    np.random.choice(["Debit", "Credit", "Paypal"]),
                ])
            payment_id += 1

            # Retry if payment failed or pending (not needed for free plans since status = success)
            retries = 0
            last_status = status
            last_date = invoice_date + timedelta(days=1)
            while last_status in ["failed", "pending"] and retries < 2:
                delay = np.random.randint(2,8) #retry after 2-7 days
                retry_date = last_date + timedelta(days=delay)
                retry_status = np.random.choice(["success", "failed", "pending"], p=[0.7, 0.2, 0.1])
                amount_paid = total if retry_status == 'success' else 0

                payments.append([
                    payment_id,
                    invoice_id,
                    retry_date,
                    amount_paid,
                    retry_status,
                    np.random.choice(["Debit", "Credit", "Paypal"])
                ])
                payment_id += 1 

                last_status = retry_status
                last_date = retry_date
                retries += 1

                if last_status == 'success':
                    break
            
            # Final invoice status after retries
            if last_status == 'success':
                invoice_status = "paid"
            else:
                invoice_status = "past_due"
            
            # Append invoice record once per cycle
            invoices.append([
                invoice_id,
                sub.subscription_id,
                invoice_date,
                total,
                invoice_status
            ])

            # Increment counters
            invoice_id += 1
            cycle_number += 1

    invoices_df = pd.DataFrame(invoices, columns=["invoice_id", "subscription_id", "invoice_date", "total_due", "invoice_status"])
    line_items_df = pd.DataFrame(line_items, columns=["line_item_id", "invoice_id", "plan_id", "description", "amount", "line_type"])
    payments_df = pd.DataFrame(payments, columns=["payment_id", "invoice_id", "payment_date", "amount_paid", "payment_status", "payment_method"])

    return invoices_df, line_items_df, payments_df