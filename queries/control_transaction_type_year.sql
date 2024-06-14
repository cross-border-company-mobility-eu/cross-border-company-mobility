SELECT T.type, EXTRACT(YEAR FROM T.date) as year, count(*) 
FROM transaction as T
GROUP BY type, year
ORDER BY type, year