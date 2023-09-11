# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class TutorialPipeline:
    def process_item(self, item, spider):
        return item

class MultiFilePipeline:
    def open_spider(self, spider):
        self.file_handles = {}

    def close_spider(self, spider):
        for file_handle in self.file_handles.values():
            file_handle.close()

    def process_item(self, item, spider):
        start_url = item.get('start_url', 'unknown')
        file_name = f"D:\DATA\{start_url.replace('://', '_').replace('/', '_')}.html"  # Changed to .txt for plain text
        
        with open(file_name, 'w', encoding='utf-8') as f:
            data_content = item.get('datacontent', '')
            f.write(data_content)
        return item
