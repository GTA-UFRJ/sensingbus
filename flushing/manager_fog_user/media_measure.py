def cartridge(tmp):
	temperature_list = []
	temperature = 0
	humidity_list = []
	humidity = 0
	light_list = []
	light = 0
	rain_list = []
	rain = 0
	i = 0
	for line in tmp:
		tmp_list = line.split(',')
		light_list.append(tmp_list[3])
		light = light + light_list[i]
		temperature_list.append(float(tmp_list[4]))
		temperature = temperature + temperature_list[i]
		humidity_list.append(tmp_list[5])
		humidity = humidity + humidity_list[i]
		rain_list.append(tmp_list[6])
		rain = rain + rain_list
		i = i + 1
	
	temperature_media = temperature / len(tmp)
	humidity_media = humidity / len(tmp)
	light_media = light / len(tmp)
	rain_media = rain / len(tmp)
	measure_media = [temperature_media, humidity_media, light_media, rain_media]
	return measure_media

