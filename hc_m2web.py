import inspect
import json
import requests
import sys
import time

ew_devid = "f4a5717d-9942-41d7-8d67-11ecafc6e66c"
ew_usern = "dthompson"
ew_passw = "gettingvizzy4it"
ew_sessn = ""


logmein = "https://m2web.talk2m.com/t2mapi/login?t2maccount=Hartness&t2musername="+ew_usern+"&t2mpassword="+ew_passw+"&t2mdeveloperid="+ew_devid
connectionsults = requests.get(logmein)
ew_sessn = json.loads(connectionsults.content.decode())["t2msession"]


getdaewons = "https://m2web.talk2m.com/t2mapi/getewons?t2maccount=Hartness&t2musername="+ew_usern+"&t2mpassword="+ew_passw+"&t2mdeveloperid="+ew_devid
ewonssults = requests.get(getdaewons)
# print(ewonssults)
ewonssults = json.loads(ewonssults.content.decode())
ewonlist = ewonssults["ewons"]

print(" Online\n|------|")
for anewon in ewonlist:
  if anewon["status"] == "online":
    print(str(anewon["description"]+" - "+anewon["name"]))
    thisewonssysinfo = "https://m2web.talk2m.com/t2mapi/get/"+anewon["name"]+"/proxy/10.11.104.11/WebView/SystemInfoPartial&t2maccount=Hartness&t2musername="+ew_usern+"&t2mpassword="+ew_passw+"&t2mdeveloperid="+ew_devid
    try:
      tryingtoreach = requests.get(thisewonssysinfo,timeout=5.0)
      with open(anewon["name"]+"_SysInfoPart.html","w") as fp:
        fp.write(tryingtoreach.content.decode())
    except Exception as exception:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
      print(errorstring)

# str(tryingtoreach)
# '<Response [200]>'

# ################################################################################
# 0: import requests                                                                                                    
# 1: logmein = "https://m2web.talk2m.com/t2mapi/login?t2maccount=Hartness&t2musername=dthompson&t2mpassword=gettingvizzy
# 2: qrsults = None                                                                                                     
# 3: qrsults = requests.get(logmein)                                                                                    
# 4: qrsults                                                                                                            
# 5: type(qrsults)                                                                                                      
# 6: print(qrsults.url)                                                                                                 
# 7: print(qrsults.status_code)                                                                                         
# 8: print(qrsults.headers)                                                                                             
# 9: print(qrsults.encoding)                                                                                            
# 10: qrsults.elapsed                                                                                                   
# 11: qrsults.content                                                                                                   
# 12: logmein = "https://m2web.talk2m.com/t2mapi/login?t2maccount=Hartness&t2musername=dthompson&t2mpassword=gettingvizz
# 13: qrsults = requests.get(logmein)                                                                                   
# 14: qrsults.status_code                                                                                               
# 15: qrsults.content                                                                                                   
# 16: showsessionwork = "https://m2web.talk2m.com/t2mapi/getaccountinfo?tm2session=e004689d28ccb5505ac90006e2229c6a"    
# 17: qrsults = requests.get(showsessionwork)                                                                           
# 18: qrsults.content                                                                                                  
# │18: qrsults.content                                                                                                   
# 19: showsessionwork = "https://m2web.talk2m.com/t2mapi/getaccountinfo?tm2session=e004689d28ccb5505ac90006e2229c6a&t2md
# 20: qrsults = requests.get(showsessionwork)                                                                           
# 21: qrsults.content                                                                                                   
# 22: showsessionwork = "https://m2web.talk2m.com/t2mapi/getaccountinfo?t2maccount=Hartness&t2musername=dthompson&t2mpas
# 23: qrsults = requests.get(showsessionwork)                                                                           
# 24: qrsults.content                                                                                                   
# 25: ewonwork = "https://m2web.talk2m.com/t2mapi/getewons?t2maccount=Hartness&t2musername=dthompson&t2mpassword=getting
# 26: qrsults = requests.get(ewonwork)                                                                                  
# 27: qrsults.content                                                                                                   
# 28: for j in qrsults.content:                                                                                         
# 29:   print(j)                                                                                                        
# 30: qrsults.content
# b'
# {"success":true,"ewons":[
# {"id":1352989,"encodedName":"H.00262-3","status":"offline","customAttributes":["","",""],"lanDevices":[],"ewonServices":[],"name":"H.00262-3","description":"Kellogg\'s Battle Creek, MI","m2webServer":"us-e-1.m2web.talk2m.com"},
# {"id":860715,"encodedName":"H.00272","status":"offline","customAttributes":["","",""],"lanDevices":[],"ewonServices":[],"name":"H.00272","description":"Colgate Palmolive - Hodges, SC","m2webServer":"us-e-1.m2web.talk2m.com"},
# {"id":790000,"encodedName":"ITW+Hartness+HQ","status":"online","customAttributes":["","",""],"lanDevices":[],"ewonServices":[],"name":"ITW Hartness HQ","description":"HartnessCONNECT R&D Lab","m2webServer":"us-e-1.m2web.talk2m.com"},
# {"id":1495203,"encodedName":"Kellogg%27s+Rome+Ewon","status":"offline","customAttributes":["","",""],"lanDevices":[],"ewonServices":[],"name":"Kellogg\'s Rome Ewon","description":"","m2webServer":"us-e-1.m2web.talk2m.com"},
# {"id":1656693,"encodedName":"W28450","status":"offline","customAttributes":["","",""],"lanDevices":[],"ewonServices":[],"name":"W28450","description":"Zobele (W28450)","m2webServer":"us-e-1.m2web.talk2m.com"},
# {"id":1810884,"encodedName":"W28455","status":"offline","customAttributes":["","",""],"lanDevices":[],"ewonServices":[],"name":"W28455","description":"HVR - W28455","m2webServer":"us-e-1.m2web.talk2m.com"},
# {"id":1787215,"encodedName":"W28456","status":"offline","customAttributes":["","",""],"lanDevices":[],"ewonServices":[],"name":"W28456","description":"Clorox - W28456","m2webServer":"us-e-1.m2web.talk2m.com"},
# {"id":884819,"encodedName":"W4510051","status":"online","customAttributes":["","",""],"lanDevices":[],"ewonServices":[],"name":"W4510051","description":"KDP - Jacksonville, FL","m2webServer":"us-e-1.m2web.talk2m.com"},
# ...
# }
# type(qrsults.content)
# <class 'bytes'>
# newsults = qrsults.content.decode()
#
# http://10.11.104.11/WebView/SystemInfoPartial