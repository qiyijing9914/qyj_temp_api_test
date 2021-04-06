import codecs
import configparser
import os

configpath=os.path.join(os.path.split(os.path.realpath(__file__))[0],'allConfig.ini')

class ReadConfig:
    def __init__(self):
        fd = open(configpath)
        data = fd.read()

        #remove BOM
        if data[:3]==codecs.BOM_UTF8:
            data = data[3:]
            file=codecs.open(configpath,'w')
            file.write(data)
            file.close()
        fd.close()

        self.cf = configparser.ConfigParser()
        self.cf.read(configpath)

    def get_db(self,name):
        vaiue=self.cf.get('DATABASE',name)
        return vaiue

if __name__ == '__main__':
    x=ReadConfig()
    print(x.get_db('host'))

