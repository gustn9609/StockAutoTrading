import configparser
import win32com.client
import pythoncom 
from datetime import datetime
import time

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

    QEURY_LIMIT_10MIN = 200
    LIMIT_SECONDS = 600 

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
        self.query_cnt = []

    def _execute_query(self, res, in_block_name, out_block_name,*out_fields, **set_fields)::
        """
        TR 코드를 실행하기 위한 메서드
        :param res:str 리소스 이름(TR)
        :param in_block_name:str 인 블록 이름
        :param out_block_name:str 아웃블록 이름
        :param in_params:list 출력 필드 리스트
        :param in_params:dict 인 블록에 설정할 필드 딕셔너리
        :return result:list 결과를 list에 담아 변환
        """
        time.sleep(1)
        print("current query cnt:", len(self.query_cnt))
        print(res, in_block_name, out_block_name)
        while len(self.query_cnt) >= EBest.QEURY_LIMIT_10MIN:
            time.sleep(1)
            print("waiting for execute query... current query cnt:", len(self.query_cnt))
            print(res, in_block_name, out_block_name)
            while len(self.query_cnt) >= EBest.QEURY_LIMIT_10MIN:
                time.sleep(1)
                print("waiting for execute query... current query cnt:", len(self.query_cnt))
                self.query_cnt = list(filter(lambda x : (datetime.today() - x).total_seconds() < EBest.LIMIT_SECONDS, self.query_cnt))

            xa_query = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery",XAQuery)
            xa_query.LoadFromResFile(XAQuery.RES_PATH + res + ".res")
            
            #in_block_name 셋팅
            


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
    
