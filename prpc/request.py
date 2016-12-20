import json


class Request:

    def __init__(self, func_name: str, func_args: list, func_kwargs: dict):
        self._func_name = func_name
        self._func_args = func_args
        self._func_kwargs = func_kwargs

    @property
    def func_name(self) -> str:
        return self._func_name

    @property
    def func_args(self) -> list:
        return self._func_args

    @property
    def func_kwargs(self) -> dict:
        return self._func_kwargs


def create_request_from_json(json_data):

    def object_hook(dict):
        pass

    return json.loads(json_data, object_hook=object_hook)
