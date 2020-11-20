import redis
import time
import pprint

if __name__ == '__main__':

    r = redis.StrictRedis(host='localhost', port=6379, db=2)

    print('Load keys.')

    print()
    for key in r.keys('*:104:*'):
        print(key)

    print('\t', 'sets keys:')
    for key in r.keys('*:104:*set'):
        print('\t', '\t', key)

    print('\t', 'hsets:')
    for key in r.keys('*:104:list__*'):
        print('\t', '\t', key)

    # for key in r.hgetall('object:hset'):
    #     print(key)
    # for key in r.hscan('object:hset', 0, match='*'):
    #     print(key)
    # for key in r.hscan('object:hset', 0, match='*3*'):
    #     print(key)
    # #
    # print('Match data by values.')
    # matches = '1', '*2', '*3*', 'data:365:*37*'
    # start = time.time()

    print('\t', 'hset keys:')
    for key in r.keys('*:104:hset'):
        unit = r.hscan(key, match='*')
        for h_key in unit[1]:
            print('\t', '\t', h_key)

    print()
    print('\t', 'hset keys values:')
    k_v = enumerate(r.keys('*:hset'))
    v_indx = 0
    start = time.time()
    for v_indx, v in k_v:
        units = r.hscan(v, match='*')
        # pprint.pprint(units[0])
        # for unit in units[1]:
        #     print('\t', '\t', unit, units[1].get(unit).decode('utf8'), )
    end = time.time()
    print()

    print('Time left for get all keys for ALL hset-substructures', end - start, 'sec')
    print('Units count:', v_indx+1)


    print()
    print('\t', 'list keys values:')
    k_v = enumerate(r.keys('*:list__*'))
    v_indx = 0
    start = time.time()
    for v_indx, v in k_v:
        units = r.lpop(v)
        # pprint.pprint(units[0])
        # for unit in units[1]:
        #     print('\t', '\t', unit, units[1].get(unit).decode('utf8'), )
    end = time.time()
    print()

    print('Time left for get all hset-substructures for ALL rows', end - start, 'sec')
    print('Units count:', v_indx+1)