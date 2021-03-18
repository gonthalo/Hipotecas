
import urllib3

def get_html(url):
	urllib3.disable_warnings()
	http_pool = urllib3.connection_from_url(url)
	r = http_pool.urlopen('GET',url)
	return r.data.decode('utf-8')

def get_house(link):
	raw = get_html(link)


if __name__ == '__main__':
	url = 'https://www.idealista.com/inmueble/91685658/'
	print (get_html(url))

