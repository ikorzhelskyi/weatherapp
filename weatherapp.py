#!/usr/bin/python3

"""Weather app project.
"""

import html
from urllib.request import urlopen, Request

ACCU_URL = "https://www.accuweather.com/uk/ua/lviv/324561/weather-forecast/324561"

# getting page from server
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64;)'}
accu_request = Request(ACCU_URL, headers=headers)
accu_page = urlopen(accu_request).read()
accu_page = accu_page.decode('utf-8')

ACCU_TEMP_TAG = '<span class="large-temp">'
accu_temp_tag_size = len(ACCU_TEMP_TAG)
accu_temp_tag_index = accu_page.find(ACCU_TEMP_TAG)
accu_temp_value_start = accu_temp_tag_index + accu_temp_tag_size
accu_temp = ''
for char in accu_page[accu_temp_value_start:]:
	if char != '<':
		accu_temp += char
	else:
	    break

ACCU_COND_TAG = '<span class="cond">'
accu_cond_tag_size = len(ACCU_COND_TAG)
accu_cond_tag_index = accu_page.find(ACCU_COND_TAG)
accu_cond_value_start = accu_cond_tag_index + accu_cond_tag_size
accu_cond = ''
for char in accu_page[accu_cond_value_start:]:
	if char != '<':
		accu_cond += char
	else:
	    break

print('AccuWeather: \n')
print(f'Temperature: {html.unescape(accu_temp)}\n')
print(f'Condition: {accu_cond}')

RP5_URL = ('http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D1%83_'
	       '%D0%9B%D1%8C%D0%B2%D0%BE%D0%B2%D1%96,_%D0%9B%D1%8C%D0%B2%D1'
	       '%96%D0%B2%D1%81%D1%8C%D0%BA%D0%B0_%D0%BE%D0%B1%D0%BB%D0%B0%D1'
	       '%81%D1%82%D1%8C')

rp5_request = Request(RP5_URL, headers=headers)
rp5_page = urlopen(rp5_request).read()
rp5_content = rp5_page.decode('utf-8')

WINFO_CONTAINER_TAG = '<div id="ArchTemp">'
RP5_TEMP_TAG = '<span class="t_0" style="display: block;">'
rp5_temp_tag = rp5_content.find(RP5_TEMP_TAG, 
	                            rp5_content.find(WINFO_CONTAINER_TAG))
rp5_temp_tag_size = len(RP5_TEMP_TAG)
rp5_temp_tag_start = rp5_temp_tag + rp5_temp_tag_size
rp5_temp = ""
for char in rp5_content[rp5_temp_tag_start:]:
	if char != '<':
		rp5_temp += char
	else:
	    break

RP5_COND_TAG = '<div class="cn5" onmouseover="tooltip(this, \'<b>'
rp5_cond_tag = rp5_content.find(RP5_COND_TAG)
rp5_cond_tag_size = len(RP5_COND_TAG)
rp5_cond_tag_start = rp5_cond_tag + rp5_cond_tag_size
rp5_cond = ""
for char in rp5_content[rp5_cond_tag_start:]:
	if char != '<':
		rp5_cond += char
	else:
	    break

print('RP5.ua: \n')
print(f'Temperature: {html.unescape(rp5_temp)}\n')
print(f'Condition: {html.unescape(rp5_cond)}')

SIN_URL = ('https://ua.sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE'
	       '%D0%B4%D0%B0-%D0%BB%D1%8C%D0%B2%D1%96%D0%B2')

sin_request = Request(SIN_URL, headers=headers)
sin_page = urlopen(sin_request).read()
sin_content = sin_page.decode('utf-8')

SIN_TEMP_TAG = '<p class="today-temp">'
sin_temp_tag = sin_content.find(SIN_TEMP_TAG)
sin_temp_tag_size = len(SIN_TEMP_TAG)
sin_temp_tag_start = sin_temp_tag + sin_temp_tag_size
sin_temp = ""
for char in sin_content[sin_temp_tag_start:]:
	if char != '<':
		sin_temp += char
	else:
	    break

SIN_COND_TAG = '<div class="description"> <!--noindex-->'
sin_cond_tag = sin_content.find(SIN_COND_TAG)
sin_cond_tag_size = len(SIN_COND_TAG)
sin_cond_tag_start = sin_cond_tag + sin_cond_tag_size
sin_cond = ""
for char in sin_content[sin_cond_tag_start:]:
	if char != '<':
		sin_cond += char
	else:
	    break

print('sinoptik.ua: \n')
print(f'Temperature: {html.unescape(sin_temp)}\n')
print(f'Condition: {html.unescape(sin_cond)}')

def get_request_headers():
    return {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64;)'}

def get_page_source(url):
    """Returns the content of the page by the given URL address.
    """

    request = Request(url, headers=get_request_headers())
    page_source = urlopen(request).read()
    return page_source.decode('utf-8')

def get_tag_content(page_content, tag):
    """Finds the necessary data in the content of the page.
    """

    tag_index = page_content.find(tag)
    tag_size = len(tag)
    value_start = tag_index + tag_size

    content = ''
    for c in page_content[value_start:]:
        if c != '<':
            content += c
        else:
            break
    return content

def get_weather_info(page_content, tags):
    """Returns information collected from tags.
    """

    return tuple([get_tag_content(page_content, tag) for tag in tags])


def main():
    """Main entry point.
    """

    weather_sites = {"AccuWeather": (ACCU_URL, ACCU_TAGS),
                     "RP5": (RP5_URL, RP5_TAGS),
                     "SINOPTIK": (SIN_URL, SIN_TAGS)}
    for name in weather_sites:
        url, tags = weather_sites[name]
        content = get_page_source(url)
        temp, condition = get_weather_info(content, tags)
        produce_output(name, temp, condition)

if __name__ == '__main__':
    main()