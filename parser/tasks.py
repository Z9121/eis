import requests
from user_agent import generate_user_agent
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from requests.exceptions import HTTPError, RequestException
from celery import Celery
import celery


app = Celery('tasks', broker='pyamqp://guest@localhost//')


class ParseHtml(celery.Task):

    name = 'parse-html'

    def run(self, url):
        """Get html page and run xml parsing"""
        headers = {
            'User-Agent': generate_user_agent()
        }
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            atags = soup.select('.w-space-nowrap a[target]')
            links = [urljoin('https://zakupki.gov.ru',
                             tag.get('href').replace('view.html', 'viewXml.html'))
                     for tag in atags]
        except Exception as exc:
            raise self.retry(exc=exc)
        for link in links:
            parse_xml.delay(link)


class ParseXml(celery.Task):

    name = 'parse-xml'

    def run(self, url):
        """Get xml page then parse and print result"""
        headers = {
            'User-Agent': generate_user_agent()
        }
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'xml')
        except Exception as exc:
            raise self.retry(exc=exc)
        print('{}: {}'.format(url, soup.publishDTInEIS.string))


parse_html = app.register_task(ParseHtml())
parse_xml = app.register_task(ParseXml())
