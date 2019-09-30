SELECT ct_id
,date
,ac_location as se_location
,employee_number
,year_employee
,company_form as company_form
,sector
,multi_cbm as multi_se
FROM cross_border_transactions.cb_table
WHERE type = "SE-SCE"