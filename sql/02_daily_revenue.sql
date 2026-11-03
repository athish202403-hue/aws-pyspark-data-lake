SELECT
    order_date,
    SUM(total_revenue) AS daily_revenue
FROM food_analytics.daily_restaurant_metrics
GROUP BY order_date
ORDER BY order_date;
