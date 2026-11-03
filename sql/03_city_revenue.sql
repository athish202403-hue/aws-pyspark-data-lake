SELECT
    city,
    SUM(total_revenue) AS city_revenue
FROM food_analytics.daily_restaurant_metrics
GROUP BY city
ORDER BY city_revenue DESC;
