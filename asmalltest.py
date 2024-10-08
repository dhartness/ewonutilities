import collections
import inspect
import json
import requests
import sys
import threading
import time

#def checksoftwarelevels(self, ewonname, ewonpage):

#Lets find the proper section
featver = "<h3>Feature Versions</h3>"
opntag = ["<div>",-1]
clstag = ["</div>",-1]
isitover = False

with open("W750036_SysInfoPart.html","r") as epage:
  ewonpage = epage.read()

ewonname = "W750036"
print("Preparing to show page.")
time.sleep(5)
# print(str(ewonpage))
# time.sleep(5)

try: #First lets find the software levels in the page.
  startingpoint = ewonpage.find(featver)
  if startingpoint > -1:
    balance = 1
    startingpoint = startingpoint + len(featver)
    stoppingpoint = -1
    cutdown = ewonpage[startingpoint:]
    # with open(ewonname+"_err.txt","a") as errfile:
    print("csl1- "+"--------------------------"+ewonname+"-----------------------------"+"\n")

    curpoint = -1
    curopntag = startingpoint
    endclstag = startingpoint
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
  print(errorstring+"\n")
try:
  # We have what may be a successful search.
  if curopntag < endclstag:
    endclstag = endclstag-len(clstag[0])
    # print("All good: The balance was "+str(balance)+" startingpoint: "+str(startingpoint)+" opntag: "+str(curopntag)+" clstag: "+str(endclstag)+"\n")
    
    softwares = ewonpage[startingpoint:endclstag].split(clstag[0])
    for indsw in range(len(softwares)):
      if(len(softwares[indsw].strip()) == 0):
        softwares.pop(indsw)
        break
      else:
        softwares[indsw] = "H"+softwares[indsw].split("H")[1]
        print("csl3- H"+str(softwares[indsw].split("H")[1])+"\n")
  else:
    print("All bad: The balance was "+str(balance)+" startingpoint: "+str(startingpoint)+" opntag: "+str(opntag)+" clstag: "+str(clstag))
    
  print("csl4- "+"The balance was "+str(balance)+" startingpoint: "+str(startingpoint)+" opntag: "+str(opntag)+" clstag: "+str(clstag)+"\n")
except Exception as exception:
  exc_type, exc_obj, exc_tb = sys.exc_info()
  errorstring = str(inspect.stack()[0][3])+" - "+str(exc_type)+" on l#"+str(exc_tb.tb_lineno)+": "+str(exception)
  #self.outputfield.append(errorstring)
  print(errorstring+"\n")

