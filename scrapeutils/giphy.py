from typing import Optional

import giphy_client
from giphy_client.rest import ApiException
from random import randint
from utils.utility import slugify
from scrapeutils import scraper


def get_gif(query: str, start: int = 0, end: int = 25) -> Optional[str]:
    # create an instance of the API class
    api_instance = giphy_client.DefaultApi()
    api_key = 'yhXEGvoYHxiYojMrFc82Dp1wcgCFnMHX'  # str | Giphy API Key.
    limit = 25  # int | The maximum number of records to return. (optional) (default to 25)
    offset = 0  # int | An optional results offset. Defaults to 0. (optional) (default to 0)
    rating = 'g'  # str | Filters results by specified rating. (optional)
    lang = 'en'  # str | Specify default country for regional content; use a 2-letter ISO 639-1 country code. See list of supported languages <a href = \"../language-support\">here</a>. (optional)
    fmt = 'gif'  # str | Used to indicate the expected response format. Default is Json. (optional) (default to json)

    try:
        response = api_instance.gifs_search_get(api_key, query, limit = limit, offset = randint(start, end), fmt = fmt,
                                                rating = rating, lang = lang)
        gif_id = response.data[0]
        gif_url = gif_id.images.original.url
        gif_filename = slugify(query) + ".gif"
        scraper.scrape_gif(gif_url, gif_filename)
        return gif_filename

    except ApiException as e:
        print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)
        return None
