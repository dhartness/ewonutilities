import ftplib
import inspect
import sys

hostname = "52.170.87.208"
username = "HcInstallations"
password = "gNPfcQa!Tw99diPy"

myconx = ftplib.FTP_TLS(hostname, username, password)
myconx.prot_p()
# '200 Protection level set to P'
print("Current Directory")
myconx.dir()
myconx.cwd("RetrospectServer")
print("\n\nRetrospectServer Directory")
myconx.dir()
print("\n\nTrying to grab the current RetrospectServer")
try:
  with open('hll.HCBackup','wb') as file:
    myconx.retrbinary('RETR RetrospectServer_24.09.0.1.HCBackup', file.write)
except Exception as exception:
  exc_type, exc_obj, exc_tb = sys.exc_info()
  errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
  print(errorstring)

print("\n\nAnd now we're closing the connection.")
myconx.close()

