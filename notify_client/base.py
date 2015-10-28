from __future__ import absolute_import

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

import requests

from .errors import HTTPError, InvalidResponse


class BaseAPIClient(object):
    def __init__(self, base_url=None, auth_token=None, enabled=True):
        self.base_url = base_url
        self.auth_token = auth_token
        self.enabled = enabled

    def _put(self, url, data):
        return self._request("PUT", url, data=data)

    def _get(self, url, params=None):
        return self._request("GET", url, params=params)

    def _post(self, url, data, token=None):
        return self._request("POST", url, data=data, token=token)

    def _delete(self, url, data=None):
        return self._request("DELETE", url, data=data)

    def _request(self, method, url, data=None, params=None, token=None):
        if not self.enabled:
            return None

        url = urlparse.urljoin(self.base_url, url)

        print("API request %s %s", method, url)
        headers = {
            "Content-type": "application/json",
            "Authorization": "Bearer {}".format(token if token else self.auth_token)
        }

        try:
            response = requests.request(
                method, url,
                headers=headers, json=data, params=params)
            response.raise_for_status()
        except requests.RequestException as e:
            api_error = HTTPError.create(e)
            print(
                "API %s request on %s failed with %s '%s'",
                method, url, api_error.status_code, api_error.message)
            raise api_error
        finally:
            print("API %s request on %s finished in %s", method, url)

        try:
            return response.json()
        except ValueError:
            raise InvalidResponse(
                response,
                message="No JSON object could be decoded"
            )
