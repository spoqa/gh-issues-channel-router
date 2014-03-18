import json
import requests

from flask import Flask, request, jsonify

from conf import token, github_oauth_token


app = Flask(__name__)
url = ("https://spoqa.slack.com/services/hooks/incoming-webhook"
       "?token=%s" % token)


class GhEventHandler(object):

    _handler_map = {}

    def add_event(self, event, **options):
        def decorator(handler):
            if event not in self._handler_map:
                self._handler_map[event] = dict(actions={})

            if "actions" in options:
                assert len(options["actions"]) != 0, \
                    "{0} has empty actions".format(handler.__name__)
                for action in options["actions"]:
                    self._handler_map[event]["actions"][action] = handler
            else:
                self._handler_map[event]["default"] = handler

            def decorated_function(*args, **kwargs):
                return handler(*args, **kwargs)
            return decorated_function
        return decorator

    def handle(self):
        event = request.headers.get("X-GitHub-Event", None)
        if event in self._handler_map:
            try:
                data = json.loads(request.data)
            except ValueError:
                data = json.loads(request.values.get("payload"))
            action = data["action"]
            if action in self._handler_map[event]["actions"]:
                self._handler_map[event]["actions"][action](data)
            elif "default" in self._handler_map[event]:
                self._handler_map[event]["default"](data)


handler = GhEventHandler()


@handler.add_event("issue_comment")
def issue_comment(data):
    for label in data["issue"]["labels"]:
        payload = {
            "username": "github",
            "icon_emoji": ":octocat:",
            "channel": u"#{0}".format(label["name"]),
            "text": u"#{0} @{1}: {2}\n<{3}>".format(
                data["issue"]["number"],
                data["comment"]["user"]["login"],
                data["comment"]["body"],
                data["comment"]["html_url"]
            )
        }
        requests.post(url, data=json.dumps(payload))


@handler.add_event("issues")
def issues(data):
    for label in data["issue"]["labels"]:
        payload = {
            "username": "github",
            "icon_emoji": ":octocat:",
            "channel": u"#{0}".format(label["name"]),
            "text": u"#{0} {1} by @{2}\n{3}\n<{4}>".format(
                data["issue"]["number"],
                data["issue"]["title"],
                data["issue"]["user"]["login"],
                data["issue"]["body"],
                data["issue"]["html_url"]
            )
        }
        requests.post(url, data=json.dumps(payload))


@handler.add_event("issues", actions=["closed", "reopened"])
def issues(data):
    for label in data["issue"]["labels"]:
        payload = {
            "username": "github",
            "icon_emoji": ":octocat:",
            "channel": u"#{0}".format(label["name"]),
            "text": u"{0}(#{1}) {2} by @{3}\n{4}\n<{5}>".format(
                data["issue"]["title"],
                data["issue"]["number"],
                data["action"].upper(),
                data["issue"]["user"]["login"],
                data["issue"]["body"],
                data["issue"]["html_url"]
            )
        }
        requests.post(url, data=json.dumps(payload))


@handler.add_event("pull_request")
def pull_requests(data):
    data = data["pull_request"]
    issue_url = data["issue_url"]
    result = json.loads(requests.get(issue_url, auth=(github_oauth_token, 
                                                      "x-oauth-basic")).text)
    for label in result["labels"]:
        payload = {
            "username": "github",
            "icon_emoji": ":octocat:",
            "channel": u"#{0}".format(label["name"]),
            "text": u"{0}(#{1}) {2} by @{3}\n{4}\n<{5}>".format(
                data["title"],
                data["number"],
                data["state"].upper(),
                data["user"]["login"],
                data["body"],
                data["html_url"]
            )
        }
        requests.post(url, data=json.dumps(payload))


@app.route("/", methods=["GET", "POST"])
def index():
    handler.handle()
    return jsonify(result="success")

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)
