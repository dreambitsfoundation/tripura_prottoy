import json
from django.http import HttpRequest


class JsonRequestParser:
    """ This class is useful for parsing the arguments in a JSON request """
    _arguments = {}
    _request: HttpRequest = None

    def __init__(self, request):
        print(request.body)
        temp_json_body = json.loads(request.body)
        self._arguments = temp_json_body
        self._request = request

    def get(self, argument_name: str):
        return self._arguments[argument_name]

    def get_or_none(self, argument_name: str):
        try:
            return self._arguments[argument_name]
        except KeyError as e:
            return None

    def set(self, argument_name: str = None, value = None):
        if argument_name is None:
            raise ValueError
        if value is None:
            raise ValueError
        try:
            self._arguments[argument_name] = value
            self._request._body = json.dumps(self._arguments)
        except Exception as e:
            raise e

    def get_request(self):
        return self._request
