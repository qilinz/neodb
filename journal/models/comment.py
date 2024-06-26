from datetime import datetime
from functools import cached_property

from django.db import models
from django.utils import timezone

from catalog.models import Item
from users.models import APIdentity

from .common import Content
from .rating import Rating
from .renderers import render_text


class Comment(Content):
    text = models.TextField(blank=False, null=False)

    @property
    def ap_object(self):
        d = {
            "id": self.absolute_url,
            "type": "Comment",
            "content": self.text,
            "published": self.created_time.isoformat(),
            "updated": self.edited_time.isoformat(),
            "attributedTo": self.owner.actor_uri,
            "withRegardTo": self.item.absolute_url,
            "href": self.absolute_url,
        }
        if self.metadata.get("position"):
            d["relatedWithItemPosition"] = self.metadata["position"]
            d["relatedWithItemPositionType"] = "time"
        return d

    @classmethod
    def update_by_ap_object(cls, owner, item, obj, post_id, visibility):
        p = cls.objects.filter(owner=owner, item=item).first()
        if p and p.edited_time >= datetime.fromisoformat(obj["updated"]):
            return p  # incoming ap object is older than what we have, no update needed
        content = obj.get("content", "").strip() if obj else ""
        if not content:
            cls.objects.filter(owner=owner, item=item).delete()
            return
        d = {
            "text": content,
            "local": False,
            "remote_id": obj["id"],
            "visibility": visibility,
            "created_time": datetime.fromisoformat(obj["published"]),
            "edited_time": datetime.fromisoformat(obj["updated"]),
        }
        if obj.get("relatedWithItemPosition"):
            d["metadata"] = {"position": obj["relatedWithItemPosition"]}
        p, _ = cls.objects.update_or_create(owner=owner, item=item, defaults=d)
        p.link_post_id(post_id)
        return p

    @property
    def html(self):
        return render_text(self.text)

    @cached_property
    def rating_grade(self):
        return Rating.get_item_rating(self.item, self.owner)

    @cached_property
    def mark(self):
        from .mark import Mark

        m = Mark(self.owner, self.item)
        m.comment = self
        return m

    @property
    def item_url(self):
        if self.metadata.get("position"):
            return self.item.get_url_with_position(self.metadata["position"])
        else:
            return self.item.url

    @staticmethod
    def comment_item(
        item: Item, owner: APIdentity, text: str | None, visibility=0, created_time=None
    ):
        comment = Comment.objects.filter(owner=owner, item=item).first()
        if not text:
            if comment is not None:
                comment.delete()
                comment = None
        elif comment is None:
            comment = Comment.objects.create(
                owner=owner,
                item=item,
                text=text,
                visibility=visibility,
                created_time=created_time or timezone.now(),
            )
        elif comment.text != text or comment.visibility != visibility:
            comment.text = text
            comment.visibility = visibility
            if created_time:
                comment.created_time = created_time
            comment.save()
        return comment
