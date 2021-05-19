import gspread
import os
import json
import datetime
import re
from oauth2client.service_account import ServiceAccountCredentials

class sheetContoroller:

    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']

    AKI_ID = os.environ.get("AKI_ID")
    RICO_ID = os.environ.get("RICO_ID")            
    #認証情報設定
    #ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
    credentials = ServiceAccountCredentials.from_json_keyfile_name('kakeibo-a67d7ffd9e01.json', scope)
    
    gc = gspread.authorize(credentials)

    #本日のdateTime
    today = datetime.datetime.today()


    #共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
    SPREADSHEET_KEY = '16iiM5Qp7Q1jS20YH3ydQV8YnPBBxcSXaPKT0g9nqQ1Y'

    def matchTest(self):
        content = 'ゲーム　200' 
        pattern1 = '.*?(\D+).*?'
        pattern2 = '.*?(\d+).*?'
        
        result1 = re.match(pattern1, content)
        result2 = re.match(pattern2, content)

        print(result1.group(1))
        print(result2.group(1))




    def recordSpending(self,string,user_id):

        print(string)

        pattern1 = '.*?(\D+).*?'
        pattern2 = '.*?(\d+).*?'
        
        try:
            what = re.match(pattern1, string).group(1)
        except:
            what = None

        amt = re.match(pattern2, string).group(1)

        print(what)
        print(amt)

        #金額が書かれていない場合、例外を投げる
        if amt == None:
            raise ValueError("error!")
    
    
        #共有設定したスプレッドシートのシート1を開く
        workbook = self.gc.open_by_key(self.SPREADSHEET_KEY)
        
        if user_id == self.AKI_ID:
            worksheet = workbook.worksheet('あき支出')
        if user_id == self.RICO_ID:
            worksheet = workbook.worksheet('りこ支出')

        i = 3
        amtCell = worksheet.cell(i, 2)
        while len(amtCell.value)>0:#セルに何か書き込まれている場合
            i += 1
            amtCell = worksheet.cell(i,2)
        
        whatCell = worksheet.cell(i,1)
        dateCell = worksheet.cell(i,3)

        #各種情報を書き込む
        if what != None:
            worksheet.update_cell(whatCell.row,whatCell.col,what)
        worksheet.update_cell(amtCell.row,amtCell.col,amt)
        worksheet.update_cell(dateCell.row,dateCell.col,self.today.strftime("%Y/%m/%d"))

    def recordDebt(self,string,user_id):

        print(string)

        pattern1 = '.*?(\D+).*?'
        pattern2 = '.*?(\d+).*?'
        
        try:
            what = re.match(pattern1, string).group(1)
        except:
            what = None

        amt = re.match(pattern2, string).group(1)

        print(what)
        print(amt)

        #金額が書かれていない場合、例外を投げる
        if amt == None:
            raise ValueError("error!")
    
    
        #共有設定したスプレッドシートのシート1を開く
        workbook = self.gc.open_by_key(self.SPREADSHEET_KEY)
        
        if user_id == self.AKI_ID:
            worksheet = workbook.worksheet('あき借金')
        if user_id == self.RICO_ID:
            worksheet = workbook.worksheet('りこ借金')

        i = 3
        amtCell = worksheet.cell(i, 2)
        while len(amtCell.value)>0:#セルに何か書き込まれている場合
            i += 1
            amtCell = worksheet.cell(i,2)
        
        whatCell = worksheet.cell(i,1)
        dateCell = worksheet.cell(i,3)

        #各種情報を書き込む
        if what != None:
            worksheet.update_cell(whatCell.row,whatCell.col,what)
        worksheet.update_cell(amtCell.row,amtCell.col,amt)
        worksheet.update_cell(dateCell.row,dateCell.col,self.today.strftime("%Y/%m/%d"))


    def outPutQuery(self,user_id):
        #共有設定したスプレッドシートのシート1を開く
        workbook = self.gc.open_by_key(self.SPREADSHEET_KEY)
        
        if user_id == self.AKI_ID:
            worksheet = workbook.worksheet('あき照会')
        if user_id == self.RICO_ID:
            worksheet = workbook.worksheet('りこ照会')

        debtAmt = worksheet.cell(5,1).value

        str = '今月は'+worksheet.cell(2,1).value+'円使ったよ！\n'+ debtAmt +"必要があるよ！"
        
        return str
    
if __name__ == '__main__':
    print(sheetContoroller.outPutQuery(self=sheetContoroller,user_id='U80822b41a172aa5455333e78afa11079'))