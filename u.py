""" Python v.3.8.7  FastAPI  Postgresql v.13  os Pydantic async/await asyncpg  uuid  js18.user """
import os
import uvicorn
import uuid
from loguru import logger as logging
import time

from functools import wraps
from enum import Enum
from email_validator import validate_email, EmailNotValidError
from fastapi import FastAPI, Depends, Response, Query
from fastapi_asyncpg import configure_asyncpg
from pydantic import BaseModel, EmailStr, UUID5, Field


class Table(str, Enum, ):
    name = "count"


class Count(BaseModel,
            title="This is a model for searching records in the database and for working with api GET",
            ):
    email: EmailStr = Field(
        description="the value must semantically match the email address",
        examples=["js18.user@gmail.com"],
        strict=True,
    )
    uuid: UUID5 = Field(
        description="the value must semantically match the format uuid",
        examples=["5f6daefb-1373-5095-8e4f-1ffbf4965cd3"],
        strict=True,
    )


class CountGet(BaseModel,
               title="This is a model for saving records in a database and for working with api POST",
               ):
    id: int = Field(
        default=None,
        ge=0,
        description="The id must be greater than zero",
        strict=True,
    )
    email: EmailStr = Field(
        default=None,
        description="the value must semantically match the email address",
        strict=True,
    )
    uuid: UUID5 = Field(
        default=None,
        description="the value must semantically match the format uuid",
        strict=True,
    )


async def validator_email(email):
    """ For next scripts """
    try:
        validate_email(email)
    except EmailNotValidError:
        return False
    return True


def lead_time(func_async):
    @wraps(func_async)
    async def wrapper(*args, **kwargs):
        start_time, result = time.time(), await func_async(*args, **kwargs)
        logging.info(
            f"{skip}Function {func_async.__name__} "
            f"execution time: {int((time.time() - start_time)*1000)} m.sec{skip}"
        )
        return result
    return wrapper


try:

    async def db_connection():
        """  Reserved for future  """

        connect = configure_asyncpg(app, 'postgresql://{user}:{password}@{host}:{port}/{name}'.format(
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            host=os.environ['DB_HOST'],
            port=os.environ['DB_PORT'],
            name=os.environ['DB_NAME']))
        return connect


    async def query_select(table, model, fields="*"):
        if model.get('id') is None:
            where: str = " and ".join([f"%s = '%s'" % (item, model[item])
                                      for item in model.keys()
                                       if (model[item] is not None)
                                       ]
                                      )
            if where == "":
                return f"select {fields} from {table}  "
            else:
                return f"select {fields} from {table} where ({where}) ;"
        else:
            return f"select {fields} from {table}  where id = {model.get('id')};"


    async def query_insert(table, model, fields="*"):
        """ To create a new query for insert record into DB  """
        length_model: int = len(model.values())
        return "Insert Into {table} ({columns}) Values ({values}) On Conflict Do Nothing Returning {fields};".format(
            table=table,
            values=",".join([f"${p + 1}" for p in range(length_model)]),
            columns=",".join(list(model.keys())),
            fields=fields,
        )


    @lead_time
    async def insert(db, table, model, ):
        """ To create a new record into DB"""
        async with db.transaction():
            return await db.fetch(await query_insert(table, model), *list(model.values()), )


    @lead_time
    async def select(db, table, model, ):
        """ To select records into DB"""
        return await db.fetch(await query_select(table, model, ), )


    skip: str = '\n'
    app = FastAPI(title="API documentation",
                  description="A set of Api for completing the task is presented",
                  )

    conn = configure_asyncpg(app, 'postgresql://{user}:{password}@{host}:{port}/{name}'.format(
        user='postgres',
        name='fintech',
        password='aa4401',
        host='localhost',
        port=5432))


    @conn.on_init
    async def init(db_initial):
        with open('create.sql', 'r') as sql:
            await db_initial.execute(sql.read(), )


    @app.get("/count",  status_code=200, description="To select records from database", )
    async def get(response: Response,
                  db=Depends(conn.connection),
                  id: int | None = Query(default=None, ge=0, ),
                  email: EmailStr | None = Query(default=None, ),
                  uuid: UUID5 | None = Query(default=None, ),
                  ):
        match id:
            case None:
                pass
            case _:
                match isinstance(id, int):
                    case False:
                        response.status_code = 400
                        return {"message": "id argument is not valid"}
                    case True:
                        pass
        row = await select(db=db,
                           table=Table.name,
                           model=CountGet(id=id,
                                          email=email,
                                          uuid=uuid,
                                          ).dict()
                           )
        match len(row):
            case 0:
                response.status_code = 400
                return {"message": "No records with this attributes into database"}
            case _:
                return row


    @app.post("/count", status_code=200, description="To create a new record into database", )
    async def post(response: Response,
                   model: Count,
                   db=Depends(conn.atomic)):

        if model.uuid == uuid.uuid5(uuid.NAMESPACE_URL, model.email):
            pass
        else:
            response.status_code = 400
            return {"Message": "Only uuid.uuid5 is allowed"}
        row: dict = await insert(db, Table.name, model=model.dict(), )
        match len(row):
            case 0:
                return await select(db, Table.name, model=model.dict(), )
            case _:
                return row

except KeyboardInterrupt:
    pass
except (Exception, TypeError, ValueError) as error:
    logging.info(error)
finally:
    pass
if __name__ == "__main__":

    try:
        uvicorn.run('u:app', host='localhost', port=8000, reload=False, )
    except KeyboardInterrupt:
        exit()
