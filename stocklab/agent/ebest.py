import configparser
import win32com.client
import pythoncom 

class XASession:
    login_state = 0
    def OnLogin(self,code,msg):
        if code =="0000":
            print(code,msg)
            XASession.login_state = 1
        else:
            print(code,msg)
        # 로그인 시도 후 호출, code가 0000이면 성공!
    def OnDisconnect(self):
        print("Session disconntected")
        XASession.login_state = 0
        # 서버와 연결이 끊어지면 발생

class EBest:
    def __init__(self, mode = None):

        """
        config.ini 파일을 로드해 사용자, 서버 정보 저장
        query_cnt는 10분당 200개의 TR 수행을 관리하기 위한 리스트
        xa_session_client는 XASession 객체
        :param mode:str - 모의서버는 DEMO 실서버는 PROD로 구분
        """
        if mode not in ["PROD", "DEMO"]:
            raise Exception("Need to run_mode(PROD or DEMO)")
        
        run_mode = "EBEST_"+mode
        config = configparser.ConfigParser()
        config.read('conf/config.ini')
        self.user = config[run_mode]['user']
        self.passwd = config[run_mode]['password']
        self.cert_passwd = config[run_mode]['cert_passwd']
        self.host = config[run_mode]['host']
        self.port = config[run_mode]['port']
        self.account = config[run_mode]['account']

        self.xa_session_client = win32com.client.DispatchWithEvents("XA_Session.XASession", XASession)

    def login(self):
        self.xa_session_client.ConnectServer(self.host,self.port)
        self.xa_session_client.Login(self.user,self.passwd,self.cert_passwd,0,0)
        while XASession.login_state == 0:
            pythoncom.PumpWaitingMessages()
        
    def logout(self):
        result = self.xa_session_client.Logout()
        if result:
            XASession.login_state = 0
            self.xa_session_client.DisconnectServer()

class XAQuery:
    RES_PATH = "C:\\eBEST\\xingAPI\\Res\\"
    tr_run_state = 0

    def OnReceiveData(self, code):
        print("OnReceiveData",code)
        XAQuery.tr_run_state = 1
    
    def OnReceiveMessage(self,error,code,message):
        print("OnReceiveMessage",error,code,message)
    
