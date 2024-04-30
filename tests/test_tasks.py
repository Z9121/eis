from unittest.mock import patch
from parser.tasks import parse_html, parse_xml
import pytest
import requests
from bs4 import BeautifulSoup
from pytest import raises
from celery.exceptions import Retry
from io import StringIO
from user_agent import generate_user_agent
from urllib.parse import urljoin


url = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?fz44=on&pageNumber=1'


@pytest.mark.celery(task_always_eager=True)
class TestParseHtml:
    
    @patch('parser.tasks.parse_xml')
    def test_success(self, parse_xml_mock):
        parse_html(url)
        parse_xml_mock.delay.assert_called()

    @patch('requests.get')
    def test_failure(self, get):
        get.side_effect = Retry()
        with raises(Retry):
            parse_html(url)

@pytest.mark.celery(task_always_eager=True)
class TestParseXml:
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_success(self, mock_stdout):
        headers = {
            'User-Agent': generate_user_agent()
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        atags = soup.select('.w-space-nowrap a[target]')
        links = [urljoin('https://zakupki.gov.ru',
                        tag.get('href').replace('view.html', 'viewXml.html'))
                for tag in atags]

        response = requests.get(links[0], headers=headers)
        soup = BeautifulSoup(response.text, 'xml')
        out = '{}: {}\n'.format(links[0], soup.publishDTInEIS.string)

        parse_xml(links[0])
        assert mock_stdout.getvalue() == out

    
    @patch('requests.get')
    def test_failure(self, get):
        get.side_effect = Retry()
        with raises(Retry):
            parse_xml(url)




