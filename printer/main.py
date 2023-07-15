from typing import Optional
import requests


class Printer:
    base_url = 'http://localhost:8000/api/checks/'

    def __init__(self, name: str, api_key: str, check_type: str, point_id: int):
        self.name = name
        self.api_key = api_key
        self.check_type = check_type
        self.point_id = point_id

    def get_pdf_list(self, /, check_status: str = 'r') -> requests.Response:
        return self.send_response(endpoint=self.base_url, params={'check_status': check_status})

    def get_pdf(self, filename: str) -> requests.Response:
        return self.send_response(endpoint=self.base_url + filename)

    def set_printed(self, filename: str) -> requests.Response:
        return self.send_response(endpoint=self.base_url + filename, method='patch')

    def send_response(self, endpoint: str,
                      params: Optional[dict] = None,
                      method: Optional[str] = 'post') -> requests.Response:
        if params is None:
            params = dict()
        params['api_key'] = self.api_key

        match method:
            case 'post':
                response = requests.post(endpoint, data=params)
            case 'patch':
                response = requests.patch(endpoint, data=params)
            case _:
                raise ValueError('Unsupported method')

        match response.status_code:
            case 200:
                return response
            case 403:
                print('Access forbidden')
            case 404:
                print('Page not found')
            case _:
                pass
        raise ValueError(response.raise_for_status())

    def print_file(self, file: bytes, filename: Optional[str]):
        """
        Print emulating
        """
        if filename:
            print(filename)
        print('*' * 10)
        print('\n' * 5)
        print('*' * 10)

    def work(self):
        new_checks = self.get_pdf_list().json()

        match new_checks['message']:
            case 'ok':
                for filename in new_checks['files']:
                    pdf = self.get_pdf(filename)
                    self.print_file(pdf.content, filename)
                    self.set_printed(filename)
            case 'empty':
                ...  # do something
                print('empty')
            case _:
                raise ValueError('')
