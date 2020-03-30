from threading import Timer
import time
import requests
from bs4 import BeautifulSoup
data = []
dct = {}
def extractLatestData():
    page = requests.get('http://covid.gov.pk/')
    soup = BeautifulSoup(page.text, 'html.parser')
    dct['name'] = 'Pakistan'
    dct['confirmed'] = soup.find(class_='text-muted numbers-main').text
    overall_stats = soup.find(class_='text-center')
    recovered = 0
    critical = 0
    deaths = 0
    for main in overall_stats:
        if (main.name == 'div'):
            for inside in main:
                if (inside.name == 'div'):
                    for data in inside:
                        if (data.name == 'h6'):
                            title = data.text
                        if (data.name == 'h4'):
                            if title.lower() == 'recovered':
                                dct['recovered'] = data.text
                            elif title.lower() == 'critical':
                                dct['serious'] = data.text
                            elif title.lower() == 'deaths':
                                dct['deaths'] = data.text
                            elif title.lower() == 'Cases (24 HRS)':
                                dct['cases_today'] = data.text
                            elif title.lower() == 'Deaths (24 HRS)':
                                dct['deaths_today'] = data.text

    provincial_stats = soup.find(class_='provinc-stat') 
    dct['cities'] = {}
    for main in provincial_stats:
        if (main.name == 'div'):
            for data in main:
                if (data.name == 'h6'):
                    title = data.text
                if (data.name == 'h4'):
                    dct['cities']['%s'%title] = data.text
                    
extractLatestData()
data.append(dct)
print(data)