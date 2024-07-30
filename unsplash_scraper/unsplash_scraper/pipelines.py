# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv

class UnsplashScraperPipeline:
    def open_spider(self, spider):
        self.file = open('images_data.csv', 'w', newline='')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['image_url', 'image_paths', 'name', 'category'])

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        self.writer.writerow([item['image_url'], ','.join(item.get('image_paths', [])), item['name'], item['category']])
        return item