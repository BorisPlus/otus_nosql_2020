import json
import redis
import time

if __name__ == '__main__':

    r = redis.StrictRedis(host='localhost', port=6379, db=4)

    print('Load json as complex structure.')
    print('\t', 'hset - https://redis.io/commands/hset')
    # TODO: https://pythontic.com/database/redis/sorted%20set%20-%20add%20and%20remove%20elements
    print('\t', 'zadd - https://redis.io/commands/zadd')
    print('\t', 'list - https://redis.io/commands/lpush')

    # JSON-ключи, которые будут списками, остальные будут hset
    # тут разделитель ;
    keys_for_list = 'ReverseRouteTrack', \
                    'DirectRouteTrack', \
                    'ReverseRouteTrack_en', \
                    'DirectRouteTrack_en'
    # тут разделитель -
    keys_for_list_2 = 'TrackOfFollowing', \
                      'ReverseTrackOfFollowing', \
                      'TrackOfFollowing_en', \
                      'ReverseTrackOfFollowing_en'

    with open('data.json', encoding='cp1251') as input_file:
        test_data = json.load(input_file)
        count = len(test_data)
        start = time.time()

        for data in test_data:
            for key, value in data.items():
                if key in keys_for_list:
                    continue
                # Внимание: тут тратится время на lower
                r.hset('object:%s' % data.get("system_object_id"), key.lower(), value)

            if key in keys_for_list:
                # Внимание: тут тратится время на преобразование строки 'x1,y1; x2,y2'
                # в список ['x1,y1', 'x2,y2'] и на strip
                for item in data.get('value').split(';'):
                    # Внимание: тут тратится время на lower
                    r.lpush('object:%s:%s' % (data.get("system_object_id"), key.lower()), item.strip())
            if key in keys_for_list_2:
                # Внимание: тут тратится время на преобразование строки 'x1 - x2 - x3'
                # в список ['x1', 'x2', 'x3'] и на strip
                for item in data.get('value').split(' - '):
                    # Внимание: тут тратится время на lower
                    r.lpush('object:%s:%s' % (data.get("system_object_id"), key.lower()), item.strip())

            # для zset путь будет упорядоченное по алфавиту по первым бувам (НЕ лексикографическое) название улиц маршрута
            # r.zadd('route', {key: score}, xx=False)

            zset_keys = ('TrackOfFollowing', )
            if key in zset_keys:
                for item in data.get('value').split(' - '):
                    # Внимание: тут тратится время на upper и ord(value[0])
                    value = key.upper()
                    r.zadd('object:%s' % data.get("system_object_id"), {value: ord(value[0])})

        end = time.time()
        print('\t', 'Were load:', count, 'units')
        print('\t', 'Time left:', end - start, 'ms')

        #
        # with open('data.json', encoding='cp1251') as input_file:
        #     test_data = json.load(input_file)
        #     start = time.time()
        #     for data in test_data:
        #         id = data.get("ID")
        #
        #         key = data.get("system_object_id")
        #         score = data.get("system_object_id")
        #         try:
        #             r.zadd('route', {key: score}, xx=False)
        #         except redis.exceptions.ResponseError as e:
        #             # print(data.get("ID"))
        #             # print(data.get("RouteNumber"))
        #             pass
        #
        #     end = time.time()
        #     print('ZADD:', end - start, 'ms')
        #
        # with open('data.json', encoding='cp1251') as input_file:
        #     test_data = json.load(input_file)
        #     start = time.time()
        #     for data in test_data:
        #         # print(data.get("RouteNumber"))
        #         try:
        #             # r.lpush('route', data.get("RouteNumber"))
        #             r.rpush('RouteNumber', data.get("RouteNumber"), 0)
        #         except redis.exceptions.ResponseError as e:
        #             print('ResponseError ' + data.get("RouteNumber"))
        #
        #     end = time.time()
        #     print('LPUSH:', end - start, 'ms')
