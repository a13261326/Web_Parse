from itemadapter import ItemAdapter
import scrapy
from scrapy.pipelines.images import ImagesPipeline


class CastoramaPipeline:
    def process_item(self, item, spider):
        return item


class CastoramaPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photos'] = [itm[1] for itm in results if itm[0]]
        return item


    def file_path(self, request, response=None, info=None):
        filename = u'{0}/{1}'.format(info.spider.query, request.url.split('/')[-1])
        return filename
