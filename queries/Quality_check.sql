-- SELECT T.type, count(*)
-- FROM cross_border_transactions.transaction as T
-- GROUP BY T.type;

# checking null dates
SELECT *
FROM cross_border_transactions.transaction as T
WHERE T.type = 'SE'
AND T.completion_date = "1900-01-01"


-- SELECT count(*) 
-- FROM cross_border_transactions.transaction as T
-- WHERE T.type = "CBM"
-- AND T.date < "2021/01/01"
-- AND T.date >= "2020/01/01"
-- -- AND T.date < "2022/01/01"
-- -- AND T.date >= "2021/01/01"