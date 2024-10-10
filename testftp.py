import ftplib
import inspect
import sys

hostname = "52.170.87.208"
username = "HcInstallations"
password = "gNPfcQa!Tw99diPy"

oursoftwares = ("HartnessConnectWeb","DeploymentManager","HartnessConnectManager","InsightCollector","InsightAdapter","OPCBroker","RetrospectServer")

filesfound = []

def getmylist(currentry):
  filesfound.append(currentry)
  print("how is this growing:\n"+str(filesfound))


myconx = ftplib.FTP_TLS(hostname, username, password, timeout=30)
myconx.prot_p()
# '200 Protection level set to P'
print("Current Directory")
trep = myconx.dir()
# print(str(type(trep)))
myconx.cwd("RetrospectServer")
print("\n\nRetrospectServer Directory")
myconx.dir(getmylist)

print("found "+str(len(filesfound))+" files")
print(filesfound)
print("what we need is ",end="")
for m2 in filesfound:
  if ".HCBackup" in m2:
    print(m2.split(" ")[-1])

print("\n\nTrying to grab the current RetrospectServer")
try:
  pass
  # with open('hll.HCBackup','wb') as file:
    # myconx.retrbinary('RETR RetrospectServer_24.09.0.1.HCBackup', file.write)
except Exception as exception:
  exc_type, exc_obj, exc_tb = sys.exc_info()
  errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
  print(errorstring)

print("\n\nAnd now we're closing the connection.")
myconx.close()

