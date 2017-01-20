import argparse
import os.path
from urllib.request import urlopen

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--api', type=str, default='', 
		help='api key for Notify My Android.')
	parser.add_argument('--url', type=str, default='http://ip.42.pl/raw',
		help='URL to probe for IP address.')
	parser.add_argument('--source', type=str, default='My Server',
		help='Name of machine sending the notification.')
	parser.add_argument('--ipfile', type=str, default='/etc/my_ip/ip',
		help='Path to file for storing current IP address.')
	return parser.parse_args()
    
def write_ip_file(file_path, ip):
	f = open(file_path, 'w')
	f.write(ip)
	f.close()
 
def read_ip_file(file_path):
	if os.path.isfile(file_path):    
		f = open(file_path, 'r')
		ip = f.readline()
		f.close()
		return ip
	else:
		return 'no ip file found'
     
def main():
	args = parse_args()

	old_ip = read_ip_file(args.ipfile)
	new_ip = urlopen(args.url).read().decode('utf-8')
 
	if old_ip != new_ip:
		nma = 'https://www.notifymyandroid.com/publicapi/notify'
		apikey = args.api
		application = args.source
		event = 'Public IP Address Changed'
		description = 'New IP: {}'.format(new_ip)
		priority = 0
 
		nma_url = ("{}"
		"?apikey={}"
		"&application={}"
		"&event={}"
		"&description={}"
		"&priority={}").format(nma,
			apikey, 
			application,
			event,
			description,
			priority)
		nma_url = nma_url.replace(' ', '%20')
		urlopen(nma_url).read()
 
	write_ip_file(args.ipfile, new_ip)
    
main()
