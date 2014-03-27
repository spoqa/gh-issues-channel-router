import markdown


class Payload(object):

    def __init__(self, channel=None, number=None, title=None, action=None,
                 user=None, body=None, url=None, username="github",
                 commit_id=None, icon_emoji=":octocat:", attachments=None):
        self.channel = channel
        self.number = number
        self.title = title
        self.action = action
        self.user = user
        self.body = body
        self.url = url
        self.commit_id = commit_id

        self.username = username
        self.icon_emoji = icon_emoji
        self.attachments = attachments if attachments else \
                               self.default_attachments

    @property
    def message(self):
        result = "%s" % self.title if self.title else ""
        result += "(#%s) " % self.number if self.number else ""
        result += "[@%s] " % self.commit_id if self.commit_id else ""
        result += "%s " % self.action.upper() if self.action else ""
        result += "by @%s\n" % self.user if self.user else "\n"
        result += "%s\n" % self.body if self.body else ""
        result += "%s" % self.url if self.url else ""
        return result

    def _generate_default_fields(self):
        fields = []
        _fields = ["number", "title", "action", "user", "body", "url",
                   "commit_id"]
        for x in _fields:
            value = getattr(self, x)
            if value:
                if x == "body":
                    value = markdown.markdown(value)
                    short = True
                else:
                    short = False
                fields.append(Field(title=x, value=value, short=short))
        return fields

    @property
    def default_attachments(self):
        attachments = Attachment(self.message, "", "96bde5",
                                 self._generate_default_fields())
        return attachments

    def to_dict(self):
        result_dict = {"username": self.username, "icon_emoji": self.icon_emoji,
                       "channel": "#%s" % self.channel, "text": self.message,
                       "attachments": self.attachments}
        return result_dict


class Attachment(object):

    def __init__(self, fallback="", text="", color="96bde5", *fields):
        self.fallback = fallback
        self.text = text
        self.pretext = markdown.markdown(text)
        self.color = color
        self.fields = fields

    def to_dict(self):
        return {
            "fallback": self.fallback,
            "text": self.text,
            "pretext": self.pretext,
            "color": self.color,
            "fields": [x.to_dict() for x in self.fields]
        }


class Field(object):

    def __init__(self, title, value, short=False):

        self.title = title
        self.value = value
        self.short = short

    def to_dict(self):

        return {
            "title": self.title,
            "value": self.value,
            "short": self.short
        }
