import requests

from botctl import errors
from botctl.types import PlatformVariable


class Gateway:
    def __init__(self, config):
        self._config = config
        self._environment = config.get_environment()
        self._headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        self._configure_host()

    def _request(self, method, endpoint, headers, data, json, fail):
        if headers:
            self._headers.update(headers)

        request_parameters = {'headers': self._headers}

        if data:
            request_parameters['data'] = data

        if json:
            request_parameters['json'] = json

        try:
            response = requests.request(
                method,
                self._host + endpoint,
                **request_parameters
            )
        except requests.exceptions.MissingSchema:
            raise errors.InvalidRemoteHost(self._host)
        except requests.exceptions.ConnectionError:
            raise errors.GatewayConnectionError(self._host)

        if response.status_code == 401:
            raise errors.TokenExpiredError(response)

        if (fail, response.ok) == (True, False):
            raise errors.GatewayError(response)

        return response

    def _configure_host(self):
        raise NotImplementedError

    def delete(self, endpoint, headers={}, data={}, json={}, fail=True):
        return self._request('DELETE', endpoint, headers, data, json, fail)

    def get(self, endpoint, headers={}, data={}, json={}, fail=True):
        return self._request('GET', endpoint, headers, data, json, fail)

    def post(self, endpoint, headers={}, data={}, json={}, fail=True):
        return self._request('POST', endpoint, headers, data, json, fail)

    def put(self, endpoint, headers={}, data={}, json={}, fail=True):
        return self._request('PUT', endpoint, headers, data, json, fail)


class BotCMSGateway(Gateway):
    def _configure_host(self):
        self._headers.update({
            'Authorization': self._config.get_value(self._environment,
                                                    PlatformVariable.TOKEN)
        })
        self._host = self._config.get_value(self._environment,
                                            PlatformVariable.CMS) + '/api/v1'


class BotIntegrationsGateway(Gateway):
    def _configure_host(self):
        self._headers.update({
            'Authorization': self._config.get_value(
                self._environment,
                PlatformVariable.API_SECRET
            )
        })
        self._host = self._config.get_value(
            self._environment,
            PlatformVariable.INTEGRATIONS_MANAGER
        )


class BotAnalyticsGateway(Gateway):
    def _configure_host(self):
        self._host = self._config.get_value(
            self._environment,
            PlatformVariable.ANALYTICS
        )
        self._headers.update({
            'Authorization': self._config.get_value(
                self._environment,
                PlatformVariable.TOKEN
            )
        })
