import requests


def request(password):
    url = 'https://{host}:8443/?database={db}&query={query}'.format(
        host='rc1a-ajeh3q1t4jvrp4ri.mdb.yandexcloud.net',
        db='development',
        query='SELECT now()')
    auth = {
        'X-ClickHouse-User': 'otus',
        'X-ClickHouse-Key': password,
    }

    res = requests.get(
        url,
        headers=auth,
        verify='/usr/local/share/ca-certificates/Yandex/YandexInternalRootCA.crt')
    res.raise_for_status()
    return res.text


if __name__ == '__main__':
    password = input('Enter password: ')
    print(request(password))
