# Exporting all unique companies from CbCM database
WITH combined AS (
    SELECT mc_id AS id, name, nat_registration_number 
    FROM cross_border_transactions.merging_company AS MC
    UNION
    SELECT ac_id AS id, name, nat_registration_number 
    FROM cross_border_transactions.acquiring_company AS AC
    UNION
    SELECT p_id AS id, name, NULL AS nat_registration_number 
    FROM cross_border_transactions.parent_company AS P
),
filtered_combined AS (
    SELECT id, name, nat_registration_number,
        ROW_NUMBER() OVER (PARTITION BY name ORDER BY CASE WHEN nat_registration_number IS NOT NULL THEN 1 ELSE 2 END) AS rn
    FROM combined
),
unique_combined AS (
    SELECT id, name, nat_registration_number
    FROM filtered_combined
    WHERE rn = 1
)
SELECT id, name, nat_registration_number
FROM unique_combined
ORDER BY name, nat_registration_number;
