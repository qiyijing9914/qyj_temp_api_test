class Request:
    def __init__(self):
        '所有员工的基类'
        self.method = ''
        self.protocal = ''
        self.ip = ''
        self.port = 0
        self.uri = ''
        self.query = {}
        self.encoding = 'UTF-8'
        self.header = {}
        self.cookies={}
        self.body = ''



    def to_string(self):
        if self.query != '':
            print('%s %s://%s:%d%s?%s HTTP/1.1'%(self.method,self.protocal,self.ip,self.port,self.uri,self.query))
        else:
            print('%s %s://%s:%d%s HTTP/1.1'%(self.method,self.protocal,self.ip,self.port,self.uri))
        print(self.header)
        print(self.cookies)
        print(self.body)
