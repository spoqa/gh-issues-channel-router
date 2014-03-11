import json

from flask import Flask, request, jsonify

app = Flask(__name__)
url = ('https://spoqa.slack.com/services/hooks/incoming-webhook'
       '?token=EqCiU0T2MCimJLsn30j7JUPF')

@app.route('/')
def index():
    data = json.loads(request.data)
    if 'issue_comment' in data:
        for label in data['issue_comment']['issue']['labels']:
            payload = {
                "username": "github",
                "icon_emoji": ":octocat:",
                "channel":u"#{0}".format(label['name']),
                "text": u"#{0} @{1}: {2}\n<{2}>".format(
                    data['issue_comment']['issue']['id'],
                    data['issue_comment']['comment']['user']['login'],
                    data['issue_comment']['comment']['body'],
                    data['issue_comment']['comment']['url']
                )
            }
            r=requests.post(url, data=json.dumps(payload))
    if 'issues' in data:
        for label in data['issues']['issue']['labels']:
            payload = {
                "username": "github",
                "icon_emoji": ":octocat:",
                "channel":u"#{0}".format(label['name']),
                "text": u"#{0} {1} by @{2}\n{3}\n<{4}>".format(
                    data['issues']['issue']['id'],
                    data['issues']['issue']['title'],
                    data['issues']['issue']['user']['login'],
                    data['issues']['issue']['body'],
                    data['issues']['issue']['url']
                )
            }
            r=requests.post(url, data=json.dumps(payload))
    return jsonify(result='success')

if __name__ == "__main__":
    app.run(debug=True)

