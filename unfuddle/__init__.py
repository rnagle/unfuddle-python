import json
import requests


class Unfuddle:

    def __init__(self, account, username, password):
        self.account = account
        self.username = username
        self.password = password
        self.base = 'https://%s.unfuddle.com/api/v1/' % self.account

    def get(self, url, query=None):
        if query is not None:
            url += '?' + dict_to_qs(query)

        resp = requests.get(
            self.base + url,
            auth=(self.username, self.password),
            verify=False,
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            })

        if resp.status_code >= 500:
            resp.raise_for_status()

        return json.loads(resp.content)

    def post(self):
        pass

    def put_json(self, url, data):
        resp = requests.put(
            self.base + url,
            auth=(self.username, self.password),
            data=json.dumps(data),
            verify=False,
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            })

        if resp.ok:
            return True
        else:
            return False

    def delete(self):
        pass

    def initializer(self):
        return self.get("initializer")

    # Account
    def get_account(self):
        return self.get("account")

    # Tickets
    def get_tickets(self, project_id):
        url = "projects/%s/tickets" % project_id
        return self.get(url)

    def get_ticket(self, project_id, id):
        url = "projects/%s/tickets/%s" % (project_id, id)
        return self.get(url)

    def update_ticket(self, ticket={}):
        url = "projects/%s/tickets/%s" % (ticket["project_id"], ticket["id"])
        return self.put_json(url, data={"ticket": ticket})

    def get_ticket_report(self, query={}):
        """
        title: "Title of the report"
        group_by: [project, priority, component, version, severity, milestone,
                due_on, reporter, assignee, status, resolution, field_1,
                field_2, field_3]
        sort_by: field to sort by
        sort_direction: [ASC, DESC]
        fields_string: fields to include in respoonse
        conditions_string:
            "field-expr-value, field-expr-value | field-expr-value"
            e.g. "due_on-gteq-2013-03-08"
        """

        url = "ticket_reports/dynamic"

        return self.get(url, query)

    # People
    def get_people(self, project_id=None):
        url = "people"

        if project_id is not None:
            url = "%s/%s" (url, project_id)

        return self.get(url)

    def get_person(self, id):
        url = "people/%s" % id
        return self.get(url)

    # Milestones
    def get_milestones(self, project_id=None, status=None):

        if project_id is not None:
            url = "projects/%s/milestones" % project_id
            return self.get(url)

        url = "milestones"

        if status is not None:
            url = "%s/%s" % (url, status)

        return self.get(url)

    def get_milestone(self, project_id, id):
        url = "projects/%s/milestones/%s" % (project_id, id)
        return self.get(url)

    # Projects
    def get_projects(self):
        return self.get("projects")

    def get_project(self, id=None, short_name=None):
        if id is not None:
            url = "projects/%s" % id

        if short_name is not None:
            url = "projects/by_short_name/%s" % short_name

        return self.get(url)

    # TODO: Repositories
    # TODO: Messages
    # TODO: Notebooks
    # TODO: Time Tracking
    # TODO: Attachments
    # TODO: Comments


class UnfuddleError(Exception):

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return repr(self.value)

    def __str__(self):
        return str(self.value)


def dict_to_qs(dictionary):
    qs = list()

    for k, v in dictionary.items():
        if isinstance(v, dict):
            for k2, v2 in v.items():
                if type(v2) in (str, unicode, int, float, bool):
                    qs.append("%s[%s]=%s" % (k, k2, v2))
                elif type(v2) in (list, tuple):
                    for v3 in v2:
                        qs.append("%s[%s][]=%s" % (k, k2, v3))
                else:
                    raise TypeError
        elif type(v) in (str, unicode, int, float, bool):
            qs.append("%s=%s" % (k, v))
        elif type(v) in (list, tuple):
            for v2 in v:
                qs.append("%s[]=%s" % (k, v2))
        else:
            raise TypeError

    return "&".join(qs)
