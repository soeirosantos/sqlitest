BOT_NAME = 'sqli'

SPIDER_MODULES = ['sqli.spiders']
NEWSPIDER_MODULE = 'sqli.spiders'

ITEM_PIPELINES = [
    'sqli.pipelines.DuplicatesPipeline'
   ,'sqli.pipelines.SqlMapPipeline',
]

DOMAIN = 'cotidiano.soeirosantos.com.br'

SQLMAP_PATH = "/home/romulo/websec/sqlmap/sqlmap.py"

#output log path
OUTPUT_PATH = "/home/romulo/python/projects/websec/sqli/output"

CEWL_PATH = "cewl.rb"

#type of resources to find by brute force
BF_EXTENSIONS = ("", ".php", ".html", ".htm")

#provide a directory to get third party files with common path locations
THIRD_PARTY_FILES_PATH = ""

#USER_AGENT = 'sqli (+http://www.yourdomain.com)'
