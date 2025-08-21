# 🧼 Data Quality Report

## 1) Overview
- Rows: <<25000>>
- Columns: <<19>>
- Time range: <<2025 sales DATA>>

## 2) Missingness

Missingness report:

                    missing_count  missing_pct
device_type                  1250          5.0
customer_age_group           1250          5.0
brand                        1250          5.0
region                       1250          5.0
payment_method               1250          5.0
delivery_days                 250          1.0
price                         250          1.0
product_id                      0          0.0
customer_id                     0          0.0
order_id                        0          0.0
main_category                   0          0.0
final_price                     0          0.0
discount_percent                0          0.0
quantity                        0          0.0
sub_category                    0          0.0
product_name                    0          0.0
review_rating                   0          0.0
order_date                      0          0.0
is_returned                     0          0.0

-device_type: 5.0 % missing -> impute or flag
-customer_age_group: 5.0 % missing -> impute or flag
-brand: 5.0 % missing -> impute or flag
-region: 5.0 % missing -> impute or flag
-payment_method: 5.0 % missing -> impute or flag
-delivery_days: 1.0 % missing -> impute or flag
-price: 1.0 % missing -> impute or flag

## 3) Duplicates

Checking duplicate order_id count:
0
duplicate order_id rows: 0

## 4) Data Types
```
	0
order_id	object
customer_id	object
product_id	object
product_name	object
main_category	object
sub_category	object
brand	object
price	float64
quantity	int64
discount_percent	int64
final_price	float64
payment_method	object
review_rating	int64
order_date	datetime64[ns]
delivery_days	float64
is_returned	int64
region	object
customer_age_group	object
device_type	object
df_calculated_final	float64
final_price_capped	float64
final_price_log	float64
order_month	period[M]
order_weekday	object
order_year	int32
discount_amount	float64
unit_price	float64
delivery_speed	object
delivery_bin	category
cohort	period[M]

```

## 5) Outliers (Numeric via IQR)
Number of numeric columns: 8
Numeric columns: ['price', 'quantity', 'discount_percent', 'final_price', 'review_rating', 'delivery_days', 'is_returned', 'df_calculated_final']
Numeric columns: ['delivery_days', 'discount_percent', 'final_price', 'price', 'quantity']

Outlier count for delivery_days: 0

Outlier count for discount_percent: 0

Outlier count for final_price: 174

Outlier count for price: 0

Outlier count for quantity: 0


## 6) Cleaning Actions
Highlight these extreme sales as key business insights.

During analysis, we identified 174 outliers in the final_price column using the IQR method. Since final_price represents revenue, these extreme values likely correspond to high-value sales, which are important business insights.

Instead of removing them, we applied the following strategies:

Capping: Values above the upper bound and below the lower bound were capped to reduce the effect of extreme values on statistical analysis.

Log Transformation: A log transformation was applied to reduce skewness and make visualizations and modeling more robust.

By keeping these outliers, we preserve valuable information about high-value transactions, which could help identify premium customer segments or trends in product pricing.
