from django.conf import settings
from catalog.common import *
from .douban import *
from catalog.movie.models import *
from catalog.tv.models import *
import logging


logger = logging.getLogger(__name__)


@SiteList.register
class IMDB(AbstractSite):
    ID_TYPE = IdType.IMDB
    URL_PATTERNS = [r'\w+://www.imdb.com/title/(tt\d+)']
    WIKI_PROPERTY_ID = '?'

    @classmethod
    def id_to_url(self, id_value):
        return "https://www.imdb.com/title/" + id_value + "/"

    def scrape(self):
        self.scraped = False
        api_url = f"https://api.themoviedb.org/3/find/{self.id_value}?api_key={settings.TMDB_API3_KEY}&language=zh-CN&external_source=imdb_id"
        res_data = BasicDownloader(api_url).download().json()
        if 'movie_results' in res_data and len(res_data['movie_results']) > 0:
            url = f"https://www.themoviedb.org/movie/{res_data['movie_results'][0]['id']}"
        elif 'tv_results' in res_data and len(res_data['tv_results']) > 0:
            url = f"https://www.themoviedb.org/tv/{res_data['tv_results'][0]['id']}"
        elif 'tv_season_results' in res_data and len(res_data['tv_season_results']) > 0:
            # this should not happen given IMDB only has ids for either show or episode
            tv_id = res_data['tv_season_results'][0]['show_id']
            season_number = res_data['tv_season_results'][0]['season_number']
            url = f"https://www.themoviedb.org/tv/{tv_id}/season/{season_number}/episode/{episode_number}"
        elif 'tv_episode_results' in res_data and len(res_data['tv_episode_results']) > 0:
            tv_id = res_data['tv_episode_results'][0]['show_id']
            season_number = res_data['tv_episode_results'][0]['season_number']
            episode_number = res_data['tv_episode_results'][0]['episode_number']
            if season_number == 0:
                url = f"https://www.themoviedb.org/tv/{tv_id}/season/{season_number}/episode/{episode_number}"
            elif episode_number == 1:
                url = f"https://www.themoviedb.org/tv/{tv_id}/season/{season_number}"
            else:
                raise ParseError(self, "IMDB id matching TMDB but not first episode, this is not supported")
        else:
            raise ParseError(self, "IMDB id not found in TMDB")
        tmdb = SiteList.get_site_by_url(url)
        pd = tmdb.scrape()
        pd.metadata['preferred_model'] = tmdb.DEFAULT_MODEL.__name__
        return pd