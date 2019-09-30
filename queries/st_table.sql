SELECT ct_id
,date
,ac_location as exit_country
,employee_number
,year_employee
,company_form as exit_company_form
,sector
,mc_location as entry_country
,mcompany_form as entry_company_form
FROM cross_border_transactions.cb_table
WHERE type = "CBC"