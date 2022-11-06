# import ftplib
import urllib.request
import ftplib

class FTPServer():

    def __init__(self, user, passwd, host) -> None:
        self.user = user
        self.passwd = passwd
        self.host = host

    # def _connect(self) -> ftplib.FTP:
    #     ftp = ftplib.FTP(self.host)
    #     ftp.login(self.user,self.passwd)
    #     return ftp
    def upload_file(self,filename):
        ftp = ftplib.FTP(self.host)
        ftp.login(self.user,self.passwd)
        ftp.cwd('\home')
        with open(f"./uploads/{filename}","rb") as file:
            ftp.storbinary(f'STOR {filename}', file)     # send the file
        ftp.quit()

    def get_file(self, file,dest):
        try:
            urllib.request.urlretrieve(f'ftp://{self.user}:{self.passwd}@10.0.86.73/home/{file}', dest)
        except:
            open(dest,"w").write("")
    
    def list_files(self):
        ftp = ftplib.FTP(self.host)
        ftp.login(self.user,self.passwd)
        # change dir
        ftp.cwd('\home') 

        # list files
        data = ftp.nlst()
        ftp.quit()

        return data