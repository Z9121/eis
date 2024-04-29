from tasks import parse_html

if __name__ == '__main__':
    urls = [
        'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?fz44=on&pageNumber=1',
        'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?fz44=on&pageNumber=2'
    ]
    for url in urls:
        parse_html.delay(url)
