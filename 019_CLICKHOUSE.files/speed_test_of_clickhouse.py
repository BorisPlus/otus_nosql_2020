import requests
import time


def request(password):
    queries = [
        'SELECT COUNT(*) FROM development.visits_v1',
        '''
        SELECT StartDate, COUNT(CounterID) 
        FROM development.visits_v1
        GROUP BY (StartDate);
        ''',
        '''
        SELECT StartDate, COUNT(CounterID)
        FROM development.visits_v1
        WHERE  StartDate < toDate('2014-03-20')
        GROUP BY(StartDate);
        ''',
    ]
    auth = {
        'X-ClickHouse-User': 'otus',
        'X-ClickHouse-Key': password,
    }
    for query in queries:
        url = 'https://{host}:8443/?database={db}&query={query}'.format(
            host='rc1a-ajeh3q1t4jvrp4ri.mdb.yandexcloud.net',
            db='development',
            query=query
        )
        start_time = time.time()
        res = requests.get(
            url,
            headers=auth,
            verify='/usr/local/share/ca-certificates/Yandex/YandexInternalRootCA.crt')
        res.raise_for_status()
        end_time = time.time()
        print(end_time - start_time, 's')
        print(res.text)
    return 'Done'


if __name__ == '__main__':
    password = input('Enter password: ')
    print(request(password))
