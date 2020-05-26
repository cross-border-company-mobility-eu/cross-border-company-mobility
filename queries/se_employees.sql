SELECT SE.ct_id, 
SE.date, 
LOC.name as country, 
"SE-SCE" as company_role,
AC.name,
AC.nat_registration_number,
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
FROM cross_border_transactions.transaction as SE
JOIN cross_border_transactions.acquiring_company as AC ON SE.ct_id = AC.ac_id
JOIN cross_border_transactions.ac_locations as ACL ON SE.ac_id = ACL.ac_id
LEFT JOIN cross_border_transactions.location as LOC ON ACL.Location_id = LOC.location_id
WHERE SE.type = "SE-SCE"