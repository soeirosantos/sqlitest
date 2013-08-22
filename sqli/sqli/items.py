from scrapy.item import Item, Field


class CandidateInjectionPoint(Item):
    form_method = Field()
    form_action = Field()
    input_name = Field()
    input_id = Field()

    def get_id(self):
        '''
            this id is used as unique identifier for [action / input name] pairs
            (or param in query string cases)
        '''
        return "%s:%s" % (self["form_action"], self["input_name"])
