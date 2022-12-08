from polymorphic.models import PolymorphicModel
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.contenttypes.models import ContentType
import uuid
from .utils import DEFAULT_ITEM_COVER, item_cover_path
# from django.conf import settings


class IdType(models.TextChoices):
    WikiData = 'wikidata', _('维基数据')
    ISBN10 = 'isbn10', _('ISBN10')
    ISBN = 'isbn', _('ISBN')  # ISBN 13
    ASIN = 'asin', _('ASIN')
    ISSN = 'issn', _('ISSN')
    CUBN = 'cubn', _('统一书号')
    ISRC = 'isrc', _('ISRC')  # only for songs
    UPC = 'upc', _('GTIN UPC EAN码')
    Feed = 'feed', _('Feed URL')
    IMDB = 'imdb', _('IMDb')
    TMDB_TV = 'tmdb_tv', _('TMDB剧集')
    TMDB_TVSeason = 'tmdb_tvseason', _('TMDB剧集')
    TMDB_TVEpisode = 'tmdb_tvepisode', _('TMDB剧集')
    TMDB_Movie = 'tmdb_movie', _('TMDB电影')
    Goodreads = 'goodreads', _('Goodreads')
    Goodreads_Work = 'goodreads_work', _('Goodreads著作')
    GoogleBook = 'googlebook', _('谷歌图书')
    DoubanBook = 'doubanbook', _('豆瓣读书')
    DoubanBook_Work = 'doubanbook_work', _('豆瓣读书著作')
    DoubanMovie = 'doubanmovie', _('豆瓣电影')
    DoubanMusic = 'doubanmusic', _('豆瓣音乐')
    DoubanGame = 'doubangame', _('豆瓣游戏')
    DoubanDrama = 'doubandrama', _('豆瓣舞台剧')
    Bandcamp = 'bandcamp', _('Bandcamp')
    Spotify_Album = 'spotify_album', _('Spotify专辑')
    Spotify_Show = 'spotify_show', _('Spotify播客')
    DoubanBook_Author = 'doubanbook_author', _('豆瓣读书作者')
    DoubanCelebrity = 'doubanmovie_celebrity', _('豆瓣电影影人')
    Goodreads_Author = 'goodreads_author', _('Goodreads作者')
    Spotify_Artist = 'spotify_artist', _('Spotify艺术家')
    TMDB_Person = 'tmdb_person', _('TMDB影人')
    IGDB = 'igdb', _('IGDB游戏')
    Steam = 'steam', _('Steam游戏')
    ApplePodcast = 'apple_podcast', _('苹果播客')


class ItemType(models.TextChoices):
    Book = 'book', _('书')
    TV = 'tv', _('剧集')
    TVSeason = 'tvseason', _('剧集分季')
    TVEpisode = 'tvepisode', _('剧集分集')
    Movie = 'movie', _('电影')
    Music = 'music', _('音乐')
    Game = 'game', _('游戏')
    Boardgame = 'boardgame', _('桌游')
    Podcast = 'podcast', _('播客')
    FanFic = 'fanfic', _('网文')
    Performance = 'performance', _('演出')
    Exhibition = 'exhibition', _('展览')


class SubItemType(models.TextChoices):
    Season = 'season', _('剧集分季')
    Episode = 'episode', _('剧集分集')
    Version = 'version', _('版本')

# class CreditType(models.TextChoices):
#     Author = 'author', _('作者')
#     Translater = 'translater', _('译者')
#     Producer = 'producer', _('出品人')
#     Director = 'director', _('电影')
#     Actor = 'actor', _('演员')
#     Playwright = 'playwright', _('播客')
#     VoiceActor = 'voiceactor', _('配音')
#     Host = 'host', _('主持人')
#     Developer = 'developer', _('开发者')
#     Publisher = 'publisher', _('出版方')


class PrimaryLookupIdDescriptor(object):  # TODO make it mixin of Field
    def __init__(self, id_type):
        self.id_type = id_type

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        if self.id_type != instance.primary_lookup_id_type:
            return None
        return instance.primary_lookup_id_value

    def __set__(self, instance, id_value):
        if id_value:
            instance.primary_lookup_id_type = self.id_type
            instance.primary_lookup_id_value = id_value
        else:
            instance.primary_lookup_id_type = None
            instance.primary_lookup_id_value = None


class LookupIdDescriptor(object):  # TODO make it mixin of Field
    def __init__(self, id_type):
        self.id_type = id_type

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        return instance.get_lookup_id(self.id_type)

    def __set__(self, instance, value):
        instance.set_lookup_id(self.id_type, value)


# class ItemId(models.Model):
#     item = models.ForeignKey('Item', models.CASCADE)
#     id_type = models.CharField(_("源网站"), blank=False, choices=IdType.choices, max_length=50)
#     id_value = models.CharField(_("源网站ID"), blank=False, max_length=1000)


# class ItemCredit(models.Model):
#     item = models.ForeignKey('Item', models.CASCADE)
#     credit_type = models.CharField(_("类型"), choices=CreditType.choices, blank=False, max_length=50)
#     name = models.CharField(_("名字"), blank=False, max_length=1000)


# def check_source_id(sid):
#     if not sid:
#         return True
#     s = sid.split(':')
#     if len(s) < 2:
#         return False
#     return sid[0] in IdType.values()


class Item(PolymorphicModel):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    # item_type = models.CharField(_("类型"), choices=ItemType.choices, blank=False, max_length=50)
    title = models.CharField(_("title in primary language"), max_length=1000, default="")
    # title_ml = models.JSONField(_("title in different languages {['lang':'zh-cn', 'text':'', primary:True], ...}"), null=True, blank=True, default=list)
    brief = models.TextField(_("简介"), blank=True, default="")
    # brief_ml = models.JSONField(_("brief in different languages {['lang':'zh-cn', 'text':'', primary:True], ...}"), null=True, blank=True, default=list)
    genres = models.JSONField(_("分类"), null=True, blank=True, default=list)
    primary_lookup_id_type = models.CharField(_("isbn/cubn/imdb"), blank=False, null=True, max_length=50)
    primary_lookup_id_value = models.CharField(_("1234/tt789"), blank=False, null=True, max_length=1000)
    metadata = models.JSONField(_("其他信息"), blank=True, null=True, default=dict)
    cover = models.ImageField(upload_to=item_cover_path, default=DEFAULT_ITEM_COVER, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    edited_time = models.DateTimeField(auto_now=True)
    # parent_item = models.ForeignKey('Item', null=True, on_delete=models.SET_NULL, related_name='child_items')
    # identical_item = models.ForeignKey('Item', null=True, on_delete=models.SET_NULL, related_name='identical_items')
    # def get_lookup_id(self, id_type: str) -> str:
    #     prefix = id_type.strip().lower() + ':'
    #     return next((x[len(prefix):] for x in self.lookup_ids if x.startswith(prefix)), None)

    class Meta:
        unique_together = [['polymorphic_ctype_id', 'primary_lookup_id_type', 'primary_lookup_id_value']]

    def __str__(self):
        return f"{self.id}{' ' + self.primary_lookup_id_type + ':' + self.primary_lookup_id_value if self.primary_lookup_id_value else ''} ({self.title})"

    @classmethod
    def get_best_lookup_id(cls, lookup_ids):
        """ get best available lookup id, ideally commonly used """
        best_id_types = [IdType.ISBN, IdType.CUBN, IdType.ASIN, IdType.IMDB, IdType.Feed, IdType.TMDB_TVSeason]
        for t in best_id_types:
            if lookup_ids.get(t):
                return t, lookup_ids[t]
        return list(lookup_ids.items())[0]

    def update_lookup_ids(self, lookup_ids):
        # TODO
        # ll = set(lookup_ids)
        # ll = list(filter(lambda a, b: b, ll))
        # print(ll)
        pass

    METADATA_COPY_LIST = ['title', 'brief']  # list of metadata keys to copy from page to item

    @classmethod
    def copy_metadata(cls, metadata):
        return dict((k, v) for k, v in metadata.items() if k in cls.METADATA_COPY_LIST and v is not None)

    def merge_data_from_extenal_pages(self):
        """Subclass may override this"""
        lookup_ids = []
        for p in self.external_pages.all():
            lookup_ids.append((p.id_type, p.id_value))
            lookup_ids += p.other_lookup_ids.items()
            for k in self.METADATA_COPY_LIST:
                if not getattr(self, k) and p.metadata.get(k):
                    setattr(self, k, p.metadata.get(k))
            if not self.cover and p.cover:
                self.cover = p.cover
        self.update_lookup_ids(lookup_ids)

    def update_linked_items_from_extenal_page(self, page):
        """Subclass should override this"""
        pass


class ItemLookupId(models.Model):
    item = models.ForeignKey(Item, null=True, on_delete=models.SET_NULL, related_name='lookup_ids')
    id_type = models.CharField(_("源网站"), blank=True, choices=IdType.choices, max_length=50)
    id_value = models.CharField(_("源网站ID"), blank=True, max_length=1000)
    raw_url = models.CharField(_("源网站ID"), blank=True, max_length=1000, unique=True)

    class Meta:
        unique_together = [['id_type', 'id_value']]


class ExternalPage(models.Model):
    item = models.ForeignKey(Item, null=True, on_delete=models.SET_NULL, related_name='external_pages')
    id_type = models.CharField(_("IdType of the source site"), blank=False, choices=IdType.choices, max_length=50)
    id_value = models.CharField(_("Primary Id on the source site"), blank=False, max_length=1000)
    url = models.CharField(_("url to the page"), blank=False, max_length=1000, unique=True)
    cover = models.ImageField(upload_to=item_cover_path, default=DEFAULT_ITEM_COVER, blank=True)
    other_lookup_ids = models.JSONField(default=dict)
    metadata = models.JSONField(default=dict)
    scraped_time = models.DateTimeField(null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    edited_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['id_type', 'id_value']]

    def __str__(self):
        return f"{self.id}{':' + self.id_type + ':' + self.id_value if self.id_value else ''} ({self.url})"

    def update_content(self, page_data):
        self.other_lookup_ids = page_data.lookup_ids
        self.metadata = page_data.metadata
        if page_data.cover_image and page_data.cover_image_extention:
            self.cover = SimpleUploadedFile('temp.' + page_data.cover_image_extention, page_data.cover_image)
        self.scraped_time = timezone.now()
        self.save()

    @property
    def ready(self):
        return bool(self.metadata)

    def get_all_lookup_ids(self):
        d = self.other_lookup_ids.copy()
        d[self.id_type] = self.id_value
        d = {k: v for k, v in d.items() if bool(v)}
        return d

    def get_preferred_model(self):
        model = self.metadata.get('preferred_model')
        if model:
            m = ContentType.objects.filter(app_label='catalog', model=model.lower()).first()
            if m:
                return m.model_class()
            else:
                raise ValueError(f'preferred model {model} does not exist')
        return None

    def get_dependent_urls(self):
        ll = self.metadata.get('dependent_urls')
        return ll if ll else []

    def get_related_urls(self):
        ll = self.metadata.get('related_urls')
        return ll if ll else []