# Calculate average difference between completion_date and transaction date
WITH avg_difference AS (
    SELECT AVG(DATEDIFF(completion_date, date)) AS average_days_difference
    FROM transaction
    WHERE completion_date IS NOT NULL
    AND date IS NOT NULL
)
# Generate time series data transactions
SELECT 
    COALESCE(t.date, DATE_SUB(t.completion_date, INTERVAL (SELECT average_days_difference FROM avg_difference) DAY)) AS date_upgraded,
    COUNT(*) AS transactions_count
FROM transaction t
WHERE (t.date IS NOT NULL OR (t.date IS NULL AND t.completion_date IS NOT NULL))
GROUP BY date_upgraded
ORDER BY date_upgraded DESC;
