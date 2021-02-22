import json
import facebook

# importしたときに内容が表示されない

def main():
	token = "EAAFZB2RecYncBAH6ysfvP6QBHCDwh3rPA17qt9ZAeG9wa6f1DK58n3LjG0ab7mV80lMRJnVQqmZCA6A42GAOLSfhQK7zP6c782eROceJvv9g0ozZB5lrLeySb70zh24lfBgW9KmSAGkdLFI4e1ivZAhxZCVwYI674g7dnpbhCIKiisVWIMYwaoinDcoAUo2tgZD"
	graph = facebook.GraphAPI(token)
	#fields = ['first_name', 'location{location}','email','link']
	profile = graph.get_object('me',fields='first_name, last_name, location,link,email')
	#return desired fields
	print(json.dumps(profile, indent=4))

if __name__ == '__main__':
	main()
