""" Python v.3.8.7,  asyncio/await, AioHTTP , uuid.UUID ,  UUIDEncoder/json.JSONEncoder   by js18.user   """

import asyncio
import aiohttp
import time
import uuid
import datetime
import json
from uuid import UUID
from pydantic import BaseModel, EmailStr, UUID5, ValidationError


class Model(BaseModel):
    uuid: UUID5
    email: EmailStr


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return obj.hex
        return json.JSONEncoder.default(self, obj)


skip: str = '\n'


async def test(task_number, connection_number, mail_name, ):
    try:
        print(f'Start async task_number:({task_number}), {datetime.datetime.now()}')
        async with aiohttp.ClientSession(read_bufsize=2 ** 12, ) as session:
            for connect in range(connection_number):
                email: str = ''.join((mail_name, str(task_number), str(connect), '@test.com'), )
                async with session.post('http://127.0.0.1:8000/count',
                                        json=json.loads(json.dumps(
                                            Model(uuid=uuid.uuid5(uuid.NAMESPACE_URL, email),
                                                  email=email, ).dict(), cls=UUIDEncoder), )
                                        ) as response:
                    await response.json()
                    if response.status != 200:
                        print(f' error test, response.status is: {response.status}', skip,
                              f'email is: {email}',
                              )
                    print(f'Transaction: task {task_number}  '
                          f'connection {connect}  '
                          f'response.status is: {response.status}')  # You can #

        print(f'End   async task_number:({task_number}), {datetime.datetime.now()}')
    except (Exception, ValueError, TypeError, ValidationError, ) as error:
        print(f'Error connection: task {task_number} connection {connection_number}  ', skip,
              f'Error:{error}')
        pass
    except KeyboardInterrupt:
        pass
    finally:
        await session.close()
        pass

    return()


async def asynchronous(t_numbers, n_connections, mail_name, ):
    futures = [test(task_number, n_connections, mail_name, )
               for task_number in range(t_numbers)
               ]
    for i, future in enumerate(asyncio.as_completed(futures)):
        await future


async def main(t_numbers, n_connections, mail_name, ):
    try:
        print(skip,
              f'Number_of_tasks is: {t_numbers}', skip,
              f'Number_of_connections into task is:  {n_connections}', skip,
              f'Number_of_connections in test is:   {t_numbers * n_connections}', skip,
              )
        start_time = time.time()
        await asynchronous(t_numbers, n_connections, mail_name, )

        print(skip,
              f'The medium time of one  connection is: ',
              f'{round((time.time() - start_time) * 1000 / (t_numbers * n_connections))} ms',
              )

        print(skip,
              '************** Test end **************', skip
              )

    except (Exception, ValueError, TypeError, ValidationError, ) as error:
        print('error : ', error)
        pass
    except (KeyboardInterrupt, ):
        pass
    finally:
        pass
    return ()


if __name__ == "__main__":

    number_of_tasks = 10
    """ number of concurrent tasks """

    number_of_connections_in_task = 10000
    """ number of calls to api in one task """

    prefix_of_mail = 'test.092.11'
    """ initial characters in the email address name field """

    asyncio.run(main(number_of_tasks, number_of_connections_in_task, prefix_of_mail, ))
