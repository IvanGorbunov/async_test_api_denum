import asyncio
import time
import aiohttp
from aiohttp.client import ClientSession

from conf import limit_of_connections, number_of_requests, token
from termcolor import cprint


async def download_link(session: ClientSession):
    url_1 = 'https://api.denumpay.ru/test/hs/api/v1/payment/ia/new'
    data = '{"account": "27cea98a-19f6-469c-857b-efeee3675c11","paymentId": "123123123", "amount": 1000000,"currency": 643, "hold": false, "interaction": "pf", "redirectUrl": { "success": "www.google.com","fail": "www.yandex.ru"}, "callbackUrl": {"success": "www.google.com", "fail": "www.yandex.ru"},"paymentInfo":{"orderId": "Займ 010101","orderInfo": "тут текст"}}'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token,
    }
    async with session.post(url=url_1, data=data, headers=headers) as response_1:
        result = await response_1.json()
        if response_1.status != 201:
            print(f'Request 1 - error    status: {response_1.status}')
            return
        payment_id = result['data']['paymentId']

        url_2 = 'https://api.denumpay.ru/test/hs/api/v1/payment/ia/pay?paymentId=' + payment_id
        data = '{"cardNumber":"1000111122223331","expDate":"01/25","cardHolder":"John Doe","cvv":"000","salt":"yGpCVni2eWc~,z3ZKDDUXe~xB,D6U.}tHwtyN-y}s-PQh++Yo"}'
        async with session.post(url=url_2, data=data, headers=headers) as response_2:
            result = await response_2.json()
            if response_2.status != 201:
                print(f'Request 2 - error    status: {response_1.status}')
                return
        print(
            f'Ping two URLs: paymentId = {payment_id}, paymentState = {result["data"]["paymentState"]}, redirectUrl = {result["data"]["redirectUrl"]}')


async def download_all(number: int, limit: int):
    my_conn = aiohttp.TCPConnector(limit=limit)
    async with aiohttp.ClientSession(connector=my_conn) as session:
        tasks = []
        for i in range(number):
            task = asyncio.ensure_future(download_link(session=session))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)  # the await must be nest inside of the session


cprint('=========================================================================', 'green', 'on_blue')
cprint(f'limit of connections: {limit_of_connections}       number of requests: {number_of_requests}', 'white',
       'on_blue')
cprint('=========================================================================', 'green', 'on_blue')
start = time.time()
asyncio.run(download_all(number=number_of_requests, limit=limit_of_connections))
end = time.time()
print(f'ping {number_of_requests} links in {end - start} seconds')
