{{
    config(
        materialized='view'
    )
}}

-- Step 1: Clean and filter subscriptions for the last 90 days
with subscriptions as (
    select
        subscription_id,
        customer_id,
        plan_id,
        lower(trim(status)) as status,
        start_date,
        end_date,
        created_at,
        updated_at
    from {{ ref('stg_subscriptions') }}
    where
        start_date >= dateadd('day', -90, current_date)
        or (end_date is null or end_date >= dateadd('day', -90, current_date))
),

-- Step 2: Clean customer details
customers as (
    select
        customer_id,
        trim(full_name) as full_name,
        lower(trim(email)) as email,
        trim(region) as region
    from {{ ref('stg_customers') }}
),

-- Step 3: Join subscriptions to customers
joined as (
    select
        s.subscription_id,
        s.customer_id,
        c.full_name,
        c.email,
        c.region,
        s.plan_id,
        s.status,
        s.start_date,
        s.end_date,
        s.created_at,
        s.updated_at
    from subscriptions s
    left join customers c using (customer_id)
),

-- Step 4: Aggregate metrics by month and region
monthly_metrics as (
    select
        date_trunc('month', start_date) as subscription_month,
        region,
        count(distinct subscription_id) as subscriptions_started,
        count(distinct case when status = 'active' then subscription_id end) as active_subscriptions
    from joined
    group by 1, 2
)

select
    subscription_month,
    region,
    subscriptions_started,
    active_subscriptions
from monthly_metrics
order by subscription_month desc, region 