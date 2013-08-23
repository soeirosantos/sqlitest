### SCRAPY SETTINGS ###

BOT_NAME = 'sqli'

SPIDER_MODULES = ['sqli.spiders']
NEWSPIDER_MODULE = 'sqli.spiders'

ITEM_PIPELINES = [
    'sqli.pipelines.DuplicatesPipeline'
   ,'sqli.pipelines.SqlMapPipeline',
]

### SPIDER SETTINGS ###

DOMAIN = 'domain.to.test.com'

START_URLS = ['http://domain.to.test.com']

### PATHS ###

SQLMAP_PATH = "/path/to/sqlmap/sqlmap.py"

#output log path
OUTPUT_PATH = "/path/to/output/logs/"

CEWL_PATH = "" #"/path/to/cewl/cewl.rb" # keep it commented if you don't want use cewl

### BRUTE FORCE SETTINGS ###

#type of resources to try find by brute force
BF_EXTENSIONS = ("", ".php", ".html", ".htm")

#provide a directory to get third party files with common path locations
THIRD_PARTY_FILES_PATH = "" #"/path/to/third/party/wordlists"

### COMMAND TEMPLATES ###

#cewl default command template. customize it, but be careful ;)     
CEWL_CMD_TPL = "ruby %(cewl_path)s %(domain)s"

#sqlmap default command template. customize it, but be careful ;)       
SQLMAP_CMD_TPL = 'nohup python %(sqlmap_path)s          \
                 -u %(target)s                   \
                 --technique=B                   \
                 --batch                         \
                 --level=5                       \
                 --risk=4                        \
                 --threads=10                    \
                 > %(output_path)s/%(file_name)s \
                 2>&1 &'

#USER_AGENT = 'sqli (+http://www.yourdomain.com)'