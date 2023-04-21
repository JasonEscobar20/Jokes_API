import requests, time

from concurrent.futures import ThreadPoolExecutor
from concurrent import futures

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ListarDatos(APIView):

    def request_api(self, url):
        session = requests.Session()

        with session.get(url) as response:
            return response.json()

    def get(self, request, *args, **kwargs):
        start_time = time.perf_counter()
        data = []
        futures_instances = []
        validates_ids = []

        with ThreadPoolExecutor(max_workers=15) as executor:
            for url in range(1, 26):
                test_api = executor.submit(self.request_api, 'https://api.chucknorris.io/jokes/random')
                futures_instances.append(test_api)

            for future in futures.as_completed(futures_instances):
                response = future.result()
                get_id = response.get('id')

                if get_id not in validates_ids:
                    data.append(response)
                    validates_ids.append(get_id)
                else:
                    task = executor.submit(self.request_api, 'https://api.chucknorris.io/jokes/random')
                    task_response = task.result()
                    data.append(task_response)

        end_time = time.perf_counter()
        print('tiempo de respuesta: ', end_time - start_time)

        return Response(data, status=status.HTTP_200_OK)