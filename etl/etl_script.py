#!/usr/bin/env python3

import subprocess
import time

def wait_for_postgres(host, max_retries=5, delay_seconds=5):
    retries = 0
    while retries < max_retries:
        try:
            result = subprocess.run(["pg_isready", "-h", host], check=True, capture_output=True, text=True)
            if "accepting connections" in result.stdout:
                print (f"Successfully connected to Postgres Host {host}")
                return True
        except subprocess.CalledProcessError as e:
            print(f"Error connecting to postgres: {e}")
            retries+=1
            print(f"Retrying in {delay_seconds} seconds... (Attempt {retries}/{max_retries})")
            time.sleep(delay_seconds)
    print ("Max retries reached. Exiting...")
    return False

source_up = wait_for_postgres(host="source_db")
destination_up = wait_for_postgres(host="destination_db")

if not(source_up and destination_up):
    exit(1)

print ("Starting ETL Script...")

source_config ={
    "dbname": "source_db",
    "user": "postgres",
    "password": "postgres",
    "host": "source_db"
}

destination_config ={
    "dbname": "destination_db",
    "user": "postgres",
    "password": "postgres",
    "host": "destination_db"
}

dump_command = [
    'pg_dump',
    '-h', source_config['host'],
    '-U', source_config['user'],
    '-d', source_config['dbname'],
    '-f', 'data_dump.sql',
    '-w'
]

load_command = [
    'psql',
    '-h', destination_config['host'],
    '-U', destination_config['user'],
    '-d', destination_config['dbname'],
    '-f', 'data_dump.sql'
]

subprocess_source_env = dict(PGPASSWORD=source_config['password'])
subprocess.run(dump_command, env=subprocess_source_env, check = True)

subprocess_destination_env = dict(PGPASSWORD=destination_config['password'])
subprocess.run(load_command, env=subprocess_destination_env, check = True)

print ("Ending ETL Script...")
