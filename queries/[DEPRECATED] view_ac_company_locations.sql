CREATE VIEW cross_border_transactions.view_acquiring_companies AS
SELECT
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
FROM cross_border_transactions.acquiring_company ac
LEFT JOIN cross_border_transactions.ac_locations al ON (ac.ac_id = al.ac_id)
LEFT JOIN cross_border_transactions.location l ON (al.Location_id = l.location_id)
LEFT JOIN cross_border_transactions.parent_company p ON (ac.p_id = p.p_id);
