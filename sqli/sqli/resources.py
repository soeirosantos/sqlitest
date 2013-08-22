from sqli.settings import CEWL_PATH, DOMAIN, BF_EXTENSIONS

class ResourceHandler(object):
    '''
        Discover resources based on cewl, url provided by user, 
        third party files and brute force
    '''

    def __call_cewl(self, domain):
        ''' invokes cewl script and returns stdout like a file words '''
        p = subprocess.Popen(CEWL_PATH + domain, shell=True, stdout=subprocess.PIPE)
        return p.stdout

    def get_wordlist_file(self, domain):
        ''' use this function for get a file with a list of words (expected one word by line) '''   
        return self.__call_cewl(domain)

    def __bruteforce_path(self, words, maxlength):
        import itertools
        return ['/'.join(candidate)
            for candidate in itertools.chain.from_iterable(itertools.product(words, repeat=i)
            for i in range(1, maxlength + 1))]

    def generate_start_urls(self, domain):
        import urlparse
        domain = urlparse.urlparse(domain, scheme='http').geturl()
        wordlist = [ line.rstrip()
                     for line in self.get_wordlist_file(domain).readlines() ]
        return [domain+'/'+path+extension 
                for path in self.__bruteforce_path(wordlist, 2) 
                for extension in BF_EXTENSIONS]

if __name__ == '__main__':
    print generate_start_urls('http://cotidiano.soeirosantos.com.br')