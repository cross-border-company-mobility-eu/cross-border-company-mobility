-- SELECT T.type, count(*)
-- FROM cross_border_transactions.transaction as T
-- GROUP BY T.type;

# checking null dates
SELECT count(*)
FROM cross_border_transactions.transaction as T
WHERE T.type = 'SE'
AND T.date < "1950/01/01";