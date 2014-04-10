

class Payload(object):

    def __init__(self, channel=None, title=None, action=None, number=None,
                 user=None, body=None, url=None, username="Github",
                 commit_id=None, icon_emoji=":octocat:", attachments=None,
                 label=None, color="96bde5"):
        self.channel = channel
        self.title = title
        self.action = action.capitalize() if action else None
        self.number = number
        self.user = user
        if len(body) > 150:
            body = "%s...\n<%s|See more>" % (body[:150], url)
        else:
            body = "%s\n<%s|See more>" % (body[:150], url)
        self.body = body
        self.url = url
        self.commit_id = commit_id
        self.label = label
        self.color = color

        self.username = username
        self.icon_emoji = icon_emoji
        self.attachments = attachments if attachments else \
                               self.default_attachments

    @property
    def message(self):
        result = "%s by <%s|@%s> (<%s|#%s>)" % (self.label,
                     "http://github.com/%s" % self.user, self.user, self.url,
                     self.number)
        return result

    def _generate_default_fields(self):
        fields = []
        _fields = ["action", "commit_id", "user", "title", "body"]
        for x in _fields:
            value = getattr(self, x)
            if value:
                if x not in ["body", "title"]:
                    short = True
                else:
                    short = False
                fields.append(Field(title=x, value=value, short=short))
        return fields

    @property
    def default_attachments(self):
        attachments = Attachment(fallback=self.message,
                                 text=self.body,
                                 color=self.color,
                                 fields=self._generate_default_fields())
        return attachments

    def to_dict(self):
        result_dict = {"username": self.username, "icon_emoji": self.icon_emoji,
                       "channel": "#%s" % self.channel, "text": self.message,
                       "attachments": [self.attachments.to_dict()],}
        return result_dict


class Attachment(object):

    def __init__(self, fallback="", text="", color="96bde5", fields=[]):
        self.fallback = fallback
        self.text = text
        self.color = color
        self.fields = fields

    def to_dict(self):
        return {
            "fallback": self.fallback,
            "color": self.color,
            "fields": [x.to_dict() for x in self.fields],
        }


class Field(object):

    def __init__(self, title, value, short=False):
        self.title = title
        self.value = value
        self.short = short

    def to_dict(self):
        return {
            "title": self.title.capitalize().replace("_", " "),
            "value": self.value,
            "short": self.short,
        }
