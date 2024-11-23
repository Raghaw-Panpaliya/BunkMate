from scrapy import Spider
from scrapy.http import FormRequest


class SimpleLoginSpider(Spider):
    name = 'simple_login'

    def start_requests(self):
        login_url = 'https://kp.christuniversity.in/KnowledgePro/StudentLogin.do'
        return FormRequest(login_url,
                            formdata={'userName': 2241240, 'password': 15051533},
                            callback=self.start_scraping)

    def start_scraping(self, response):
        print(response.text)
        pass

if __name__ == "__main__":
    kp = SimpleLoginSpider(Spider)
    kp.start_requests()