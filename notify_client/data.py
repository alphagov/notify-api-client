from __future__ import unicode_literals
from .base import BaseAPIClient


class NotifyAPIClient(BaseAPIClient):
    def init_app(self, app):
        self.base_url = app.config['NOTIFY_DATA_API_URL']
        self.auth_token = app.config['NOTIFY_DATA_API_AUTH_TOKEN']

    def send_sms(self, mobile_number, message, job_id=None, token=None, description=None):

        notification = {}
        notification.update({
            "to": mobile_number,
            "message": message
        })

        if job_id:
            notification.update({
                "jobId": job_id
            })

        if description:
            notification.update({
                "description": description
            })

        return self._post(
            '/sms/notification',
            data={
                "notification": notification
            }, token=token)

    def fetch_notifications(self):
        return self._get('/notifications')
