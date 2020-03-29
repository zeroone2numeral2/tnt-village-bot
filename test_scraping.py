from pprint import pprint
import unicodedata

import requests
from bs4 import BeautifulSoup


def get_html(read_local_file=True):
    if not read_local_file:
        print('REQUEST')
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        result = requests.post(
            "http://tntvillage.scambioetico.org/?releaselist",
            data={"cat": "0", "page": str(0), "srcrel": ""},
            headers={'User-Agent': user_agent}
        )

        html_text = result.text
        # print(html_text)
        with open('result.html', 'w+') as f:
            f.write(html_text)
    else:
        print('FILE')
        with open('result.html', 'r', encoding='utf-8') as f:
            html_text = f.read()

    return html_text


def table_to_list(soup):
    result_rows = list()

    table_rows = soup.find_all('tr')
    for i, row in enumerate(table_rows):
        if i == 0:
            print('skipping table header...')
            continue

        row_data = dict()

        row_columns = row.find_all('td')
        for column in row_columns:
            if column.find('a'):
                for a in column.find_all('a', href=True):
                    if a['href'].startswith('magnet:?'):
                        row_data['magnet'] = a['href']
                    elif a['href'].startswith('http://forum.tntvillage.scambioetico.org/index.php?showtopic='):
                        row_data['title'] = a.text
                    elif 'act=Attach' in a['href']:
                        row_data['torrent_url'] = a['href']
                if column.text:
                    desc = column.text
                    row_data['desc'] = unicodedata.normalize("NFKD", desc)  # https://stackoverflow.com/a/34669482

        result_rows.append(row_data)

    return result_rows


def main():
    html_text = get_html()

    soup = BeautifulSoup(html_text, features='html.parser')
    # print(soup.prettify())
    rows_list = table_to_list(soup)

    pprint(rows_list)


main()

