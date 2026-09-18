import pandas as pd

orders = pd.read_csv("data/orders.csv")

# Convert quantity to numeric.
# Invalid values such as "abc" become NaN.
orders["quantity_numeric"] = pd.to_numeric(
    orders["quantity"],
    errors="coerce"
)

# Identify invalid quantities.
invalid_quantity = (
    orders["quantity_numeric"].isna()
    | (orders["quantity_numeric"] > 10)
    | (orders["quantity_numeric"] <= 0)
)

# print("Invalid quantity rows:", invalid_quantity.sum())

# Split the data using the boolean mask.
invalid_orders = orders[invalid_quantity].copy()
valid_orders = orders[~invalid_quantity].copy()

# Add reason for rejection.
invalid_orders["reject_reason"] = "INVALID_QUANTITY"

# Save rejected records.
invalid_orders.to_csv(
    "output/rejects/invalid_data.csv",
    index=False
)

# print("Valid orders:", len(valid_orders))
# print("Invalid orders:", len(invalid_orders))
# print("Reject file created successfully.")

customer=pd.read_csv('data/customers.csv')

customer_exist=orders['customer_id'].isin(customer['customer_id'])

# print(customer_exist.value_counts())

customer_not_exist=orders[~customer_exist].copy()

# orphan_id=orders[~null_id]
missing_id=customer_not_exist[customer_not_exist['customer_id'].isna()]
orphan_id=customer_not_exist[~customer_not_exist['customer_id'].isna()].copy()


orders['customer_match_status']='Matched'
orders.loc[orders['customer_id'].isna(),'customer_match_status']='missing'

orders.loc[orders['customer_id'].isin(orphan_id['customer_id']),'customer_match_status']='orphan'
# print('new data',orders.head(100))

# print(orders["customer_match_status"].value_counts())

products=pd.read_csv('data/products.csv')

product_exist=orders['product_id'].isin(products['product_id'])

orders['product_status_match']='matched'

orders.loc[~product_exist,'product_status_match']='orphan'

# print(orders['product_status_match'].value_counts())

# orders['order_date']=pd.to_datetime(orders['order_date'],errors='coerce')
# test_date=pd.to_datetime(orders['order_date'],errors='coerce')
# print(test_date.dtype)
# print(test_date.isna().sum())


orders['test_date_clean']=pd.to_datetime(orders['order_date'],errors='coerce')


orders['test_date_status']='valid'

orders.loc[(orders['test_date_clean'].isna()) &
 (~orders['order_date'].isna()),'test_date_status']='invalid'

orders.loc[orders['order_date'].isna(),'test_date_status']='originally_missing'

# print(orders['test_date_status'].value_counts())

# print(orders['amount'].describe())

unknown=orders['amount'].isna()

unknown_df=orders[orders['amount'].isna()].copy()

# print(unknown_df.shape)

orders['clean_amount']=orders['amount']

merge_order=orders.merge(products,on='product_id')

# print(merge_order.shape)
# print(merge_order.head())




orders.loc[(unknown_df['product_id'].isin(products['product_id']))&
  (~merge_order['quantity_numeric'].isna()),'clean_amount']=merge_order['price']*merge_order['quantity_numeric']
print(orders['clean_amount'].isna().sum())


