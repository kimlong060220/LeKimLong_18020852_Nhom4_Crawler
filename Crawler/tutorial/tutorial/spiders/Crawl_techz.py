import scrapy
import json
import codecs
import string
class Crawl(scrapy.Spider):
    name = "thethao"
    sequence_number = 0
    start_urls = ["https://www.techz.vn"]
        
    def parse(self, response):
        # Đây là điều kiện để được thu thập là trang mở được và là trang có content là article 
        if response.status == 200 and response.css('meta[property="og:type"]::attr("content")').get() == 'article':
            article = {
                "Link" : response.url, 
                "STT" : self.sequence_number,
                "Tieude": response.css("div.title-detail h1::text").get(),
                "Tóm tắt" : response.css("div.sapo-detail h2::text").get(),
                "Thời gian": response.css("div.mr-auto span.post-time::text").get(),
                "keywork" :  [ 
                    k.strip() for k in response.css('meta[name="keywords"]::attr("content")').get().split(',')
                ],
                # "Tags" :List_tags,
                "Noi dung": response.css("div.detail-text p::text").getall(),
                "Tác giả" : response.css("div.mr-auto a::text").get(),
                "Nguồn": response.css("div.mr-auto span.mr-3 a::text").get()
            }

            self.sequence_number+=1
            with codecs.open("Output_techz.json" , "a" , encoding= 'utf8') as content_file:
                json.dump(article , content_file ,indent= 4 ,ensure_ascii=False)
        yield from response.follow_all(css='a[href^="https://www.techz.vn/"]::attr(href), a[href^="/"]::attr(href)', callback=self.parse)