#!/usr/bin/env python3
import psycopg2

def main():
    pg_conn = psycopg2.connect(user="kafka_test", password="kafka_test", database="kafka_test", host="postgres", port=5433)
    cur = pg_conn.cursor()

    cur.close()
    pg_conn.close()

if __name__ == '__main__':
    main()
