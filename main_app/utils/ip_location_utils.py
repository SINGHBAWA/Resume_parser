from django.contrib.gis import geoip2

"""Make sure that django has the correct IP even if there is a proxy/CDN"""


def get_ip_address():
    """Process a request"""
    import requests
    response = requests.request( "GET", "https://api.ipify.org/?format=json" )
    ip_address = response.json().get( "ip" )
    print("IP ADDRESS: {ip}".format(ip=ip_address))
    return ip_address


def get_city(ip_address):

    g = geoip2.GeoIP2()
    if ip_address:
        city_data = g.city(ip_address)
        city = city_data['city']
    else:
        city = 'Rome'  # default city
    return city


def get_location(ip_address):
    g = geoip2.GeoIP2()
    location = None
    if ip_address:
        location = g.coords(ip_address)
    return location