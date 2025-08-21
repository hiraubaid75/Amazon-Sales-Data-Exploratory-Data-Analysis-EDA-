# 🧪 Hypothesis Testing

> Note: Methods are auto-picked based on variable types. Replace/expand as needed.

## H1: Return rates are the same for Mobile vs Desktop
- Test: Chi-square test on contingency table (Device × Returned)
- Result: <<stat, p-value>>
- Interpretation: <<accept/reject H0>>

## H2: Discount % does not affect Quantity sold
- Test: Correlation and simple regression check
- Result: <<coef, p-value>>
- Interpretation: <<accept/reject H0>>

## H3: Younger (18–25) vs older groups have same return rate
- Test: Chi-square (AgeGroup × Returned)
- Result: <<stat, p-value>>
- Interpretation: <<accept/reject H0>>

## H4: Delivery performance consistent across regions
- Test: Chi-square (Region × DeliveryStatus)
- Result: <<stat, p-value>>
- Interpretation: <<accept/reject H0>>

## H5: Brand does not influence return probability
- Test: Chi-square (Brand × Returned) [filter to top brands]
- Result: <<stat, p-value>>
- Interpretation: <<accept/reject H0>>
