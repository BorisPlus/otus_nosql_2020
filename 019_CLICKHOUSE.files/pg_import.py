import psycopg2


def import_data(password):

    # VDS
    # conn = psycopg2.connect(
    #     host="192.168.102.99",
    #     database="development",
    #     user="root",
    #     password=password,
    #     port=15434)

    conn = psycopg2.connect("""
        host=rc1c-p8y8xsux30mu6sb9.mdb.yandexcloud.net
        port=6432
        dbname=db1
        user=user1
        password=%s
        target_session_attrs=read-write
    """ % password)

    with  conn.cursor() as cur:
        cur.execute("""
            DROP TABLE development.visits CASCADE;

            CREATE TABLE development.visits (
               counter_id bigint GENERATED BY DEFAULT AS IDENTITY,
               start_date date NOT NULL,
               sign integer, 
               isnew integer, 
               visit_id decimal, 
               user_id decimal, 
               start_time time, 
               duration integer
             ) PARTITION BY LIST (start_date);
             
            CREATE TABLE visits_2014_03_17 PARTITION 
            of development.visits FOR VALUES 
                IN ('2014-03-17');
                
            CREATE TABLE visits_2014_03_18 PARTITION 
            of development.visits FOR VALUES 
                IN ('2014-03-18');
            
            CREATE TABLE visits_2014_03_19 PARTITION 
            of development.visits FOR VALUES 
                IN ('2014-03-19');
            
            CREATE TABLE visits_2014_03_20 PARTITION 
            of development.visits FOR VALUES 
                IN ('2014-03-20');
            
            CREATE TABLE visits_2014_03_21 PARTITION 
            of development.visits FOR VALUES 
                IN ('2014-03-21');
            
            CREATE TABLE visits_2014_03_22 PARTITION 
            of development.visits FOR VALUES 
                IN ('2014-03-22');
            
            CREATE TABLE visits_2014_03_23 PARTITION 
            of development.visits FOR VALUES 
                IN ('2014-03-23');
                
        """)

    conn.commit()
    conn.autocommit = False

    with  conn.cursor() as cur:
        with open('visits_v1.tsv', 'r', encoding='iso-8859-1') as file_in:
            row_id = 0
            for row_id, row in enumerate(file_in):
                row_data = row.split('\t')
                cur.execute("""
                    INSERT INTO development.visits (
                        start_date,
                        sign,
                        isnew,
                        visit_id,
                        user_id,
                        start_time,
                        duration
                    ) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    row_data[1],
                    row_data[2],
                    row_data[3],
                    row_data[4],
                    row_data[5],
                    row_data[6],
                    row_data[7]
                ))

                if row_id % 1000 == 0:
                    print(row_id + 1)
                    conn.commit()
            print(row_id + 1)
        conn.commit()
    conn.close()


if __name__ == '__main__':
    password = input('Enter password: ')
    print(import_data(password))
