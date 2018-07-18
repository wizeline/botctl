import os
import json
import sys

import requests

from botctl.errors import GatewayError


class Gateway:
    def __init__(self, config):
        self._config = config
        self._headers = {
            'Content-Type': 'application/json',
            'Authorization': self._config.get_value('token'),
            'Accept': 'application/json'
        }
        self._configure_host()

    def _request(self, method, endpoint, headers, data, json):
        self._headers.update(headers)
        response = requests.request(
            method,
            self._host + endpoint,
            headers=self._headers,
            data=data,
            json=json
        )

        if not response.ok:
            sys.stderr.write(f'Request failed: {response.status_code}\n'
                             f'Response body: {response.text}\n')
            raise GatewayError(response)

        return response

    def _configure_host(self):
        self._host = ''

    def get(self, endpoint, headers={}, data={}, json={}):
        return self._request('GET', endpoint, headers, data, json)

    def post(self, endpoint, headers={}, data={}, json={}):
        return self._request('POST', endpoint, headers, data, json)

    def delete(self, endpoint, headers={}, data={}, json={}):
        return self._request('DELETE', endpoint, headers, data, json)


class BotCMSGateway(Gateway):
    def _configure_host(self):
        self._host = self._config.get_value('cms') + '/api/v1'
