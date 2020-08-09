import scrapy
import json
import codecs
class Crawl(scrapy.Spider):
    name = "websosanh"
    sequence_number = 0
    def start_requests(self):
        yield scrapy.Request(url = "https://websosanh.vn/"  , callback= self.get_link_Categories)
    
    # Lấy link các danh mục 
    def get_link_Categories(self , response ) :
        for link in response.css("div.menu-main > ol.list-no-style > li.has-child"):
            yield scrapy.Request(url = link.css("a::attr(href)").get() , callback= self.get_link_product)
    # "Lấy link sản phẩm từ trang danh mục"
    def get_link_product(self , response):
        for link in response.css("div.page-content-wrap > ul.list-no-style > li.product-item"):
            yield scrapy.Request(url = link.css("a::attr(href)").get() , callback= self.parse)
        for link in response.css("div.pagination-wrap > ul.pagination > li"):
            yield scrapy.Request(url = link.css("a::attr(href)").get() , callback= self.get_link_product)
    # Thực hiện thu thập dữ liệu 
    # Hạn chế chưa lấy được hết giá so sánh ở trang vì do nó nằm ở trang 2 3 .
    def parse(self, response):
        specifications =[]
        prices = []
        compares = []
        for j in response.css("table.table-specifications tbody tr"):
            specifications.append(j.css("th::text").get() +" : " +j.css("td::text").get())
        for price in response.css("li.store-col"):
            prices.append("Giá : " +price.css("span.store-price::text").get() + "link : " + price.css("a::attr(href)").get())
        for compare in response.css("div.compare-info-row"):
            compares.append("Giá : " +compare.css("div.row-col div.compare-money::text").get()+ "   Link : " + compare.css("div.row-col h3.compare-info-name a::attr(href)").get())
                

        product = {
            "STT" : self.sequence_number ,
            "Tieude": response.css("h1.page-title::text").get(),
            "specifications" : specifications,
            "Description" : response.css("div.product-short-description >ul > li::text").getall(),
            "Content" : '\n'.join([
                ''.join(c.css('*::text').getall())
                    for c in response.css('div.product-description-content')
            ]),
            "Giá " : prices,
            "So sánh " : compares ,
            "Chuyên mục " : response.css("section.breadcrumbs > div.container > ol.list-no-style > li > a::text").getall()
            
        }

        self.sequence_number+=1
        with codecs.open("Output_websosanh2.json" , "a" , encoding= 'utf8') as content_file:
            json.dump(product , content_file ,indent= 4 ,ensure_ascii=False)