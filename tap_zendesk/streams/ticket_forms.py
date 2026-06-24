import json
from zenpy.lib.exception import APIException
from singer import utils
from tap_zendesk import http
from tap_zendesk.streams.abstracts import Stream


class TicketForms(Stream):
    name = "ticket_forms"
    replication_method = "INCREMENTAL"
    replication_key = "updated_at"
    is_optional = True

    def sync(self, state):
        bookmark = self.get_bookmark(state, self.name)

        forms = self.client.ticket_forms()
        for form in forms:
            if utils.strptime_with_tz(form.updated_at) >= bookmark:
                # NB: We don't trust that the records come back ordered by
                # updated_at (we've observed out-of-order records),
                # so we can't save state until we've seen all records
                self.update_bookmark(state, self.name, form.updated_at)
                yield (self.stream, form)

    def check_access(self):
        '''
        Check whether the permission was given to access stream resources or not.
        '''
        try:
            self.client.ticket_forms()
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
