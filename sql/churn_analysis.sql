SELECT
    s.internet_type,
    COUNT(*) AS customers,
    SUM(c.churn) AS churned_customers,
    ROUND(100*SUM(c.churn) / COUNT(c.churn),2) AS churn_rate_pct
FROM customers AS c
JOIN customer_services AS s
    ON c.customer_id = s.customer_id
WHERE c.churn IS NOT NULL
GROUP BY s.internet_type
ORDER BY churned_rate_pct DESC;

SELECT
    s.premium_tech_support,
    COUNT(*) AS customers,
    ROUND(100.0 * SUM(c.churn) / COUNT(c.churn), 2) AS churn_rate_pct
FROM customers AS c
JOIN customer_services AS s
    ON c.customer_id = s.customer_id
WHERE c.churn IS NOT NULL
GROUP BY s.premium_tech_support
ORDER BY churned_rate_pct DESC;

--Moving our focus to churn rate by contract risk, revenue risk, tenure risk and churn reason

--Looking at churn rate by contract type
SELECT
    a.contract,
    COUNT(c.churn) AS customers,
    SUM(c.churn) AS churned_customers,
    ROUND(100*SUM(c.churn)/COUNT(c.churn), 2) AS churn_rate_pct
FROM customers as c
JOIN customer_accounts as a
    ON c.customer_id = a.customer_id
WHERE c.churn IS NOT NULL
GROUP BY a.contract
ORDER BY churn_rate_pct DESC;

--tenure risk
SELECT
    CASE
        WHEN tenure_months <= 12 THEN '0-12 months'
        WHEN tenure_months <= 24 THEN '13-24 months'
        WHEN tenure_months <= 48 THEN '25-48 months'
        ELSE '49+ months'
    END AS tenure_group,
    COUNT(*) AS customers,
    ROUND(100*SUM(c.churn)/COUNT(c.churn), 2) AS churn_rate_pct
FROM customers AS c
WHERE churn IS NOT NULL
GROUP BY tenure_group
ORDER BY churn_rate_pct DESC;

--Revenue associated with churned customers
SELECT
    c.customer_status,
    COUNT(*) AS customers,
    ROUND(AVG(a.total_revenue), 2) AS avg_total_revenue,
    ROUND(SUM(a.total_revenue), 2) AS total_revenue
FROM customers AS c
JOIN customer_accounts AS a
    ON c.customer_id = a.customer_id
WHERE c.customer_status IN ('Stayed', 'Churned')
GROUP BY c.customer_status;

--Monthly revenue lost to churned customers
SELECT
    ROUND(SUM(a.monthly_charge), 2) AS monthly_revenue_lost
FROM customers AS c
JOIN customer_accounts AS a
    ON c.customer_id = a.customer_id
WHERE c.churn = 1;

--Looking at most common churn reasons
SELECT
    churn_reason,
    COUNT(*) AS customers
FROM customers
WHERE churn = 1
GROUP BY churn_reason
ORDER BY COUNT(*) DESC;

--Churn categories and percentage of churned customers associated w/ a category
SELECT
    churn_category,
    COUNT(*) AS customers,

    ROUND(
        100.0 * COUNT(*) /
        (
            SELECT COUNT(*)
            FROM customers
            WHERE churn = 1
        ), 2) AS percentage_of_churn
FROM customers
WHERE churn = 1
GROUP BY churn_category
ORDER BY COUNT(*) DESC;







