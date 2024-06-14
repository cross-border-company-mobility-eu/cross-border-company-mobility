# Calculate the total transactions and dates nullity
SELECT
    COUNT(*) AS total_transactions,
    SUM(CASE WHEN t.completion_date IS NULL THEN 1 ELSE 0 END) AS null_completion_date,
    SUM(CASE WHEN t.date IS NULL THEN 1 ELSE 0 END) AS null_date,
    SUM(CASE WHEN t.completion_date IS NULL AND t.date IS NULL THEN 1 ELSE 0 END) AS both_null,
    SUM(CASE WHEN t.completion_date IS NULL AND t.date IS NOT NULL THEN 1 ELSE 0 END) AS completion_date_null_only,
    SUM(CASE WHEN t.completion_date IS NOT NULL AND t.date IS NULL THEN 1 ELSE 0 END) AS date_null_only
FROM transaction t;
