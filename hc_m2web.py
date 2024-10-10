import collections
import datetime
import ftplib
import inspect
import json
import requests
import sys
import threading
import time

### Get the software levels for comparison,
### Then note which ones you actually need and ftp them at the end.

class checkpcbehindewon:
  def __init__(self):
    self.ew_devid = "f4a5717d-9942-41d7-8d67-11ecafc6e66c"
    self.ew_usern = "dthompson"
    self.ew_passw = "gettingvizzy4it"
    self.ew_sessn = ""
    self.logmein = "https://m2web.talk2m.com/t2mapi/login?t2maccount=Hartness&t2musername="+self.ew_usern+"&t2mpassword="+self.ew_passw+"&t2mdeveloperid="+self.ew_devid
    self.getdaewons = "https://m2web.talk2m.com/t2mapi/getewons?t2maccount=Hartness&t2musername="+self.ew_usern+"&t2mpassword="+self.ew_passw+"&t2mdeveloperid="+self.ew_devid
    self.getdaewon = "https://m2web.talk2m.com/t2mapi/getewon?name="+"placeholder"+"&t2maccount=Hartness&t2musername="+self.ew_usern+"&t2mpassword="+self.ew_passw+"&t2mdeveloperid="+self.ew_devid

    self.outputfield = collections.deque()

    self.stopped = False
    self.run()
    
  ########################################################
  ###  Method: main()
  ###  Purpose:
  ###  Date: 09/04/2024
  ########################################################
  def run(self):
    connectionsults = requests.get(self.logmein)
    # self.ew_sessn = json.loads(connectionsults.content.decode())["t2msession"]
    ewonssults = requests.get(self.getdaewons)
    ewonssults = json.loads(ewonssults.content.decode())
    ewonlist = ewonssults["ewons"]
    maxtime = 60
    starttime = 0

    # print("Launching display thread")
    self.outputfield.append("Launching display thread")
    theoutputter = threading.Thread(target=self.displayresultshere,args=(),name="outputter",daemon=True).start()
    self.outputfield.append("Is it running?")
    # print(" Online\n|-----------|")
    self.outputfield.append(" Online\n|-----------|")
    whatdoesthislooklike = []
    for anewon in ewonlist:
      # print("checking "+str(len(whatdoesthislooklike)))
      if anewon["status"] == "online":
        try:
          whatdoesthislooklike.append([False,str(anewon["name"])])
          time.sleep(.15)
          threading.Thread(target=self.processthesite,args=(str(anewon["name"]),whatdoesthislooklike[len(whatdoesthislooklike)-1]),name=anewon["name"]+"_thread",daemon=True).start()
        except Exception as exception:
          exc_type, exc_obj, exc_tb = sys.exc_info()
          errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
          #print(errorstring)
          self.outputfield.append(errorstring)
    starttime = time.perf_counter()
    while(True):
      cnttru = 0
      cntfal = 0
      bustfree = True
      for jf in whatdoesthislooklike:
        if jf[0] == False:
          cntfal += 1
          bustfree = False
        else:
          cnttru += 1
      print(str(len(whatdoesthislooklike))+" (T:"+str(cnttru)+" F:"+str(cntfal)+")\n--")
      # print(str(len(whatdoesthislooklike))+"(T:"+str(cnttru)+" F:"+str(cntfal)+") - "+str(whatdoesthislooklike)+"\n--\n")
      if bustfree:
        self.outputfield.append("All threads have completed.")
        break
      elif (time.perf_counter() - starttime) > maxtime:
        self.outputfield.append("Some threads have timed out and will be stopped.")
        break
      #The two previous could be combined but I like them separated for reasons.
      else:
        time.sleep(.25)

#   time.sleep(15)
    self.stopped = True
    # time.sleep(3)
    # print("counting down(3): "+str(len(whatdoesthislooklike))+"\n"+str(whatdoesthislooklike))
    # time.sleep(5)
    # print("counting down(5): "+str(len(whatdoesthislooklike))+"\n"+str(whatdoesthislooklike))
    # time.sleep(6)
    # print("last count(6): "+str(len(whatdoesthislooklike))+"\n"+str(whatdoesthislooklike))
    
  ########################################################
  ###  Method: checkdiskspace()
  ###  Purpose: Find the software levels from the sysinfo page. Then compare it with our FTP server.
  ###  Date: 09/04/2024
  ########################################################
  def checkdiskspace(self, ewonname, ewonpage):
    featver = "<h3>Free Space</h3>"
    spaces = self.findmyniche(ewonname, featver, ewonpage)
    try:
      if len(spaces) > 0:
        with open(ewonname+"_err.txt","a") as errfile:
          errfile.write("csl1- "+"-------------------------- "+ewonname+" free space -----------------------------"+"\n"+\
            "\n".join(spaces)+"\n")
      else:
        with open(ewonname+"_err.txt","a") as errfile:
          errfile.write("csl1- "+"-------------------------- "+ewonname+" free space -----------------------------"+"\n"+\
            " *** Unable to discern drives and diskspace ***\n")
    except Exception as exception:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
      self.outputfield.append(ewonname+": "+errorstring)
      with open(ewonname+"_err.txt","a") as errfile:
        errfile.write(errorstring+"\n")

  ########################################################
  ###  Method: checksoftwarelevels()
  ###  Purpose: Find the software levels from the sysinfo page. Then compare it with our FTP server.
  ###  Date: 09/04/2024
  ########################################################
  def checksoftwarelevels(self, ewonname, ewonpage):
    #Lets find the proper section
    featver = "<h3>Feature Versions</h3>"
    softwares = self.findmyniche(ewonname, featver, ewonpage)
    try:
      if len(softwares) > 0:
        with open(ewonname+"_err.txt","a") as errfile:
          errfile.write("csl1- "+"-------------------------- "+ewonname+" software -----------------------------"+"\n"+\
            "\n".join(softwares)+"\n")
      else:
        with open(ewonname+"_err.txt","a") as errfile:
          errfile.write("csl1- "+"-------------------------- "+ewonname+" software -----------------------------"+"\n"+\
            " *** Unable to discern software and levels ***\n")
    except Exception as exception:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
      self.outputfield.append(ewonname+": "+errorstring)
      with open(ewonname+"_err.txt","a") as errfile:
        errfile.write(errorstring+"\n")

  ########################################################
  ###  Method: displayresultshere()
  ###  Purpose: Controls the results box and the Start/Stop button.
  ###  Date: 04/04/2024
  ########################################################
  def displayresultshere(self):
    #make an internal list. Add twostrings to the list to be processed.
    try:
      with open("hc_m2web.log","a") as logfile:
        logfile.write("Starting displayresultshere at "+str(datetime.datetime.now())+"\n")
      print("Starting displayresultshere")
      while (not self.stopped):
        if len(self.outputfield):
          twostrings = self.outputfield.popleft()
          print(twostrings)
          with open("hc_m2web.log","a") as logfile:
            logfile.write(twostrings+"\n")
        else:
          time.sleep(.5)
    except Exception as exception:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
      print(errorstring)

  ########################################################
  ###  Method: findmyniche()
  ###  Purpose: Strips specific section information from sysinfo page
  ###  Date: 09/04/2024
  ########################################################
  def findmyniche(self, ewonname, targety, ewonpage):
    opntag = ["<div>",-1]
    clstag = ["</div>",-1]
    isitover = False
    termedlist = []
    try: #First lets find the software levels in the page.
      startingpoint = ewonpage.find(targety)
      curopntag = startingpoint
      endclstag = startingpoint

      if startingpoint > -1:
        balance = 1
        startingpoint = startingpoint + len(targety)
        stoppingpoint = -1
        curpoint = -1
        while(not isitover):
          opntag[1] = ewonpage.find(opntag[0], curopntag)
          clstag[1] = ewonpage.find(clstag[0], endclstag)
          # I'm expecting an opening tag first. Else something is wrong.
          if opntag[1] < clstag[1]:
            balance += 1
            curopntag = opntag[1]+len(opntag[0])
          elif opntag[1] > clstag[1]:
            balance -= 1
            endclstag = clstag[1]+len(clstag[0])
          if balance == 0:
            isitover = True
            cutdown = ewonpage[startingpoint:endclstag]
    except Exception as exception:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
      self.outputfield.append(ewonname+": "+errorstring)
      with open(ewonname+"_err.txt","a") as errfile:
        errfile.write(errorstring+"\n")
    try:
      # We have what may be a successful search.
      if curopntag < endclstag:
        endclstag = endclstag-len(clstag[0])
        termedlist = ewonpage[startingpoint:endclstag].split(clstag[0])
        if len(termedlist) > 0:
          for indsw in range(len(termedlist)):
            if(len(termedlist[indsw].strip()) == 0):
              termedlist.pop(indsw)
              break
            else:
              termedlist[indsw] = termedlist[indsw].split("<div>")[1][1:].strip()

    except Exception as exception:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
      self.outputfield.append(ewonname+": "+errorstring)
      with open(ewonname+"_err.txt","a") as errfile:
        errfile.write(errorstring+"\n")
    return termedlist
    
  ########################################################
  ###  Method: ftpcheckupandout()
  ###  Purpose:
  ###  Date: 09/04/2024
  ########################################################
  def ftpcheckupandout(self):
    pass
    # myconx = ftplib.FTP_TLS(hostname, username, password)
    # myconx.prot_p()
      # '200 Protection level set to P'
    # myconx.dir()
    # myconx.close()

  ########################################################
  ###  Method: getthepcsysinfo()
  ###  Purpose:Pulls down the systeminfo page if it can reach it.
  ###  Date: 09/04/2024
  ########################################################
  def getthepcsysinfo(self, ewonname):
    tryingtoreach = None
    with open(ewonname+"_err.txt","a") as errfile:
      errfile.write("1- "+ewonname+"\n")
    try:
      thisewonssysinfo = "https://m2web.talk2m.com/t2mapi/get/"+ewonname+"/proxy/10.11.104.11/WebView/SystemInfoPartial&t2maccount=Hartness&t2musername="+self.ew_usern+"&t2mpassword="+self.ew_passw+"&t2mdeveloperid="+self.ew_devid
      try:
        with open(ewonname+"_err.txt","a") as errfile:
          errfile.write("2- "+thisewonssysinfo+"\n")
          # self.outputfield.append("here we go")
          tryingtoreach = requests.get(thisewonssysinfo,timeout=5.0)
          errfile.write("3- "+str(tryingtoreach)+"\n")
        if tryingtoreach.status_code == 200:
          with open(ewonname+"_SysInfoPart.html","w") as fp:
            # fp.write(tryingtoreach.content.decode())
            fp.write(tryingtoreach.text)
        else:
          with open(ewonname+"_err.txt","a") as errfile:
            errfile.write("6- "+"  dropping .html because of status code "+str(tryingtoreach.status_code)+"\n")
          self.outputfield.append(ewonname+": "+"  dropping .html because of status code "+str(tryingtoreach.status_code))
          tryingtoreach = None
      except requests.exceptions.RequestException:
        pass
      except Exception as exception:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
        self.outputfield.append(ewonname+": "+errorstring)
        with open(ewonname+"_err.txt","a") as errfile:
          errfile.write("7- "+errorstring+"\n")
    except Exception as exception:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
      self.outputfield.append(ewonname+": "+errorstring)
      with open(ewonname+"_err.txt","a") as errfile:
        errfile.write("7- "+errorstring+"\n")
    return tryingtoreach

  ########################################################
  ###  Method: processthesite()
  ###  Purpose:Pulls down the systeminfo page if it can reach it.
  ###          Processes it for pertinent data it needs.
  ###          Sets completion flag to True at the end signifying the thread is done.
  ###  Date: 09/04/2024
  ########################################################
  def processthesite(self, ewonname, completionflag):
    try:
      isanythingthere = self.getthepcsysinfo(ewonname)
      if isanythingthere != None:
        pagedump = isanythingthere.text
        self.checksoftwarelevels(ewonname, pagedump)
        self.checkdiskspace(ewonname, pagedump)
      self.outputfield.append(ewonname+": "+"Completed successfully.")
      completionflag[0] = True
    except Exception as exception:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
      self.outputfield.append(ewonname+": "+errorstring)
      with open(ewonname+"_err.txt","a") as errfile:
        errfile.write("7- "+errorstring+"\n")
      self.outputfield.append(ewonname+": "+"Failed with exception. Check its error log")
      completionflag[0] = True
        


if __name__  ==  '__main__':
  checkpcbehindewon()
  
  
  
    # featver = "<h3>Feature Versions</h3>"
    # # opntag = ["<div>",-1]
    # # clstag = ["</div>",-1]
    # # isitover = False
    # # try: #First lets find the software levels in the page.
      # # startingpoint = ewonpage.find(featver)
      # # curopntag = startingpoint
      # # endclstag = startingpoint

      # # if startingpoint > -1:
        # # balance = 1
        # # startingpoint = startingpoint + len(featver)
        # # stoppingpoint = -1
        # # curpoint = -1
        # # while(not isitover):
          # # opntag[1] = ewonpage.find(opntag[0], curopntag)
          # # clstag[1] = ewonpage.find(clstag[0], endclstag)
          # # # I'm expecting an opening tag first. Else something is wrong.
          # # if opntag[1] < clstag[1]:
            # # balance += 1
            # # curopntag = opntag[1]+len(opntag[0])
          # # elif opntag[1] > clstag[1]:
            # # balance -= 1
            # # endclstag = clstag[1]+len(clstag[0])
          # # if balance == 0:
            # # isitover = True
            # # cutdown = ewonpage[startingpoint:endclstag]
    # # except Exception as exception:
      # # exc_type, exc_obj, exc_tb = sys.exc_info()
      # # errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
      # # #self.outputfield.append(errorstring)
      # # with open(ewonname+"_err.txt","a") as errfile:
        # # errfile.write(errorstring+"\n")
    # # try:
      # # # We have what may be a successful search.
      # # if curopntag < endclstag:
        # # endclstag = endclstag-len(clstag[0])
        # # softwares = ewonpage[startingpoint:endclstag].split(clstag[0])
        # for indsw in range(len(softwares)):
