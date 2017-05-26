def cartridge(tmp):

	header = ['datetime','lat','lng','light','temperature','humidity','rain']
	measure = ['light','temperature','humidity','rain']
	for var in header:
		for line in measure:
			if(line == var):
				for line in tmp:
					vect_tmp = line.split(",")
					nr_measure = nr_measure + float(vect_tmp[contador])
					
		contador = contador + 1			
			
	
