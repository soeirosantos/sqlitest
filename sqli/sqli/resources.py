from sqli.settings import *

class BruteForceResources(object):
    '''
        Discover resources based on cewl, url provided by user, 
        third party files and brute force
    '''

    def __load_wordlists_from_cewl(self, domain):
        ''' invokes cewl script and returns stdout like a file words '''
        words = []
        if CEWL_PATH:
            import subprocess
            cewl_cmd = CEWL_CMD_TPL %  {"cewl_path" : CEWL_PATH, "domain" : domain}
            p = subprocess.Popen(cewl_cmd
                                ,shell=True
                                ,stdout=subprocess.PIPE)
            words = p.stdout.readlines()
        return words
    
    def __load_wordlists_from_files(self):
        words = []
        if THIRD_PARTY_FILES_PATH:
            import glob
            files = glob.glob(THIRD_PARTY_FILES_PATH+"/*")
            for file_ in files:
                words = words + open(file_).readlines()
        return words

    def __load_wordlists(self, domain):
        return self.__load_wordlists_from_cewl(domain) + self.__load_wordlists_from_files()


    def __bruteforce_path(self, words, depth):
        import itertools
        return ['/'.join(candidate)
            for candidate in itertools.chain.from_iterable(itertools.product(words, repeat=i)
            for i in range(1, depth + 1))]

    def generate_urls(self):
        if "http://" not in DOMAIN:
            domain_ = "http://"+DOMAIN
        else:
            domain_ = DOMAIN    

        wordlist = [line.replace("\n", "") for line in self.__load_wordlists(domain_) ]
        
        return [domain_+'/'+path+extension 
                for path in self.__bruteforce_path(wordlist, 2) 
                for extension in BF_EXTENSIONS]

if __name__ == '__main__':
    pass