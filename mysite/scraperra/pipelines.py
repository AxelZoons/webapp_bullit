# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import xlsxwriter


class ScraperraPipeline:

    def __init__(self):
        self.wb = None
        self.ws = None
        self.current_row_index = 0

    def process_item(self, item, spider):

        adapter = ItemAdapter(item)
        d = adapter.asdict()
        cell_format = self.wb.add_format({'bold': True, 'bottom': 2})

        if self.current_row_index == 0: #write header
            for col, value in enumerate(d.keys()):
                self.ws.write(self.current_row_index, col, value, cell_format)

        data = d.values()

        for col, value in enumerate(data):
            self.ws.write(self.current_row_index+1, col, value)

        self.current_row_index += 1

        return item

    def open_spider(self, spider):
        spider.logger.info('IN OPEN SPIDER')
        self.wb = xlsxwriter.Workbook('output.xlsx')
        self.ws = self.wb.add_worksheet()

    def close_spider(self, spider):
        spider.logger.info('IN CLOSE SPIDER')
        self.ws.autofit()
        self.wb.close()