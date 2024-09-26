import collections
import inspect
import json
import requests
import sys
import threading
import time

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
    self.ew_sessn = json.loads(connectionsults.content.decode())["t2msession"]


    ewonssults = requests.get(self.getdaewons)
    ewonssults = json.loads(ewonssults.content.decode())
    ewonlist = ewonssults["ewons"]

    print("Launching display thread")
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
          threading.Thread(target=self.getthepcsysinfo,args=(str(anewon["name"]),whatdoesthislooklike[len(whatdoesthislooklike)-1]),name=anewon["name"]+"_thread",daemon=True).start()
        except Exception as exception:
          exc_type, exc_obj, exc_tb = sys.exc_info()
          errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
          print(errorstring)
          # self.outputfield.append(errorstring)
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
      print(str(len(whatdoesthislooklike))+"(T:"+str(cnttru)+" F:"+str(cntfal)+") - "+str(whatdoesthislooklike)+"\n--\n")
      if bustfree:
        break
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
  ###  Method: checksoftwarelevels()
  ###  Purpose: Find the software levels from the sysinfo page. Then compare it with our FTP server.
  ###  Date: 09/04/2024
  ########################################################
  def checksoftwarelevels(self, ewonname, ewonpage):
    #Lets find the proper section
    featver = "<h3>Feature Versions</h3>"
    opntag = ["<div>",-1]
    clstag = ["</div>",-1]
    isitover = False
    try: #First lets find the software levels in the page.
      startingpoint = ewonpage.find(featver)
      if startingpoint > -1:
        balance = 0
        startingpoint = startingpoint + len(featver)
        stoppingpoint = -1
        cutdown = ewonpage[startingpoint:]
        with open(ewonname+"_err.txt","a") as errfile:
          errfile.write("csl1- "+"--------------------------"+ewonname+"-----------------------------"+"\n")
          errfile.write("csl1- "+cutdown+"\n")
          errfile.write("csl1- "+"--------------------------"+ewonname+"-----------------------------"+"\n")
        # self.outputfield.append("--------------------------"+ewonname+"-----------------------------")
        # self.outputfield.append(cutdown)
        # self.outputfield.append("--------------------------"+ewonname+"-----------------------------")
        curpoint = -1
        while(not isitover):
          opntag[1] = cutdown.find(opntag[0])
          clstag[1] = cutdown.find(clstag[0])
          # I'm expecting an opening tag first. Else something is wrong.
          if opntag[1] < clstag[1]:
            balance += 1
            cutdown = cutdown[opntag[1]:]
          elif opntag[1] > clstag[1]:
            balance -= 1
            cutdown = cutdown[clstag[1]:]
          elif balance == 0:
            isitover = True
            cutdown = ewonpage[startingpoint:clstag[1]]
            with open(ewonname+"_err.txt","a") as errfile:
              errfile.write("csl2- "+"************************"+ewonname+"**************************"+"\n")
              errfile.write("csl2- "+cutdown+"\n")
              errfile.write("csl2- "+"************************"+ewonname+"**************************"+"\n")
          elif balance < 0:
            isitover = True
    except Exception as exception:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
      #self.outputfield.append(errorstring)
      with open(ewonname+"_err.txt","a") as errfile:
        errfile.write(errorstring+"\n")
    try:
      # We have what may be a successful search.
      if opntag[1] < clstag[1]:
        # Now lets split on the closing tag, then strip all of the tags from it.
        softwares = cutdown.split(clstag[0])
        for indsw in softwares:
          indsw = indsw[indsw.find("H"):]
        self.outputfield.append(softwares)
        with open(ewonname+"_err.txt","a") as errfile:
          errfile.write("csl3- "+str(softwares)+"\n")

      else:
        self.outputfield.append("The balance was "+str(balance)+" startingpoint: "+str(startingpoint)+" opntag: "+str(opntag)+" clstag: "+str(clstag))
        
      with open(ewonname+"_err.txt","a") as errfile:
        errfile.write("csl4- "+"The balance was "+str(balance)+" startingpoint: "+str(startingpoint)+" opntag: "+str(opntag)+" clstag: "+str(clstag)+"\n")
    except Exception as exception:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
      #self.outputfield.append(errorstring)
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
      print("Starting displayresultshere")
      while((not self.stopped) and (len(self.outputfield) > 0)):
        # if 
        if len(self.outputfield):
          twostrings = self.outputfield.popleft()
          print(twostrings)
        else:
          time.sleep(1)
    except Exception as exception:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
      print(errorstring)

  ########################################################
  ###  Method: getthepcsysinfo()
  ###  Purpose:
  ###  Date: 09/04/2024
  ########################################################
  def getthepcsysinfo(self, ewonname, completionflag):
    with open(ewonname+"_err.txt","a") as errfile:
      errfile.write("1- "+ewonname+"\n")
    try:
      # print(ewonname+"\n")
      # errfile.write(ewonname+"\n")
      # self.outputfield.append("started ewonname: "+ewonname)
      thisewonssysinfo = "https://m2web.talk2m.com/t2mapi/get/"+ewonname+"/proxy/10.11.104.11/WebView/SystemInfoPartial&t2maccount=Hartness&t2musername="+self.ew_usern+"&t2mpassword="+self.ew_passw+"&t2mdeveloperid="+self.ew_devid
      try:
        with open(ewonname+"_err.txt","a") as errfile:
          errfile.write("2- "+thisewonssysinfo+"\n")
          # self.outputfield.append("here we go")
          tryingtoreach = requests.get(thisewonssysinfo,timeout=5.0)
          errfile.write("3- "+str(tryingtoreach)+"\n")
        with open(ewonname+"_err.txt","a") as errfile:
        ### self.outputfield.append(ewonname+" returned "+str(tryingtoreach.status_code)+".")
        # self.outputfield.append(ewonname+" returned "+str(tryingtoreach))
          errfile.write("4- "+ewonname+" returned "+str(tryingtoreach.status_code)+" type "+str(type(tryingtoreach.status_code))+"\n")
        if tryingtoreach.status_code == 200:
          self.checksoftwarelevels(ewonname, tryingtoreach.text)
          # errfile.write("5- "+"  writing "+ewonname+".html"+"\n")
          # self.outputfield.append("  writing "+ewonname+".html")
          with open(ewonname+"_SysInfoPart.html","w") as fp:
            # fp.write(tryingtoreach.content.decode())
            fp.write(tryingtoreach.text)
        else:
          with open(ewonname+"_err.txt","a") as errfile:
            errfile.write("6- "+"  dropping "+ewonname+".html"+"\n")
          # self.outputfield.append("  dropping "+ewonname+".html")
      except Exception as exception:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
        # print(errorstring)
        with open(ewonname+"_err.txt","a") as errfile:
          errfile.write("7- "+errorstring+"\n")
    except Exception as exception:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
      # print(errorstring)
      with open(ewonname+"_err.txt","a") as errfile:
        errfile.write("7- "+errorstring+"\n")
    completionflag[0] = True

if __name__  ==  '__main__':
  checkpcbehindewon()