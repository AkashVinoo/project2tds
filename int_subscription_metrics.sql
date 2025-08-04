{{--
    int_subscription_metrics.sql

    Intermediate model for monthly subscription analytics.
    - Joins customer and subscription data
    - Cleans and aggregates for downstream marts
    - Filters to last 90 days

    dbt Best Practices:
    - Uses {{ ref() }} for dependencies
    - CTEs for logical steps
    - Jinja templating
    - Consistent naming (int_ prefix)
    - Well-documented business logic
--}}

WITH

-- 1. Filter subscriptions to those created or active in the last 90 days
recent_subscriptions AS (
    SELECT
        subscription_id,
        customer_id,
        plan_id,
        status,
        start_date,
        end_date,
        created_at,
        updated_at
    FROM {{ ref('stg_subscriptions') }}
    WHERE
        start_date >= dateadd('day', -90, current_date)
        OR (end_date IS NULL OR end_date >= dateadd('day', -90, current_date))
),

-- 2. Select and clean customer details
customer_details AS (
    SELECT
        customer_id,
        TRIM(full_name) AS full_name,
        LOWER(email) AS email,
        region
    FROM {{ ref('stg_customers') }}
),

-- 3. Join subscriptions to customer details
subscriptions_joined AS (
    SELECT
        rs.subscription_id,
        rs.customer_id,
        cd.full_name,
        cd.email,
        cd.region,
        rs.plan_id,
        rs.status,
        rs.start_date,
        rs.end_date,
        rs.created_at,
        rs.updated_at
    FROM recent_subscriptions rs
    LEFT JOIN customer_details cd
        ON rs.customer_id = cd.customer_id
),

-- 4. Aggregate to monthly granularity for metrics
monthly_metrics AS (
    SELECT
        DATE_TRUNC('month', start_date) AS month,
        region,
        COUNT(DISTINCT subscription_id) AS subscriptions_started,
        COUNT(DISTINCT CASE WHEN status = 'active' THEN subscription_id END) AS active_subscriptions
    FROM subscriptions_joined
    GROUP BY 1, 2
)

SELECT *
FROM monthly_metrics
ORDER BY month DESC, region 