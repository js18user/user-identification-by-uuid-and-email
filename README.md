# user-identification-by-uuid-and-email
user identification by uuid and email

The software stack for implementing the task is as follows:
- Python 3.10.9 
- Fastapi
- Asyncio
- Async/await
- Pydantic
- Asyncpg
- SQL
- Postgresql 14.5  DBaaS  or Localhost
- Logging
- UUID
- Aiohttp

Statement of the problem (Technical specifications for programming)
- It is required to implement a REST API using the FastAPI framework running in asynchronous mode. 
- The API must contain a single endpoint that processes a POST request containing two parameters passed in the form: UUID (RFC 4122), email address.
- When processing a request, a data check must be carried out; if the parameters are valid, the data is added to the PostgreSQL database.
- The response to the request must be in JSON format containing the database entry ID, UUID and email address.
- Database access parameters and table name are configured in the .env file. 
- It is also necessary to implement a Python script that will allow you to perform load testing of a given endpoint while simultaneously generating N requests to the endpoint.

This program implements the maintenance of a database of simple counts:
- ID
- email
- uuid

Main functions:
- creating a count
- count search
 
User service is possible using:
- GET
- POST

List of programs:
- u.py  main program
- ut.py load testing program, the program specifies the following conditions:
  - number of simultaneously executed tasks,
  - number of POST transactions in each task,
  - email address prefix.
- create.sql  .SQL file for creating a table in the database.
- requirements.txt  no comment

Return codes:
- 200 - successful completion of the request
- 400 - there are errors in the request
- 422 - Pydantic validate response (very rare)

The present task is self-documented:
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc

http://127.0.0.1:8000/count   for work
