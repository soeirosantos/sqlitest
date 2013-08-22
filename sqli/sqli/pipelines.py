from scrapy.exceptions import DropItem
from sqli.settings import SQLMAP_PATH, OUTPUT_PATH, SQLMAP_CMD_TPL

class DuplicatesPipeline(object):

    def __init__(self):
        self.candidate_injection_points_cache = set()

    def process_item(self, item, spider):
        identifier = item.get_id()
        if identifier in self.candidate_injection_points_cache:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.candidate_injection_points_cache.add(identifier)
            return item

class SqlMapPipeline(object):
    
    def process_item(self, item, spider):
        import subprocess
	
        cmd = self.get_command(item)
        p = subprocess.Popen(cmd, shell=True)

        return item

    def get_command(self, item):
        return SQLMAP_CMD_TPL % {"target" : self.get_target(item)
                         ,"file_name"    : self.get_log_file_name(item)
                         ,"sqlmap_path"  : SQLMAP_PATH
                         ,"output_path"  : OUTPUT_PATH}

    def get_target(self, item):
        '''
            returns the value of sqlmap -u parameter and related parameters depending the HTTP method
        '''
        return self.__get_target_tpl(item["form_method"])  % {"form_action":item["form_action"], "input_name":item["input_name"]}
        
    def __get_target_tpl(self, method):
        if method == "get":
            return "%(form_action)s?%(input_name)s=foo"
        else:
            return "%(form_action)s --data=\"%(input_name)s=foo\""

    def get_log_file_name(self, item):
        '''
            returns a log file name for the corresponding item
        '''
        import urlparse
        return urlparse.urlparse(item["form_action"]).path.replace("/", "_").replace(".", "_")+"_"+item["input_name"]+".log"