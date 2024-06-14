# Creating a Transactions view that makes emphasis on the date imputation
WITH avg_difference AS (
    SELECT AVG(DATEDIFF(completion_date, date)) AS average_days_difference
    FROM transaction
    WHERE completion_date IS NOT NULL
    AND date IS NOT NULL
),
unique_transactions AS (
    SELECT
        t.ct_id AS Ct_Id,
        t.date AS Date,
        t.type AS Type,
        t.completion_date AS Completion_Date,
        ac.name AS AC_name,
        ac.company_form AS AC_company_form,
        al.name AS AC_location,
        mc.name AS MC_name,
        mc.company_form AS MC_company_form,
        ml.name AS MC_location,
        DATEDIFF(t.completion_date, t.date) AS Difference_in_Days,
        CASE 
            WHEN t.date IS NOT NULL THEN t.date
            WHEN t.completion_date IS NOT NULL THEN DATE_SUB(t.completion_date, INTERVAL (SELECT average_days_difference FROM avg_difference) DAY)
            ELSE NULL
        END AS Date_Upgraded,
        ROW_NUMBER() OVER (PARTITION BY t.ct_id ORDER BY t.ct_id) AS rn
    FROM transaction t
    LEFT JOIN acquiring_company ac ON t.ac_id = ac.ac_id
    LEFT JOIN ac_locations acl ON ac.ac_id = acl.ac_id
    LEFT JOIN location al ON acl.location_id = al.location_id
    LEFT JOIN merging_company mc ON t.mc_id = mc.mc_id
    LEFT JOIN mc_locations mcl2 ON mc.mc_id = mcl2.mc_id
    LEFT JOIN location ml ON mcl2.location_id = ml.location_id
)
SELECT
    Ct_Id,
    Date,
    Completion_Date,
    Difference_in_Days,
    Date_Upgraded,
    Type,
    AC_name,
    AC_company_form,
    AC_location,
    MC_name,
    MC_company_form,
    MC_location
FROM unique_transactions
WHERE rn = 1
ORDER BY Type, AC_location, MC_location;
