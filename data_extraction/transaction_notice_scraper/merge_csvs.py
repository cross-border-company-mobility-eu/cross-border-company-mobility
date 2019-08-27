import os
import glob
import csv

os.chdir("notices")

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

header = []

with open("output.csv", "w", newline='') as f:
	writer = csv.writer(f)
	data = []
	for item in all_filenames:
		thisfiledata = []
		with open(item, "r") as inputfile:
			reader = csv.reader(inputfile, delimiter=',')
			for row in reader:
				thisfiledata.append(row)
		header = thisfiledata.pop(0)
		data.extend(thisfiledata)

	data.insert(0,header)
	writer.writerows(data)	

# #combine all files in the list
# combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
# #export to csv
# combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')