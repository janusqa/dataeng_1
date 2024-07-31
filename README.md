### dbt
- $pip install dbt-postgres
  - this installs dbt-core and dbt-postgres only
- $ pip install --upgrade dbt-<adapter> # optional
  - eg. $ pip install --upgrade dbt-postgres
- $ dbt init # answer the questions
  - Enter project name: eg. custom_postgres
  - select from list of dbs which db we want to use. We choose postgres since we installed that adapter
  - Done. A folder custom_postgres should have been created.
  - in ~/.dbt create a profiles.yaml file
    - see example there 
    ```
        custom_postgres:
        outputs:
            dev:
            dbname: destination_db
            host: destination_db
            pass: postgres
            port: 5432
            schema: public
            threads: 1
            type: postgres
            user: postgres
        target: dev
    ```
- set up a folder in custom_postgres/models to hold your models
- set up your base querys actors, film_actors, films to their backing tables in destination_db
- create a schema.yml to describe what your tables will look like.  This is for validation purposes. This contains both your source tables and your tables that will be based on these base/source tables
- create a sources.yml to describe your db source and what your base tables are

### dbt macros
- macros can be use to automate repetitive task
  - eg say we want to generate the film_ratings over and over again to be used somewhere else
  - we can set up our sql for film_ratings in a macro (we resuded our model code). See "macros/film_ratings_macro.sql"
  - now go back to "models/film_ratings.sql" and use your macro



### postgres fu
- docker exec -it <destination_db_docker_id> psql - U postgres # connect to running docker container
  - \c destination_db  # connect to db
    - \dt  # list tables 
    - SELECT * FROM film_ratings;