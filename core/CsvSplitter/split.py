def split_csv(dirName):
	fil = 'output/'+dirName+'/members.csv'
	csvfilename = open(fil, 'r').readlines()
	#store header values
	header = csvfilename[0] 
	#remove header from list
	csvfilename.pop(0) 
	file = 1
	#Number of lines to be written in new file
	record_per_file = 50

	for j in range(len(csvfilename)):
		if j % record_per_file == 0:
			write_file = csvfilename[j:j+record_per_file]
	                #adding header at the start of the write_file
			write_file.insert(0, header)
	 	 	#write in file
			open(str(fil.replace('.csv',''))+ str(file) + '.csv', 'w+').writelines(write_file)
			file += 1
