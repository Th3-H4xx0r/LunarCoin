from requests import get


ip = get('https://api.ipify.org')
print(f'My public IP address is: {ip.content}')

