-- CUADRE DE CIFRAS

--  1 Transaction (we know is squared if it matches with the Excel)
-- SELECT type, COUNT(*) as count
-- FROM cross_border_transactions.transaction
-- GROUP BY type
# ------------------------

-- 2 Acquiring company (cross check with ac_locations) both should have the same `ac_id` count
-- 16009 on 21-03-2023
-- SELECT COUNT(distinct(ac_id)) as count
-- FROM cross_border_transactions.acquiring_company
-- 16587 on 21-03-2023

-- SELECT COUNT(*) as count
-- FROM cross_border_transactions.ac_locations

# ------------------------


-- SELECT COUNT(*) as count
-- FROM cross_border_transactions.merging_company;

SELECT COUNT(distinct(m_id)) as count
FROM cross_border_transactions.view_merging_companies;

-- SELECT COUNT(distinct(ac_id)) as count
-- FROM cross_border_transactions.ac_locations

-- SELECT type, COUNT(*) as count
-- FROM cross_border_transactions.view_cross_border_transactions
-- GROUP BY type

-- SELECT type, COUNT(DISTINCT(ct_id)) as count
-- FROM cross_border_transactions.view_employee_thresholds
-- GROUP BY type

