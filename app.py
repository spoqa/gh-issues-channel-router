import os
import json
import requests

from flask import Flask, request, jsonify

from responses import Payload


SLACK_REQUEST_URL = os.environ.get("SLACK_REQUEST_URL")
GITHUB_OAUTH_TOKEN =  os.environ.get("GITHUB_OAUTH_TOKEN")


app = Flask(__name__)


def slack_request(payload):
    return requests.post(SLACK_REQUEST_URL, data=json.dumps(payload.to_dict()))


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
        event = request.headers.get("X-GitHub-Event")
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
        slack_request(
            Payload(channel=label["name"], number=data["issue"]["number"],
                    user=data["comment"]["user"]["login"],
                    body=data["comment"]["body"],
                    url=data["comment"]["html_url"]
            )
        )


@handler.add_event("issues")
def issues(data):
    for label in data["issue"]["labels"]:
        slack_request(
            Payload(channel=label["name"],
                    number=data["issue"]["number"],
                    title=data["issue"]["title"],
                    user=data["issue"]["user"]["login"],
                    body=data["issue"]["body"],
                    url=data["issue"]["html_url"]
            )
        )


@handler.add_event("issues", actions=["closed", "reopened"])
def issues(data):
    for label in data["issue"]["labels"]:
        slack_request(
            Payload(channel=label["name"],
                    number=data["issue"]["number"],
                    action=data["action"],
                    title=data["issue"]["title"],
                    user=data["issue"]["user"]["login"],
                    body=data["issue"]["body"],
                    url=data["issue"]["html_url"]
            )
        )


@handler.add_event("pull_request")
def pull_requests(data):
    data = data["pull_request"]
    issue_url = data["issue_url"]
    result = json.loads(requests.get(issue_url, auth=(GITHUB_OAUTH_TOKEN, 
                                                      "x-oauth-basic")).text)
    for label in result["labels"]:
        slack_request(
            Payload(channel=label["name"],
                    number=data["number"],
                    action=data["state"],
                    title=data["title"],
                    user=data["user"]["login"],
                    body=data["body"],
                    url=data["html_url"]
            )
        )


@handler.add_event("pull_request_review_comment")
def pull_request_review_comment(data):
    data = data["pull_request_review_comment"]
    pr_url = data["pull_request_url"]
    result = json.loads(requests.get(pr_url, auth=(GITHUB_OAUTH_TOKEN, 
                                                   "x-oauth-basic")).text)
    result = json.loads(requests.get(result["pull_request"]["issue_url"],
                                     auth=(GITHUB_OAUTH_TOKEN,
                                           "x-oauth-basic")).text)
    for label in result["labels"]:
        slack_request(
            Payload(channel=label["name"],
                    title=data["id"],
                    commit_id=data["commit_id"],
                    user=data["user"]["login"],
                    body=data["body"],
                    url=data["_links"]["html"]["href"]
            )
        )


@app.route("/", methods=["GET", "POST"])
def index():
    handler.handle()
    return jsonify(result="success")

if __name__ == "__main__":
    app.run(debug=True)
