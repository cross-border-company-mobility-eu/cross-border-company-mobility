-- SELECT * FROM cross_border_transactions.view_merging_companies
-- where m_id = 11722;

SELECT count(*) 
FROM (
SELECT vmc.*
FROM cross_border_transactions.view_merging_companies vmc
JOIN (
    SELECT mc_id, MIN(unique_mc_id) AS min_id
    FROM cross_border_transactions.view_merging_companies
    GROUP BY mc_id
) AS subquery ON vmc.mc_id = subquery.mc_id AND vmc.unique_mc_id = subquery.min_id
) as allr;

select count(*) from(
SELECT mc_id, MIN(unique_mc_id) AS min_id
FROM cross_border_transactions.view_merging_companies
GROUP BY mc_id
) as allf

-- select count(*) from(
-- SELECT distinct mc_id
-- FROM cross_border_transactions.view_merging_companies
-- ) ghs;