CREATE VIEW cross_border_transactions.view_merging_companies AS
SELECT
    CONCAT(mc.mc_id, '-', ml.Location_id) AS unique_mc_id,
    mc.mc_id AS mc_id,
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
FROM cross_border_transactions.merging_company mc
LEFT JOIN cross_border_transactions.mc_locations ml ON (mc.mc_id = ml.mc_id)
JOIN cross_border_transactions.location l ON (ml.Location_id = l.location_id);

