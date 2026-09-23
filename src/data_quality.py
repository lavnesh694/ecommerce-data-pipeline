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

orders['row_id']=orders.index

# print(merge_order.shape)
# print(merge_order.head())




can_calculate_sum=(orders['product_id'].isin(products['product_id'])& (orders['quantity_numeric'].notna()) &
  (orders['quantity_numeric']>=1) & (orders['quantity_numeric']<=10))

merge_order=orders.merge(products[['price','product_id']],on='product_id',how='left')

merge_order['calculated_amount']=merge_order['price']*merge_order['quantity_numeric']

# print(merge_order[['product_id', 'price', 'quantity_numeric', 'calculated_amount']].head())

orders.loc[can_calculate_sum,'clean_amount']=merge_order.loc[can_calculate_sum,'calculated_amount']

orders['amount_status']='matched'

orders.loc[(round(orders['clean_amount'],2)!=round(orders['amount'],2)) & (orders['amount'].isna()),'amount_status']="Reconstructed"
orders.loc[(round(orders['clean_amount'],2)!=round(orders['amount'],2)) & (~orders['amount'].isna()),'amount_status']="Mismatched"
orders.loc[(round(orders['clean_amount'],2)!=round(orders['amount'],2)) & (~orders['amount'].isna()) & (orders['clean_amount'].isna()),'amount_status']="Not_calculated"




# print(orders['amount_status'].value_counts())



# now we have to calculate 504 mismatched values



mismatched=orders[orders['amount_status']=='Mismatched']

difference=mismatched['clean_amount']-mismatched['amount']

# print(difference.describe())

mismatched['difference']=mismatched['clean_amount']-mismatched['amount']

# print(mismatched.loc[mismatched['difference'].idxmin()])




# print(mismatched.loc[mismatched['difference'].idxmax()])

# print(products[products['product_id']=='PROD0020'])

orders.loc[orders['amount_status']=='Mismatched','reject_reason']='INVALID_AMOUNT'
orders.loc[(orders['quantity_numeric']<=0) | (orders['quantity_numeric']>10) | (orders['quantity_numeric'].isna()),'reject_reason']='INVALID_QUANTITY'

# print(orders['reject_reason'].value_counts());
# print(orders['quantity_numeric'].isna().sum());

invalid=orders[(orders['amount_status']=='Mismatched') |
 ((orders['quantity_numeric']<=0) | (orders['quantity_numeric']>10) |
  orders['quantity_numeric'].isna())]

# print(invalid.shape)

invalid.to_csv('output/rejects/invalid_data.csv')

valid=orders[~((orders['amount_status']=='Mismatched') |
 ((orders['quantity_numeric']<=0) | (orders['quantity_numeric']>10) |
  orders['quantity_numeric'].isna()))]

# print(orders['order_id'].duplicated().sum())

# print(orders['order_date'].dtype)

# invalid_order_ids = invalid['order_id'].nunique()
# print(invalid_order_ids)

# print(orders['order_id'].isin(invalid['order_id']).sum())
# orders=orders['amount'].rename('source_amount',inplace=True)
# orders=orders['clean_amount'].rename('amount',inplace=True)

# print(orders.columns)



valid = valid.rename(columns={
    'amount': 'source_amount',
    'clean_amount': 'amount'
})
valid = valid.drop(columns=[
    'quantity_numeric',
    'test_date_clean',
    'row_id',
    'reject_reason'
])


# valid.to_csv('output/curated/orders_clean.csv')

# lets start order_status


valid['order_status']=valid['order_status'].str.strip().str.lower()

# print(valid['order_status'].value_counts())


valid.to_csv('output/curated/orders_clean.csv')
valid_before_dedup_count = len(valid)
duplicates_removed_count = valid.duplicated().sum()

duplicates= valid[valid['order_id'].duplicated(keep=False)].sort_values(by='order_id')
# print(duplicates.size)
# print(duplicates.head(10))
# print(duplicates.head(10).to_string(index=False))

duplicates = duplicates.reset_index(drop=True)

print(duplicates.head(10))

print(duplicates.duplicated().sum())

valid=valid.drop_duplicates(keep='first')

print(valid.shape)

valid.to_csv('output/curated/orders_clean.csv',index=False)

# Keep one canonical copy of each exact duplicate record.


# Pipeline audit report: one data-quality metric per row.
data_quality_summary = pd.DataFrame({
    "metric": [
        "raw_orders",
        "missing_customer_id",
        "orphan_customer_id",
        "orphan_product_id",
        "invalid_order_date",
        "missing_order_date",
        "invalid_quantity",
        "reconstructed_amount",
        "mismatched_amount",
        "total_rejected",
        "valid_before_dedup",
        "exact_duplicates_removed",
        "final_curated_orders",
    ],
    "count": [
        len(orders),
        (orders["customer_match_status"] == "missing").sum(),
        (orders["customer_match_status"] == "orphan").sum(),
        (orders["product_status_match"] == "orphan").sum(),
        (orders["test_date_status"] == "invalid").sum(),
        (orders["test_date_status"] == "originally_missing").sum(),
        invalid_quantity.sum(),
        (orders["amount_status"] == "Reconstructed").sum(),
        (orders["amount_status"] == "Mismatched").sum(),
        len(invalid),
        valid_before_dedup_count,
        duplicates_removed_count,
        len(valid),
    ],
})

data_quality_summary.to_csv(
    "output/data_quality_summary.csv",
    index=False,
)

print("Data-quality summary created:")
print(data_quality_summary)
