SELECT mc_id AS id, name, nat_registration_number FROM cross_border_transactions.merging_company AS MC
UNION
SELECT ac_id AS id, name, nat_registration_number FROM cross_border_transactions.acquiring_company AS AC
UNION
SELECT p_id AS id, name, 'na' as nat_registration_number FROM cross_border_transactions.parent_company AS P