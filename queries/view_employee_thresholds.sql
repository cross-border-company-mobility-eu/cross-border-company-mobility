CREATE VIEW cross_border_transactions.view_employee_thresholds AS
(
	SELECT CBT.ct_id, 
	CBT.date, 
	LOC.name as country, 
	"AC" as company_role,
	CBT.type,
	AC.name,
	AC.nat_registration_number,
	AC.employee_number as employee_number,
	CASE
			   WHEN AC.employee_number = 0 THEN '0'
			   WHEN AC.employee_number > 0 AND AC.employee_number <= 5 THEN "1-5"
			   WHEN AC.employee_number > 6 AND AC.employee_number <= 50 THEN "6-50"
			   WHEN AC.employee_number > 50 AND AC.employee_number <= 100 THEN "51-100"
			   WHEN AC.employee_number > 100 AND AC.employee_number <= 300 THEN "101-300"
			   WHEN AC.employee_number > 300 AND AC.employee_number <= 500 THEN "301-500"
			   WHEN AC.employee_number > 500 AND AC.employee_number <= 1000 THEN "501-1000"
			   WHEN AC.employee_number > 1000 AND AC.employee_number <= 2000 THEN "1001-2000"
			   WHEN AC.employee_number > 2000 THEN ">2000"
			   WHEN AC.employee_number IS NULL THEN NULL
			   ELSE NULL
			END as employee_group
	FROM cross_border_transactions.transaction as CBT
	JOIN cross_border_transactions.acquiring_company as AC ON CBT.ac_id = AC.ac_id
	LEFT JOIN cross_border_transactions.ac_locations as ACL ON CBT.ac_id = ACL.ac_id
	LEFT JOIN cross_border_transactions.location as LOC ON ACL.Location_id = LOC.location_id
	UNION 
	SELECT CBT.ct_id, 
	CBT.date, 
	LOC.name as country, 
	"MC" as company_role,
	CBT.type,
	MC.name,
	MC.nat_registration_number,
	MC.employee_number as employee_number,
	CASE
			   WHEN MC.employee_number = 0 THEN '0'
			   WHEN MC.employee_number > 0 AND MC.employee_number <= 5 THEN "1-5"
			   WHEN MC.employee_number > 6 AND MC.employee_number <= 50 THEN "6-50"
			   WHEN MC.employee_number > 50 AND MC.employee_number <= 100 THEN "51-100"
			   WHEN MC.employee_number > 101 AND MC.employee_number <= 300 THEN "101-300"
			   WHEN MC.employee_number > 301 AND MC.employee_number <= 500 THEN "301-500"
			   WHEN MC.employee_number > 501 AND MC.employee_number <= 1000 THEN "501-1000"
			   WHEN MC.employee_number > 1001 AND MC.employee_number <= 2000 THEN "1001-2000"
			   WHEN MC.employee_number > 2000 THEN ">2000"
			   WHEN MC.employee_number IS NULL THEN NULL
			   ELSE NULL
			END as employee_group
	FROM cross_border_transactions.transaction as CBT
	JOIN cross_border_transactions.merging_company as MC ON CBT.ac_id = MC.mc_id
	LEFT JOIN cross_border_transactions.mc_locations as MCL ON CBT.ac_id = MCL.mc_id
	LEFT JOIN cross_border_transactions.location as LOC ON MCL.Location_id = LOC.location_id
	)
;

