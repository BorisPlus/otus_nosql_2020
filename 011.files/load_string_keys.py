import redis
import time

if __name__ == '__main__':

    r = redis.StrictRedis(host='localhost', port=6379, db=4)

    print('Load strings keys.')
    count = len(lexems)
    start = time.time()
    for key in r.keys('data:*'):
        print(key)

    end = time.time()
    print('\t', 'Were load:',  count, 'units')
    print('\t', 'Time left:',  end-start, 'ms')
