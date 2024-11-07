import collections
import datetime
import ftplib
import inspect
import json
import os
import requests
import sys
import threading
import time

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
    self.compiledsoftwareneeds = collections.deque()
    self.compileddiskspaceneeds = collections.deque()
    self.compiledcamerapings = collections.deque()

    self.ftpserverfilelisting = []
    self.currentresultdate = "results"+str(datetime.datetime.now()).split()[0].replace("-","")
    try:
      os.mkdir(self.currentresultdate)
    except Exception as exception:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
      self.outputfield.append(errorstring)

    self.stopped = False
    self.run()
    
  ########################################################
  ###  Method: main()
  ###  Purpose:
  ###  Date: 09/04/2024 d2lb48
  ########################################################
  def run(self):
    maxtime = 60
    starttime = 0
    ewonlist = None
    self.outputfield.append("Launching display thread")
    theoutputter = threading.Thread(target=self.displayresultshere,args=(),name="outputter",daemon=True).start()
    self.outputfield.append("Is it running?")
    self.outputfield.append(" Online\n|-----------|")
    self.outputfield.append("Checking for old files.")
    try:
      os.remove("softwarereport.txt")
    except Exception as exception:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
      self.outputfield.append(errorstring)
    try:
      os.remove("diskspacereport.txt")
    except Exception as exception:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
      self.outputfield.append(errorstring)
    try:
      os.remove("campingsreport.txt")
    except Exception as exception:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
      self.outputfield.append(errorstring)
    try:
      connectionsults = requests.get(self.logmein)
      # self.ew_sessn = json.loads(connectionsults.content.decode())["t2msession"]
      ewonssults = requests.get(self.getdaewons)
      ewonssults = json.loads(ewonssults.content.decode())
      ewonlist = ewonssults["ewons"]
    except Exception as exception:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
      self.outputfield.append(errorstring)
    whatdoesthislooklike = []
    try:
      if len(ewonlist):
        self.ftpcheckupandout(self.ftpserverfilelisting)
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
            self.outputfield.append(errorstring)
    except Exception as exception:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
      self.outputfield.append(errorstring)
    self.outputfield.append(str(whatdoesthislooklike))
    starttime = time.perf_counter()
    try:
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
        print(str(len(whatdoesthislooklike))+" (T:"+str(cnttru).rjust(3)+" F:"+str(cntfal).rjust(3)+")")
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
    except Exception as exception:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
      self.outputfield.append(errorstring)

    self.collationatcompletion()
    
    time.sleep(3)

    self.stopped = True
    
  ########################################################
  ###  Method: checkcameraconnection()
  ###  Purpose: Find the camera connectivity from the sysinfo page. Then compare it with our FTP server.
  ###  Date: 11/06/2024
  ########################################################
  def checkcameraconnection(self, ewonname, ewonpage):
    featver = "<h3>Device Addresses</h3>"
    spaces = self.findmyniche(ewonname, featver, ewonpage)
    myresults = []
    try:
      if len(spaces) > 0:
        self.outputfield.append([ewonname,"Cameras recognized, checking for lack of connectivity."])
        for adrv in spaces:
          if "red" in adrv:
            mkspcstr = [ewonname,adrv.split()[0]]
            myresults.append(mkspcstr)
        if len(myresults) > 0:
          self.compiledcamerapings.append(myresults)
      else:
        self.outputfield.append([ewonname,"\n"+ewonname+" cameras"+"\n"+\
            " *** No cameras connected. ***\n"])
    except Exception as exception:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
      self.outputfield.append([ewonname,errorstring])

  ########################################################
  ###  Method: checkdiskspace()
  ###  Purpose: Find the software levels from the sysinfo page. Then compare it with our FTP server.
  ###  Date: 09/04/2024
  ########################################################
  def checkdiskspace(self, ewonname, ewonpage):
    featver = "<h3>Free Space</h3>"
    spaces = self.findmyniche(ewonname, featver, ewonpage)
    myresults = []
    try:
      if len(spaces) > 0:
        self.outputfield.append([ewonname,"Drives recognized, checking for low space."])
        for adrv in spaces:
          if "C:" in adrv:
            spz = eval(adrv[adrv.index("(")+1:adrv.index(")")-1])
            # self.outputfield.append([ewonname,"Drive: "+str(adrv)+". Think its "+str(spz)+" which is: "+str(type(spz))+"."])
            if spz >= 60:
              mkspcstr = [ewonname,adrv.split()[0],adrv.split(" / ")[0].split()[2],adrv.split(" GB")[0].split()[4],spz]
              # self.outputfield.append([ewonname, "|| - "+str(mkspcstr)+" is adding to xls."])
              myresults.append(mkspcstr)
            else:
              self.outputfield.append([ewonname, str(spz)+" is not larger than or equal to 60"])
        if len(myresults) > 0:
          self.compileddiskspaceneeds.append(myresults)
      else:
        self.outputfield.append([ewonname,"\n"+"csl1- "+ewonname+" free space"+"\n"+\
            " *** Unable to discern drives and diskspace ***\n"])
    except Exception as exception:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
      self.outputfield.append([ewonname,errorstring])

  ########################################################
  ###  Method: checksoftwarelevels()
  ###  Purpose: Find the software levels from the sysinfo page. Then compare it with our FTP server.
  ###  Date: 09/04/2024
  ########################################################
  def checksoftwarelevels(self, ewonname, ewonpage):
    #Lets find the proper section
    featver = "<h3>Feature Versions</h3>"
    oursoftwares = (("HartnessConnectWeb","HartnessConnectWeb"),
                    ("Hartness Connect Deployment Manager","DeploymentManager"),
                    ("Hartness Connect Manager","HartnessConnectManager"),
                    ("Hartness Insight Collector","InsightCollector"),
                    ("Hartness Insight Adapter","InsightAdapter"),
                    ("Hartness OPCBroker","OPCBroker"),
                    ("Hartness Retrospect Server","RetrospectServer"))
    softwares = self.findmyniche(ewonname, featver, ewonpage)
    myresults = []
    try:
      if len(softwares) > 0:
        self.outputfield.append([ewonname,"Software recognized, checking for versions."])
        for asfw in softwares:
          smller = asfw.split(" - ")[0]
          target = [x[1] for x in oursoftwares if smller in x[0]][0]
          hunted = [x for x in self.ftpserverfilelisting if target in x[1]][0]
          if hunted[1].split("_")[1] > asfw.split(" - ")[1]:
            mkspcstr = [ewonname,target,asfw.split(" - ")[1],hunted[1].split("_")[1]]
            myresults.append(mkspcstr)
        if len(myresults) > 0:
          self.compiledsoftwareneeds.append(myresults)
      else:
        self.outputfield.append([ewonname,"\n"+"csl1- "+ewonname+" software "+"\n"+\
            " *** Unable to discern software and levels ***\n"])
    except Exception as exception:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
      self.outputfield.append([ewonname,errorstring])
        
  ########################################################
  ###  Method: collation at completion()
  ###  Purpose: As each site completes its run any that are found deficient will add its information to one of two lists.
  ###    and this method will process those lists into two separate files and concatenante them to a single csv file.
  ###  Date: 04/04/2024
  ########################################################
  def collationatcompletion(self):
    self.outputfield.append("Collating Report")
    self.createsoftwarereport()
    self.createfreespacereport()
    self.createcamerareport()
    try:
      with open("checkin"+self.currentresultdate+".csv","w") as compl:
        compl.write("Software Check Results\n")
        try:
          with open("softwarereport.txt","r") as getsoft:
            apart = getsoft.read()
            compl.write(apart)
          # os.remove("softwarereport.txt")
        except Exception as exception:
          exc_type, exc_obj, exc_tb = sys.exc_info()
          errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
          self.outputfield.append(errorstring)        
        compl.write("\n\nDisk Check Results\n")
        try:
          with open("diskspacereport.txt","r") as getdisk:
            apart = getdisk.read()
            compl.write(apart)
          # os.remove("diskspacereport.txt")
        except Exception as exception:
          exc_type, exc_obj, exc_tb = sys.exc_info()
          errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
          self.outputfield.append(errorstring)
        compl.write("\n\nCamera Check Results\n")
        try:
          with open("campingsreport.txt","r") as getdisk:
            apart = getdisk.read()
            compl.write(apart)
          # os.remove("campingsreport.txt")
        except Exception as exception:
          exc_type, exc_obj, exc_tb = sys.exc_info()
          errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
          self.outputfield.append(errorstring)
    except Exception as exception:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
      self.outputfield.append(errorstring)

  ########################################################
  ###  Method: createcamerareport()
  ###  Purpose:
  ###  Date: 04/04/2024
  ########################################################
  def createcamerareport(self):
    try:
      self.outputfield.append(self.compiledcamerapings)
      prevnum = ""
      with open("campingsreport.txt","w") as disked:
        self.outputfield.append("Camera Offlines Sites Reported: "+str(len(self.compiledcamerapings)))
        for lowfree in self.compiledcamerapings:
          prevnum = "joke"
          for asite in lowfree:
            if prevnum == "joke":
              prevnum = asite[0]
            disked.write(prevnum+","+asite[1]+"\n")
            prevnum = ""
    except Exception as exception:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
      self.outputfield.append(errorstring)

  ########################################################
  ###  Method: createfreespacereport()
  ###  Purpose:
  ###  Date: 04/04/2024
  ########################################################
  def createfreespacereport(self):
    try:
      self.outputfield.append(self.compileddiskspaceneeds)
      prevnum = ""
      with open("diskspacereport.txt","w") as disked:
        self.outputfield.append("Disk Fulls Sites Reported: "+str(len(self.compileddiskspaceneeds)))
        for lowfree in self.compileddiskspaceneeds:
          prevnum = "joke"
          for asite in lowfree:
            if prevnum == "joke":
              prevnum = asite[0]
            disked.write(prevnum+","+asite[1]+","+str(asite[2])+","+str(asite[3])+","+str(asite[4])+"\n")
            prevnum = ""
    except Exception as exception:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
      self.outputfield.append(errorstring)

  ########################################################
  ###  Method: createfreespacereport()
  ###  Purpose:
  ###  Date: 04/04/2024
  ########################################################
  def createsoftwarereport(self):
    try:
      self.outputfield.append(self.compiledsoftwareneeds)
      with open("softwarereport.txt","w") as disked:
        self.outputfield.append("Software Outdated Sites Reported: "+str(len(self.compiledsoftwareneeds)))
        for lowfree in self.compiledsoftwareneeds:
          prevnum = "joke"
          for asite in lowfree:
            if prevnum == "joke":
              prevnum = asite[0]
            disked.write(prevnum+","+asite[1]+","+asite[2]+","+asite[3][:-1]+"\n")
            prevnum = ""
    except Exception as exception:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
      self.outputfield.append(errorstring)

  ########################################################
  ###  Method: displayresultshere()
  ###  Purpose: Controls the results box and the Start/Stop button.
  ###  Date: 04/04/2024
  ########################################################
  def displayresultshere(self):
    #make an internal list. Add twostrings to the list to be processed.
    try:
      with open(self.currentresultdate+"\\"+"hc_m2web.log","a") as logfile:
        logfile.write("Starting displayresultshere at "+str(datetime.datetime.now())+"\n")
      print("Starting displayresultshere")
      while (not self.stopped):
        if len(self.outputfield):
          twostrings = self.outputfield.popleft()
          if type(twostrings) == str:
            pass
            # print(twostrings)
          elif type(twostrings) == list:
            with open(self.currentresultdate+"\\"+twostrings[0]+"_err.txt","a") as errfile:
              errfile.write(twostrings[1]+"\n")        
          with open(self.currentresultdate+"\\"+"hc_m2web.log","a") as logfile:
            logfile.write(str(twostrings)+"\n")
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
      self.outputfield.append([ewonname,errorstring])
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
      self.outputfield.append([ewonname,errorstring])
    return termedlist
    
  ########################################################
  ###  Method: ftpcheckupandout()
  ###  Purpose:
  ###  Date: 09/04/2024
  ########################################################
  def ftpcheckupandout(self, onlythefilesineed):
    hostname = "52.170.87.208"
    username = "HcInstallations"
    password = "gNPfcQa!Tw99diPy"
    myconx = None
    dirsfound = []
    filesfound = []
    conxgood = True
    # onlythefilesineed = []
    self.outputfield.append("Checking FTP site at "+hostname+" for current software levels.")
    print("Checking FTP site at "+hostname+" for current software levels.")

    def getmyfiles(currentry):
      if currentry.find(".") > -1:
        filesfound.append(currentry)

    def getmydirs(currentry):
      if currentry.find(".") == -1:
        dirsfound.append(currentry)

    def getitall(currentry):
      filesfound.append(currentry)

    try:
      myconx = ftplib.FTP_TLS(hostname, username, password, timeout=30)
      myconx.prot_p() # '200 Protection level set to P'
      myconx.dir(getmydirs)
      for thisdir in dirsfound:
        try:
          filesfound.clear()
          if thisdir[0] != 'd':
            continue
          self.outputfield.append("Trying to navigate to: "+thisdir[49:])
          myconx.cwd(thisdir[49:])
          myconx.dir(getitall)
          for filly in filesfound:
            if ".HCBackup" in filly:
              onlythefilesineed.append([thisdir[49:],filly[49:].split(".HCBackup")[0]])
              # onlythefilesineed.append([thisdir[49:],filly[49:]])
          myconx.cwd("..")
        except Exception as exception:
          exc_type, exc_obj, exc_tb = sys.exc_info()
          errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
          self.outputfield.append(errorstring)
          myconx.cwd("..")
      # Let try to download these for convenience.
      self.outputfield.append("Compare to current version in the file and if its lower remove the old file and download the new one.")
      try:
        if os.exists("ftparchive.txt"):
          filestocompare = []
          with open("ftparchive.txt","r") as savesw:
            for line in savesw:
              filestocompare.append(line[1:-1].replace("'","").split(","))
              print(line)
      except Exception as exception:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
        self.outputfield.append(errorstring)
      
      #
      #
      #
      #
      #
      #
      #
      
      # Lets right this to a text file in case we can't connect next time.
      if len(onlythefilesineed) > 0:
        self.outputfield.append("Length of software library is greater than zero. Will attempt to write to file.")
        try:
          with open("ftparchive.txt","w") as savesw:
            for j1 in onlythefilesineed:
              savesw.write(str(j1)+"\n")
          self.outputfield.append("File \'ftparchive.txt\' has been created.")
        except Exception as exception:
          exc_type, exc_obj, exc_tb = sys.exc_info()
          errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
          self.outputfield.append("error, writing \'ftparchive.txt\':"+errorstring)
    except Exception as exception:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
      self.outputfield.append("issue connecting to ftp server, will try to use archived information - "+errorstring)
      conxgood = False
      try:
        with open("ftparchive.txt","r") as savesw:
          for line in savesw:
            # self.outputfield.append("Read line
            onlythefilesineed.append(line[1:-2].replace("'","").split(","))
            print("** "+line)
        print(onlythefilesineed)
        self.outputfield.append("File \'ftparchive.txt\' has been read.")
      except Exception as exception:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
        self.outputfield.append(errorstring)
    try:
      self.outputfield.append("Our current software versions")
      if conxgood:
        for otfin in onlythefilesineed:
          self.outputfield.append(otfin[1].split(".HCBackup")[0])
      self.outputfield.append("\n\nAnd now we're closing the connection.")
      myconx.close()
    except Exception as exception:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
      self.outputfield.append(errorstring)

  ########################################################
  ###  Method: getthepcsysinfo()
  ###  Purpose:Pulls down the systeminfo page if it can reach it.
  ###  Date: 09/04/2024
  ########################################################
  def getthepcsysinfo(self, ewonname):
    tryingtoreach = None
    attemptno = 1
    self.outputfield.append([ewonname, "1- "+ewonname+"\n"])
    try:
      if "ITW Hartness HQ" in ewonname:
        thisewonssysinfo = "https://m2web.talk2m.com/t2mapi/get/"+ewonname+"/proxy/10.11.104.15/WebView/SystemInfoPartial&t2maccount=Hartness&t2musername="+self.ew_usern+"&t2mpassword="+self.ew_passw+"&t2mdeveloperid="+self.ew_devid
      else:
        thisewonssysinfo = "https://m2web.talk2m.com/t2mapi/get/"+ewonname+"/proxy/10.11.104.11/WebView/SystemInfoPartial&t2maccount=Hartness&t2musername="+self.ew_usern+"&t2mpassword="+self.ew_passw+"&t2mdeveloperid="+self.ew_devid
      try:
        # self.outputfield.append(ewonname+" brokenwhile loop "+str())
        while(attemptno <= 3):
          self.outputfield.append([ewonname, "2- attempt #"+str(attemptno)+"\n2-"+thisewonssysinfo+"\n"])
          # self.outputfield.append("here we go")
          tryingtoreach = requests.get(thisewonssysinfo,timeout=10.0)
          self.outputfield.append([ewonname,"3- "+str(tryingtoreach)+"\n"])
          if tryingtoreach.status_code == 200:
            with open(self.currentresultdate+"\\"+ewonname+"_SysInfoPart.html","w") as fp:
              # fp.write(tryingtoreach.content.decode())
              fp.write(tryingtoreach.text)
            attemptno = 10
          else:
            self.outputfield.append([ewonname,"(#"+str(attemptno)+") dropping .html; status code "+str(tryingtoreach.status_code)+"; will try up to three times."])
            tryingtoreach = None
            attemptno += 1
            time.sleep(3)
      # except requests.exceptions.RequestException:
        # pass
      except Exception as exception:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
        self.outputfield.append([ewonname,errorstring])
    except Exception as exception:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
      self.outputfield.append([ewonname,errorstring])
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
      self.outputfield.append("Checking PC at "+ewonname)
      isanythingthere = self.getthepcsysinfo(ewonname)
      if isanythingthere != None:
        pagedump = isanythingthere.text
        self.checksoftwarelevels(ewonname, pagedump)
        self.checkdiskspace(ewonname, pagedump)
        self.checkcameraconnection(ewonname, pagedump)
      self.outputfield.append(ewonname+": "+"Completed successfully.")
      completionflag[0] = True
    except Exception as exception:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
      self.outputfield.append([ewonname,errorstring])
      completionflag[0] = True

if __name__  ==  '__main__':
  checkpcbehindewon()
