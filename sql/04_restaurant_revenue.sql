SELECT
    name,
    SUM(total_revenue) AS revenue
FROM food_analytics.daily_restaurant_metrics
GROUP BY name
ORDER BY revenue DESC
LIMIT 5;
