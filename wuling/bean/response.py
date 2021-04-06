class Response:
    def __init__(self):
        self.encoding = 'UTF-8'
        self.status_code=200
        self.status_desc=''
        self.header = {'Content-Type': 'application/json;charset=UTF-8'}
        self.cookies= {}
        self.body = ''