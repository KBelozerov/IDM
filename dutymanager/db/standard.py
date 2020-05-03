from .abc import AbstractDict
from .models import Chat, Trusted, Template
from typing import Union

__all__ = (
    'Chats', 'Chat',
    'Proxies', 'Trusted',
    'Templates', 'Template'
)


class Chats(AbstractDict):

    dataclass = Chat

    def __call__(self, uid: str, field: str = "id") -> Union[str, int]:
        return self[uid].get(field, "null")

    async def create(self, *args):
        uid, chat_id, title = args
        await Chat.create(uid=uid, id=chat_id, title=title)
        self[uid] = {"id": chat_id, "title": title}

    async def remove(self, uid: int) -> int:
        await Chat.filter(uid=uid).delete()
        return self.pop(uid)

    async def change(self, uid: int, **kwargs):
        await Chat.filter(uid=uid).update(**kwargs)
        self[uid].update(**kwargs)


class Templates(AbstractDict):

    dataclass = Template

    def __call__(self, tag: str) -> dict:
        return self[tag.lower()]

    async def create(self, *args):
        tag, text, attachments = args
        save = await Template.create(
            tag=tag.lower(),
            text=text,
            attachments=attachments
        )
        self[save.tag] = {"message": text, "attachment": attachments}

    async def remove(self, tag: str):
        await Template.filter(tag=tag.lower()).delete()
        self.pop(tag.lower())

    async def change(self, tag: str, **kwargs):
        await Template.filter(tag=tag.lower()).update(**kwargs)
        self[tag.lower()].update(**kwargs)


class Proxies(AbstractDict):

    dataclass = Trusted

    def __call__(self, uid: int) -> str:
        return self[uid]

    async def create(self, *args):
        uid, name = args
        await Trusted.create(id=uid, name=name)
        self[uid] = name

    async def remove(self, uid: int):
        await Trusted.filter(id=uid).delete()
        self.pop(uid)

    async def change(self, *args):
        uid, name = args
        await Trusted.filter(id=uid).update(name=name)
        self[uid] = name