import hashlib
import logging

from twisted.internet.defer import Deferred, DeferredList

import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.defer import mustbe_deferred
from scrapy.utils.log import failure_to_exc_info
from scrapy.utils.misc import arg_to_iter
from scrapy.utils.python import to_bytes
from scrapy.utils.request import request_fingerprint

logger = logging.getLogger(__name__)


class PokemonGalleryPipeline(ImagesPipeline):
    count = 0

    def process_item(self, item, spider):
        info = self.spiderinfo
        requests = arg_to_iter(self.get_media_requests(item, info))
        dlist = [self.process_pokemon_request(request, info) for request in requests]
        dfd = DeferredList(dlist, consumeErrors=1)
        return dfd.addCallback(self.item_completed, item, info)

    def process_pokemon_request(self, request, info):
        fingerprint = request_fingerprint(request)
        callback = request.callback or (lambda _: _)
        errorback = request.errback
        request.callback = None
        request.errback = None

        # Otherwise, wait for result
        wad = Deferred().addCallbacks(callback, errorback)
        info.waiting[fingerprint].append(wad)

        info.downloading.add(fingerprint)
        dfd = mustbe_deferred(self.media_to_download, request, info)
        dfd.addCallback(self._check_media_to_download, request, info)
        dfd.addBoth(self._cache_result_and_execute_waiters, fingerprint, info)
        dfd.addErrback(lambda f: logger.error(
            f.value, exc_info=failure_to_exc_info(f), extra={'spider': info.spider})
        )
        return dfd.addBoth(lambda _: wad)  # it must return wad at last

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            filename = image_url.split('/')[-1]
            yield scrapy.Request(image_url, dont_filter=True, meta={'pokemon_name':item['pokemon_name'], 'filename':filename})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        self.count += 1
        return item

    def file_path(self, request, response=None, info=None):
        # Modify the file path HERE to your own custom path 
        filename = request.meta['filename']
        return '%s/%s' % (request.meta['pokemon_name'], filename)
