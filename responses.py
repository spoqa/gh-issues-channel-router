


class Payload(object):

    def __init__(self, channel=None, number=None, title=None, action=None,
                 user=None, body=None, url=None, username="github",
                 commit_id=None, icon_emoji="octocat"):
        self.channel = channel
        self.number = number
        self.title = title
        self.action = action
        self.user = user
        self.body = body
        self.url = url
        self.username = username
        self.icon_emoji = icon_emoji
        self.commit_id = commit_id

    @property
    def message(self):
        result = "%s" % self.title if self.title else ""
        result += "(#%s) " % self.number if self.number else ""
        result += "[@%s] " % self.commit_id if self.commit_id else ""
        result += "%s " % self.title if self.title else ""
        result += "%s " % self.action if self.action.upper() else ""
        result += "by @%s\n" % self.user if self.user else "\n"
        result += "%s\n" % self.body if self.body else ""
        result += "%s" % self.url if self.url else ""
        return result

    def to_dict(self):
        result_dict = {"username": self.username, "icon_emoji": self.icon_emoji,
                       "channel": "#%s" % self.channel, "text": self.message}

        return result_dict
