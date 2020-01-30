SELECT
	CBT.ct_id,
	LOC.name AS country,
	AC.nat_registration_number AS nat_reg_num,
	'AC' AS cbm_type,
	AC.employee_number AS employee_number,
	AC.company_form AS company_form
FROM
	cross_border_transactions.transaction AS CBT
	JOIN cross_border_transactions.acquiring_company AS AC ON CBT.ct_id = AC.ac_id
	JOIN cross_border_transactions.ac_locations AS ACL ON CBT.Acquiring_company_ac_id = ACL.ac_id
	LEFT JOIN cross_border_transactions.location AS LOC ON ACL.Location_id = LOC.id
WHERE
	CBT.type = 'CBM'
	AND(LOC.iso_id = 'AT'
		AND AC.employee_number > 300
		AND AC.company_form = 'Public limited - AG')
	OR(LOC.iso_id = 'HR'
		AND AC.employee_number > 200)
	OR(LOC.iso_id = 'AT'
		AND AC.employee_number > 300)
	OR(LOC.iso_id = 'HR'
		AND AC.employee_number > 200)
	OR(LOC.iso_id = 'CZ'
		AND AC.employee_number > 50)
	OR(LOC.iso_id = 'DK'
		AND AC.employee_number > 35)
	OR(LOC.iso_id = 'FI'
		AND AC.employee_number > 150)
	OR(LOC.iso_id = 'FR'
		AND AC.employee_number > 1000)
	OR(LOC.iso_id = 'DE'
		AND AC.employee_number > 500)
	OR(LOC.iso_id = 'HU'
		AND AC.employee_number > 200)
	OR(LOC.iso_id = 'LU'
		AND AC.employee_number > 1000)
	OR(LOC.iso_id = 'NL'
		AND AC.employee_number > 100)
	OR(LOC.iso_id = 'NO'
		AND AC.employee_number > 30)
	OR(LOC.iso_id = 'SE'
		AND AC.employee_number > 25)
	OR(LOC.iso_id = 'SK'
		AND AC.employee_number > 50)
	OR(LOC.iso_id = 'SI'
		AND AC.employee_number > 50)
	OR(LOC.iso_id = 'LI'
		AND AC.employee_number > 500)
UNION
SELECT
	CBT.ct_id,
	LOC.name AS country,
	MC.nat_registration_number AS nat_reg_num,
	'MC' AS cbm_type,
	MC.employee_number AS employee_number,
	MC.company_form AS company_form
FROM
	cross_border_transactions.transaction AS CBT
	JOIN cross_border_transactions.merging_company AS MC ON CBT.ct_id = MC.mc_id
	JOIN cross_border_transactions.mc_locations AS MCL ON CBT.Acquiring_company_ac_id = MCL.mc_id
	LEFT JOIN cross_border_transactions.location AS LOC ON MCL.Location_id = LOC.id
WHERE
	CBT.type = 'CBM'
	AND(LOC.iso_id = 'AT'
		AND MC.employee_number > 300
		AND MC.company_form = 'Public limited - AG')
	OR(LOC.iso_id = 'HR'
		AND MC.employee_number > 200)
	OR(LOC.iso_id = 'AT'
		AND MC.employee_number > 300)
	OR(LOC.iso_id = 'HR'
		AND MC.employee_number > 200)
	OR(LOC.iso_id = 'CZ'
		AND MC.employee_number > 50)
	OR(LOC.iso_id = 'DK'
		AND MC.employee_number > 35)
	OR(LOC.iso_id = 'FI'
		AND MC.employee_number > 150)
	OR(LOC.iso_id = 'FR'
		AND MC.employee_number > 1000)
	OR(LOC.iso_id = 'DE'
		AND MC.employee_number > 500)
	OR(LOC.iso_id = 'HU'
		AND MC.employee_number > 200)
	OR(LOC.iso_id = 'LU'
		AND MC.employee_number > 1000)
	OR(LOC.iso_id = 'NL'
		AND MC.employee_number > 100)
	OR(LOC.iso_id = 'NO'
		AND MC.employee_number > 30)
	OR(LOC.iso_id = 'SE'
		AND MC.employee_number > 25)
	OR(LOC.iso_id = 'SK'
		AND MC.employee_number > 50)
	OR(LOC.iso_id = 'SI'
		AND MC.employee_number > 50)
	OR(LOC.iso_id = 'LI'
		AND MC.employee_number > 500)
;