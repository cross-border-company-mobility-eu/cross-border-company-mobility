CREATE VIEW cross_border_transactions.view_cross_border_transactions AS
(
	SELECT
		tr.ct_id AS ct_id,
		tr.date AS date,
		tr.type AS type,
		tr.researcher AS researcher,
		tr.comment AS comment,
		tr.found_registry AS found_registry,
		tr.completion_date AS completion_date,
		tr.lawfirm AS lawfirm,
		tr.multi_cbm AS multi_cbm,
		t1.name AS name,
		t1.employee_number AS employee_number,
		t1.year_employee AS year_employee,
		t1.total_employee_number_eu AS total_employee_number_eu,
		t1.total_employee_number_ww AS total_employee_number_ww,
		t1.year_total_employee AS year_total_employee,
		t1.diverging_employee_number AS diverging_employee_number,
		t1.year_diverging_employee AS year_diverging_employee,
		t1.company_form AS company_form,
		t1.ac_listed AS ac_listed,
		t1.sector AS sector,
		t1.nace_code AS nace_code,
		t1.nat_registration_number AS nat_registration_number,
		t1.tnic AS tnic,
		t1.ewc AS ewc,
		t1.company_website AS company_website,
		t1.parent_name AS parent_name,
		t1.ac_location AS ac_location,
		t1.ac_iso AS ac_iso,
		t1.ac_location2 AS ac_location2,
		t2.mc_name AS mc_name,
		t2.memployee_number AS memployee_number,
		t2.myear_employee AS myear_employee,
		t2.mcompany_form AS mcompany_form,
		t2.mnace_code AS mnace_code,
		t2.mnat_registration_number AS mnat_registration_number,
		t2.msector AS msector,
		t2.mc_location AS mc_location,
		t2.mc_iso AS mc_iso,
		t2.mc_location2 AS mc_location2,
		td.transaction_plan AS transaction_plan,
		td.company_has_employees AS company_has_employees,
		td.company_has_workscouncil AS company_has_workscouncil,
		td.company_has_economiccommittee AS company_has_economiccommittee,
		td.impact_on_employees AS impact_on_employees,
		td.negotiated_agreement AS negotiated_agreement,
		td.sbn_voluntary_application AS sbn_voluntary_application,
		td.standard_rule_application AS standard_rule_application,
		td.bler_existing AS bler_existing,
		td.bler_to_negotiate AS bler_to_negotiate,
		td.bler_composition AS bler_composition
	FROM (( cross_border_transactions.transaction tr
			JOIN (
				SELECT
					ac.ac_id AS a_id,
					ac.ac_id AS ac_id,
					ac.name AS name,
					ac.employee_number AS employee_number,
					ac.year_employee AS year_employee,
					ac.total_employee_number_eu AS total_employee_number_eu,
					ac.total_employee_number_ww AS total_employee_number_ww,
					ac.year_total_employee AS year_total_employee,
					ac.diverging_employee_number AS diverging_employee_number,
					ac.year_diverging_employee AS year_diverging_employee,
					ac.company_form AS company_form,
					ac.ac_listed AS ac_listed,
					ac.sector AS sector,
					ac.nace_code AS nace_code,
					ac.nat_registration_number AS nat_registration_number,
					ac.tnic AS tnic,
					ac.ewc AS ewc,
					ac.p_id AS p_id,
					ac.company_website AS company_website,
					p.name AS parent_name,
					l.name AS ac_location,
					l.iso_id AS ac_iso,
					ac.secondary_location AS ac_location2
				FROM ((( cross_border_transactions.acquiring_company ac
							LEFT JOIN cross_border_transactions.ac_locations al ON ((ac.ac_id = al.ac_id)))
						LEFT JOIN cross_border_transactions.location l ON ((al.Location_id = l.location_id)))
					LEFT JOIN cross_border_transactions.parent_company p ON ((ac.p_id = p.p_id)))) t1 ON ((tr.ac_id = t1.a_id)))
			JOIN (
			SELECT
				mc.mc_id AS m_id,
				mc.name AS mc_name,
				mc.employee_number AS memployee_number,
				mc.year_employee AS myear_employee,
				mc.company_form AS mcompany_form,
				mc.nace_code AS mnace_code,
				mc.nat_registration_number AS mnat_registration_number,
				mc.sector AS msector,
				l.name AS mc_location,
				l.iso_id AS mc_iso,
				mc.secondary_location AS mc_location2
			FROM ((cross_border_transactions.merging_company mc
					LEFT JOIN cross_border_transactions.mc_locations ml ON ((mc.mc_id = ml.mc_id)))
				LEFT JOIN cross_border_transactions.location l ON ((ml.Location_id = l.location_id)))) t2 ON ((tr.mc_id = t2.m_id)))
				LEFT JOIN cross_border_transactions.transaction_details td ON tr.ct_id = td.ct_id
);