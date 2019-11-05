class StaticFields:
	# Dictionary of EU country names and their codes
	euMemberStates = {
		'AL':['Albania'],
		'AD':['Andorra'],
		'AT':['Austria'],
		'AZ':['Azerbaijan'],
		'BY':['Belarus'],
		'BE':['Belgium'],
		'BA':['Bosnia and Herzegovina','Bosnia'],
		'BG':['Bulgaria'],
		'HR':['Croatia'],
		'CY':['Cyprus'],
		'CZ':['Czech Republic','Czech'],
		'DK':['Denmark'],
		'EE':['Estonia'],
		'FI':['Finland'],
		'FR':['France'],
		'GE':['Georgia'],
		'DE':['Germany'],
		'GR':['Greece'],
		'HU':['Hungary'],
		'IS':['Iceland'],
		'IE':['Ireland'],
		'IT':['Italy'],
		'KZ':['Kazakhstan'],
		'XK':['Kosovo'],
		'LV':['Latvia'],
		'LI':['Liechtenstein'],
		'LT':['Lithuania'],
		'LU':['Luxembourg'],
		'MK':['Macedonia'],
		'MT':['Malta'],
		'MD':['Moldova'],
		'MC':['Monaco','Monte Carlo'],
		'ME':['Montenegro'],
		'NL':['Netherlands','The Netherlands','Holland'],
		'NO':['Norway'],
		'PL':['Poland'],
		'PT':['Portugal'],
		'RO':['Romania'],
		'RU':['Russia'],
		'SM':['San Marino'],
		'RS':['Serbia'],
		'SK':['Slovakia'],
		'SI':['Slovenia'],
		'ES':['Spain'],
		'SE':['Sweden'],
		'CH':['Switzerland'],
		'TR':['Turkey'],
		'UA':['Ukraine'],
		'VA':['Vatican City'],
		'UK':['United Kingdom','Great Britain','England']
	}

	# List of keys in the euMemberStates dictionary
	euMemberStateCodes = ['AL', 'AD', 'AT', 'AZ', 'BY', 'BE', 'BA', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 'GE', 'DE', 'GR', 'HU', 'IS', 'IE', 'IT', 'KZ', 'XK', 'LV', 'LI', 'LT', 'LU', 'MK', 'MT', 'MD', 'MC', 'ME', 'NL', 'NO', 'PL', 'PT', 'RO', 'RU', 'SM', 'RS', 'SK', 'SI', 'ES', 'SE', 'CH', 'TR', 'UA', 'GB', 'VA', 'UK']
	# List of values in the euMemberStates dictionary
	euMemberStateNames = ['Albania', 'Andorra', 'Austria', 'Azerbaijan', 'Belarus', 'Belgium', 'Bosnia and Herzegovina', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Estonia', 'England', 'Finland', 'France', 'Georgia', 'Germany', 'Greece', 'Great Britain', 'Hungary', 'Iceland', 'Ireland', 'Italy', 'Kazakhstan', 'Kosovo', 'Latvia', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macedonia', 'Malta', 'Moldova', 'Monaco', 'Montenegro', 'Netherlands', 'Norway', 'Poland', 'Portugal', 'Romania', 'Russia', 'San Marino', 'Serbia', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Turkey', 'Ukraine', 'Vatican City', 'United Kingdom']

	# Cross-border (CBM) merger keywords
	cbm_kw_1 = ['verschmelzung', 'grenzüberschreitende']

	cbm_kw_2 = ['verschmelzung', '§ 122d']
	cbm_kw_3 = ['verschmelzung', '§ 122a']
	cbm_kw_4 = ['verschmelzung', '§ 122j']

	cbm_kw_5 = ['übernehmen', 'übertragen']
	cbm_kw_6 = ['aufnehmen', 'übertragen']
	cbm_kw_7 = ['verschmelzung', 'übertragen']
	cbm_kw_8 = ['verschmelzung', 'übernehmen']
	cbm_kw_9 = ['verschmelzung', 'aufnehmen']
	cbm_kw_NOT = ['formwechsel']

	cbm_kw_10 = ['verschmelzung', 'grenzuberschreiten']
	cbm_kw_11 = ['ubernehmen', 'ubertragen']
	cbm_kw_12 = ['aufnehmen', 'ubertragen']
	cbm_kw_13 = ['verschmelzung', 'ubertragen']
	cbm_kw_14 = ['verschmelzung', 'ubernehmen']

	cbm_kw_15 = ['verschmelzung', ' 122d ']
	cbm_kw_16 = ['verschmelzung', ' 122a ']
	cbm_kw_17 = ['verschmelzung', ' 122d)']
	cbm_kw_18 = ['verschmelzung', ' 122a)']
	cbm_kw_19 = ['verschmelzung', ' 122j ']
	cbm_kw_20 = ['verschmelzung', ' 122j)']
	cbm_kw_21 = ['verschmelzung', ' 122 a ']
	cbm_kw_22 = ['verschmelzung', ' 122 d ']
	cbm_kw_23 = ['verschmelzung', ' 122 j ']

	# Seat transfer (ST) keywords
	st_kw_1 = ['formwechsel', 'grenzüberschreiten']
	st_kw_2 = ['verschmelzung', 'formwechsel']
	st_kw_3 = ['sitzver']
	st_kw_4 = ['neuer sitz']
	st_kw_5 = ['formwechsel', 'grenzuberschreiten']
	st_kw_NOT = ['§ 122a','§ 122j']
	st_kw_NOT2 = ['122a','122j']

	# Societas Europaea (SE) keywords
	se_kw_1 = [' se ','formwechsel']
	se_kw_2 = ['(se)','formwechsel']
	se_kw_3 = [' (se) ','formwechsel']
	se_kw_4 = ['se-vo']


# Test if fields print correctly
#print(StaticFields.euMemberStateCodes)
#print(StaticFields.euMemberStateNames)