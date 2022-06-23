import requests
from bs4 import BeautifulSoup
from plyer import notification
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from loggingModule import makeLog

class RealTimeCovid:
    def __init__(self):
        self._log = makeLog()
    def _makeRequest(self,url):
        try:
            response = requests.get(url,verify=False)
            return response.text
        except Exception as e:
            self._log.error(e)
    def getCovidStats(self):
        try:
          html_data = self._makeRequest('https://www.worldometers.info/coronavirus/')
          # print(html_data)
          soup = BeautifulSoup(html_data, 'html.parser')
          total_global_row = soup.find_all('tr', {'class': 'total_row'})[-1]
          total_cases = total_global_row.find_all('td')[2].get_text()
          new_cases = total_global_row.find_all('td')[3].get_text()
          total_recovered = total_global_row.find_all('td')[6].get_text()
          print('total cases : ', total_cases)
          print('new cases :', new_cases[1:])
          print('total recovered : ', total_recovered)
          notification_message = f" Total cases : {total_cases}\n New cases : {new_cases[1:]}\n Total Recovered : {total_recovered}\n"
          notification.notify(
            title="COVID-19 Statistics",
            message=notification_message,
            timeout=5,
            toast = True
          )
          print("here are the stats for COVID-19")
        except requests.exceptions.SSLError as request_error:
            self._log.error(request_error)
            print('sir i am getting HTTPS Connection Pool request error please use google search function ')