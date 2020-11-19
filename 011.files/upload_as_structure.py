import json
import redis
import time

if __name__ == '__main__':

    DEBUG_UPLOAD_LIMIT = 250

    r = redis.StrictRedis(host='localhost', port=6379, db=4)

    print('Upload json as complex structure.')
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
        index = 0  # не надо эту строку в коде, это для интерпритатора PyCharm

        start = time.time()

        for index, data in enumerate(test_data):
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

            zset_keys = ('TrackOfFollowing',)
            if key in zset_keys:
                for item in data.get('value').split(' - '):
                    # Внимание: тут тратится время на upper и ord(value[0])
                    value = key.upper()
                    r.zadd('object:%s' % data.get("system_object_id"), {value: ord(value[0])})
            #
            r.save()

            if DEBUG_UPLOAD_LIMIT and index >= DEBUG_UPLOAD_LIMIT:
                break

        end = time.time()
        print('\t', 'Were upload:', index + 1, 'units')
        print('\t', 'Time left:', end - start, 'ms')
