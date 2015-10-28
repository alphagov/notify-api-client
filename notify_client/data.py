from __future__ import unicode_literals
from .base import BaseAPIClient
from .errors import HTTPError


class DataAPIClient(BaseAPIClient):
    def init_app(self, app):
        self.base_url = app.config['NOTIFY_DATA_API_URL']
        self.auth_token = app.config['NOTIFY_DATA_API_AUTH_TOKEN']

    def register(self, email_address, password, mobile_number):
        return self._post(
            '/users',
            data={
                "user": {
                    "emailAddress": email_address,
                    "password": password,
                    "mobileNumber": mobile_number
                }
            })

    def get_organisation(self, organisation_id):
        try:
            return self._get("/organisation/{}".format(organisation_id))
        except HTTPError as e:
            if e.status_code != 404:
                raise
        return None

    def get_user_by_email_address(self, email_address):
        try:
            return self._get("/users", params={"email_address": email_address})
        except HTTPError as e:
            if e.status_code != 404:
                raise
        return None

    def get_user_by_id(self, user_id):
        try:
            return self._get("/users/{}".format(user_id))
        except HTTPError as e:
            if e.status_code != 404:
                raise
        return None

    def get_users_by_service_id(self, service_id):
        return self._get("/service/{}/users".format(service_id))

    def authenticate_user(self, email_address, password):
        try:
            return self._post(
                '/users/auth',
                data={
                    "userAuthentication": {
                        "emailAddress": email_address,
                        "password": password,
                    }
                })
        except HTTPError as e:
            if e.status_code not in [400, 403, 404]:
                raise
        return None

    def add_user_to_service(self, email_address, service_id):
        return self._post(
            '/service/{}/add-user'.format(service_id),
            data={
                "user": {
                    "emailAddress": email_address
                }
            })

    def remove_user_from_service(self, email_address, service_id):
        return self._post(
            '/service/{}/remove-user'.format(service_id),
            data={
                "user": {
                    "emailAddress": email_address
                }
            })

    def activate_user(self, user_id):
        return self._post('/user/{}/activate'.format(user_id))

    def get_service_by_user_id_and_service_id(self, user_id, service_id):
        return self._get("/user/{}/service/{}".format(user_id, service_id))

    def get_services_by_user_id(self, user_id):
        return self._get("/user/{}/services".format(user_id))

    def get_services_usage(self, service_id):
        return self._get("/service/{}/usage".format(service_id))

    def create_service(self, service_name, user_id):
        return self._post(
            '/service',
            data={
                "service": {
                    "name": service_name,
                    "userId": user_id
                }
            })

    def activate_service(self, service_id):
        return self._post('/service/{}/activate'.format(service_id), data={})

    def deactivate_service(self, service_id):
        return self._post('/service/{}/deactivate'.format(service_id), data={})

    def create_job(self, job_name, service_id):
        return self._post(
            '/job',
            data={
                "job": {
                    "name": job_name,
                    "serviceId": service_id
                }
            })

    def get_jobs_by_service_id(self, service_id):
        return self._get("/service/{}/jobs".format(service_id))

    def get_notifications_by_job_id(self, job_id):
        return self._get("/job/{}/notifications".format(job_id))

    def get_notification_by_id(self, notification_id):
        return self._get("/notification/{}".format(notification_id))

    def send_sms(self, mobile_number, message, job_id=None, token=None):

        notification = {}
        notification.update({
            "to": mobile_number,
            "message": message
        })

        if job_id:
            notification.update({
                "jobId": job_id
            })

        return self._post(
            '/sms/notification',
            data={
                "notification": notification
            }, token=token)
