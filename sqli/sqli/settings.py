### SCRAPY SETTINGS ###

BOT_NAME = 'sqli'

SPIDER_MODULES = ['sqli.spiders']
NEWSPIDER_MODULE = 'sqli.spiders'

ITEM_PIPELINES = [
    'sqli.pipelines.DuplicatesPipeline'
   ,'sqli.pipelines.SqlMapPipeline',
]

### SPIDER SETTINGS ###

DOMAIN = 'cotidiano.soeirosantos.com.br'

START_URLS = ['http://cotidiano.soeirosantos.com.br/']

### PATHS ###

SQLMAP_PATH = "/home/romulo/websec/sqlmap/sqlmap.py"

#output log path
OUTPUT_PATH = "/home/romulo/python/projects/websec/github/sqlitest/sqli/output"

CEWL_PATH = "" #"/home/romulo/websec/cewl/cewl/cewl.rb"

### BRUTE FORCE SETTINGS ###

#type of resources to try find by brute force
BF_EXTENSIONS = ("", ".php", ".html", ".htm")

#provide a directory to get third party files with common path locations
THIRD_PARTY_FILES_PATH = "" #"/home/romulo/python/projects/websec/github/sqlitest/sqli/wordlists"

### COMMAND TEMPLATES ###

#cewl default command template. customize it, but be careful ;)     
#FIXME: fix the ruby command interpreter
CEWL_CMD_TPL = "ruby-1.9.3-p194@cewl %(cewl_path)s %(domain)s"

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