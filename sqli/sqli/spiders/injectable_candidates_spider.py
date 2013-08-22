from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.http import Request, FormRequest
from sqli.items import CandidateInjectionPoint
from urlparse import *
from sqli.settings import DOMAIN, START_URLS
from sqli.resources import BruteForceResources

class SelectCandidateInjectionPoint(BaseSpider):
    name = 'sqli_spider'
    allowed_domains = [DOMAIN]
    start_urls = START_URLS + BruteForceResources().generate_urls()

    def parse(self, response):
        content_type = response.headers['Content-Type']        
        
        if response.status not in (401, 404, 500) and 'text/html' in content_type:
            hxs = HtmlXPathSelector(response)
            
            for form in hxs.select("//form"):
                for input in form.select(".//input"):
                    
                    method = self.extract_one(form.select("@method")) or 'GET'
                    action = self.extract_one(form.select("@action"))
                    name = self.extract_one(input.select("@name"))
                    input_id = self.extract_one(input.select("@id"))

                    if name and action:
                        absolute_action = self.parse_url(action, response)["url"]
                        
                        yield CandidateInjectionPoint(
                                                form_method=method
                                               ,form_action=absolute_action
                                               ,input_name=name
                                               ,input_id=input_id
                                            )

            for a_tag in hxs.select('//a[contains(@href, "?")]'):
                
                href = self.extract_one(a_tag.select('@href'))

                if href:
                    href_parts = self.parse_url(href, response)
                    absolute_url = href_parts["url"]
                    for param_name in href_parts["params"].keys():
                        
                        yield CandidateInjectionPoint(
                                                form_method='GET'
                                               ,form_action=absolute_url
                                               ,input_name=param_name
                                            )

            links_to_follow = hxs.select("//a/@href").extract()

            for link in links_to_follow:
                link_parts = self.parse_url(link, response)
                absolute_url = link_parts["url"]
                
                yield Request(absolute_url, callback=self.parse)

            has_forms_to_follow = hxs.select("//form")

            if has_forms_to_follow:
                yield FormRequest.from_response(response, callback=self.parse)

    def extract_one(self, node):
        if node:
            if isinstance(node, list):
                if len(node) == 1:
                    return node[0].extract()
                else:
                    raise Exception("extract_one expects nodes with one element")
            else:
                return node.extract()

    def parse_url(self, url, response):
        if url:
            parsed = urlparse(url)
            url = urljoin(response.url, parsed.path)
            params = parse_qs(parsed.query)

            return {"url":url, "params":params}