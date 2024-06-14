SELECT
    mc_id,
    ac_id,
    COUNT(*) AS count
FROM
    cross_border_transactions.transaction
GROUP BY
    mc_id,
    ac_id
HAVING
    count > 1;
