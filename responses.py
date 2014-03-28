import markdown


class Payload(object):

    def __init__(self, channel=None, number=None, title=None, action=None,
                 user=None, body=None, url=None, username="github",
                 commit_id=None, icon_emoji=":octocat:", attachments=None,
                 label=None):
        self.channel = channel
        self.number = number
        self.title = title
        self.action = action
        self.user = user
        self.body = body
        self.url = url
        self.commit_id = commit_id
        self.label = label

        self.username = username
        self.icon_emoji = icon_emoji
        self.attachments = attachments if attachments else \
                               self.default_attachments

    @property
    def message(self):
        result = "%s by @%s (%s)" % (self.label, self.user, self.url)
        return result

    def _generate_default_fields(self):
        fields = []
        _fields = ["number", "title", "action", "user", "body", "url",
                   "commit_id"]
        for x in _fields:
            value = getattr(self, x)
            if value:
                if x == "body":
                    short = True
                else:
                    short = False
                if x == "url":
                    value = "<%(url)s>" % {"url": value}
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
                       "attachments": [self.attachments.to_dict()]}
        return result_dict


class Attachment(object):

    def __init__(self, fallback="", text="", color="96bde5", fields=[]):
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
            "short": self.short,
        }
