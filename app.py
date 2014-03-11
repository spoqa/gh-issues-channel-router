import json
import requests

from flask import Flask, request, jsonify

app = Flask(__name__)
url = ('https://spoqa.slack.com/services/hooks/incoming-webhook'
       '?token=EqCiU0T2MCimJLsn30j7JUPF')


@app.route('/', methods=['GET', 'POST'])
def index():
    data = json.loads(request.data)
    if request.headers['X-GitHub-Event'] == 'issue_comment':
        for label in data['issue']['labels']:
            payload = {
                "username": "github",
                "icon_emoji": ":octocat:",
                "channel": u"#{0}".format(label['name']),
                "text": u"#{0} @{1}: {2}\n<{2}>".format(
                    data['issue']['id'],
                    data['comment']['user']['login'],
                    data['comment']['body'],
                    data['comment']['url']
                )
            }
            r = requests.post(url, data=json.dumps(payload))
    if request.headers['X-GitHub-Event'] == 'issues':
        for label in data['issue']['labels']:
            payload = {
                "username": "github",
                "con_emoji": ":octocat:",
                "channel": u"#{0}".format(label['name']),
                "text": u"#{0} {1} by @{2}\n{3}\n<{4}>".format(
                    data['issue']['id'],
                    data['issue']['title'],
                    data['issue']['user']['login'],
                    data['issue']['body'],
                    data['issue']['url']
                )
            }
            r = requests.post(url, data=json.dumps(payload))
    return jsonify(result='success')

if __name__ == "__main__":
    app.run(debug=True)
