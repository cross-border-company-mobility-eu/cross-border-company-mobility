SELECT CBD.ct_id, 
CBD.date, 
LOC.name as country, 
"RC" as cbm_type,
AC.employee_number as employee_number,
CASE
           WHEN AC.employee_number = 0 THEN '0'
           WHEN AC.employee_number > 0 AND AC.employee_number <= 5 THEN "1-5"
           WHEN AC.employee_number > 6 AND AC.employee_number <= 50 THEN "6-50"
           WHEN AC.employee_number > 101 AND AC.employee_number <= 300 THEN "101-300"
           WHEN AC.employee_number > 301 AND AC.employee_number <= 500 THEN "301-500"
           WHEN AC.employee_number > 501 AND AC.employee_number <= 1000 THEN "501-1000"
           WHEN AC.employee_number > 1001 AND AC.employee_number <= 2000 THEN "1001-2000"
           WHEN AC.employee_number > 2000 THEN ">2000"
           WHEN AC.employee_number IS NULL THEN "n.a."
           ELSE "n.a."
        END as employee_group
FROM cross_border_transactions.transaction as CBD
JOIN cross_border_transactions.acquiring_company as AC ON CBD.ct_id = AC.ac_id
JOIN cross_border_transactions.ac_locations as ACL ON CBD.Acquiring_company_ac_id = ACL.ac_id
LEFT JOIN cross_border_transactions.location as LOC ON ACL.Location_id = LOC.id
WHERE CBD.type = "CBD"
UNION 
SELECT CBD.ct_id, 
CBD.date, 
LOC.name as country, 
"OC" as cbm_type,
MC.employee_number as employee_number,
CASE
           WHEN MC.employee_number = 0 THEN '0'
           WHEN MC.employee_number > 0 AND MC.employee_number <= 5 THEN "1-5"
           WHEN MC.employee_number > 6 AND MC.employee_number <= 50 THEN "6-50"
           WHEN MC.employee_number > 101 AND MC.employee_number <= 300 THEN "101-300"
           WHEN MC.employee_number > 301 AND MC.employee_number <= 500 THEN "301-500"
           WHEN MC.employee_number > 501 AND MC.employee_number <= 1000 THEN "501-1000"
           WHEN MC.employee_number > 1001 AND MC.employee_number <= 2000 THEN "1001-2000"
           WHEN MC.employee_number > 2000 THEN ">2000"
           WHEN MC.employee_number IS NULL THEN "n.a."
           ELSE "n.a."
        END as employee_group
FROM cross_border_transactions.transaction as CBD
JOIN cross_border_transactions.merging_company as MC ON CBD.ct_id = MC.mc_id
JOIN cross_border_transactions.mc_locations as MCL ON CBD.Acquiring_company_ac_id = MCL.mc_id
LEFT JOIN cross_border_transactions.location as LOC ON MCL.Location_id = LOC.id
WHERE CBD.type = "CBD"


