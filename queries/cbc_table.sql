SELECT ct_id
,date
,ac_location as emerging_company_country
,employee_number
,year_employee
,company_form as emerging_company_form
,sector
,mc_location as original_company_country
,mcompany_form as original_company_form
,multi_cbm as multi_cbd
FROM cross_border_transactions.cb_table
WHERE type = "CBD"