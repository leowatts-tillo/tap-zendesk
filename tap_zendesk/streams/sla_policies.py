import json
from zenpy.lib.exception import APIException
from tap_zendesk import http
from tap_zendesk.streams.abstracts import Stream


class SLAPolicies(Stream):
    name = "sla_policies"
    replication_method = "FULL_TABLE"
    is_optional = True

    def sync(self, state): # pylint: disable=unused-argument
        for policy in self.client.sla_policies():
            yield (self.stream, policy)

    def check_access(self):
        '''
        Check whether the permission was given to access stream resources or not.
        '''
        try:
            self.client.sla_policies()
        except APIException as e:
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
