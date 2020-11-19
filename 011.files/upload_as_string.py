import json
import redis
import time

if __name__ == '__main__':

    DEBUG_UPLOAD_LIMIT = 250

    r = redis.StrictRedis(host='localhost', port=6379, db=4)

    print('Upload json as true-string.')
    with open('data.json', encoding='cp1251') as input_file:
        test_data = json.load(input_file)
        count = len(test_data)
        start = time.time()
        index = 0  # не надо эту строку в коде, это для интерпритатора PyCharm
        for index, data in enumerate(test_data):
            r.set('data:%s' % index, str(data).lower())
            r.save()
            if DEBUG_UPLOAD_LIMIT and index >= DEBUG_UPLOAD_LIMIT:
                break
        end = time.time()
        print('\t', 'Were upload:', index + 1, 'units')
        print('\t', 'Time left:', end - start, 'ms')
