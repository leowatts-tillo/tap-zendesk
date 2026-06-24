import json
import requests
from zenpy.lib.exception import APIException
from tap_zendesk import http
from tap_zendesk.exceptions import ZendeskNotFoundError
from tap_zendesk.streams.abstracts import Stream


class TalkPhoneNumbers(Stream):
    name = 'talk_phone_numbers'
    replication_method = "FULL_TABLE"
    is_optional = True

    def sync(self, state): # pylint: disable=unused-argument
        for phone_number in self.client.talk.phone_numbers():
            yield (self.stream, phone_number)

    def check_access(self):
        try:
            self.client.talk.phone_numbers()
        except ZendeskNotFoundError:
            # Skip 404 as goal is to check whether TalkPhoneNumbers have read permission
            pass
        except requests.exceptions.HTTPError as e:
            # Zenpy's Talk API raises requests.HTTPError directly for certain HTTP errors.
            # Convert 403 Forbidden to ZendeskForbiddenError for consistent handling in discover.py.
            if e.response is not None and e.response.status_code == 403:
                raise http.ZendeskForbiddenError(str(e)) from None
            raise
        except APIException as e:
            # Handle Zenpy APIException 403 with various message formats
            try:
                args0 = json.loads(e.args[0])
                err = args0.get('error')
                description = args0.get('description', '')
            except (json.JSONDecodeError, ValueError, IndexError) as exc:
                raise e from exc
            if (isinstance(err, dict) and err.get('message') == "Access to this resource is restricted. Please contact the account administrator for assistance.") \
                    or description == "Missing the following required scopes: read":
                raise http.ZendeskForbiddenError(str(e)) from None
            raise
