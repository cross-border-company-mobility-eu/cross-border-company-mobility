SELECT ct_id
,date
,type
,multi_cbm
,ac_location
,employee_number
,year_employee
,company_form
,sector
,mc_location
,memployee_number
,myear_employee
,mcompany_form
,msector
FROM cross_border_transactions.cb_table
#WHERE type = "CBM"