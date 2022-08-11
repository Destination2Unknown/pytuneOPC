"""
   
Updated and maintained by destination0b10unknown@gmail.com
Copyright 2022 destination2unknown

Licensed under the MIT License;
you may not use this file except in compliance with the License.

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
   
"""
import sys
import time
import tkinter as tk
import csv
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import threading
from matplotlib import animation
from datetime import datetime
from asyncua.sync import Client,ua
from pytunelogix.common import generalclasses as g

def main():
    class data(object):
        def __init__(self):      
            self.reset()
            self.CSVFileWriter=0
            self.PID_PV=0
            self.PID_SP=0
            self.PID_CV=0
            self.loop_record=0
                        
        def update(self,PV,CV,SP):
            self.PV=np.append(self.PV,PV)
            self.CV=np.append(self.CV,CV)
            self.SP=np.append(self.SP,SP) 
            
        def reset(self):
            self.PV = np.zeros(0)
            self.CV = np.zeros(0)
            self.SP = np.zeros(0)        
            self.ErrCount=0
            self.ReadCount=0
            self.SetupFlag=False
            self.RunNowFlag=False
            self.CSVFile=object          

        def plc(self,ip):
            self.comm = Client(ip)
                
    def thread_record():        
        gData.loop_record = g.PeriodicInterval(Record, int(deltat.get())/1000)
        
    def Record():
        if gData.SetupFlag==False:
            #Setup communnication object 
            gData.plc(ip.get())            
            gData.comm.connect()                  
            spstatus.set("")
            pvstatus.set("")
            cvstatus.set("")        
            gData.ErrCount=0
            gData.ReadCount=0
            gData.SetupFlag=True 
            gData.RunNowFlag=True
            button_record.configure(bg = "Black")
            button_record["state"] = "disabled"
            gData.PID_PV = gData.comm.get_node(pvtexttag.get())
            gData.PID_CV = gData.comm.get_node(cvtexttag.get())
            gData.PID_SP = gData.comm.get_node(sptexttag.get())
            try:
                #Write new data to csv if read was successful, if not write last value, Open File or create if it doesn't exist
                gData.CSVFile = open(fname.get(), 'a')
                gData.CSVFileWriter = csv.writer(gData.CSVFile, delimiter=';', lineterminator='\n', quotechar='/', quoting=csv.QUOTE_MINIMAL)
                #Write headers if its a new file
                if os.stat(fname.get()).st_size == 0:
                    gData.CSVFileWriter.writerow(('PV','CV','SP','TimeStamp'))

            except Exception as e:    
                spstatus.set('File Error: ' + str(e))  
                cvstatus.set('File Error: ' + str(e))  
                pvstatus.set('File Error: ' + str(e)) 

        current_date_time = datetime.utcnow().strftime('%d-%m-%Y %H:%M:%S.%f')    

        try:            
            #Setup tags to read            
            gData.PID_PV.read_value()
            gData.PID_CV.read_value()
            gData.PID_SP.read_value()
    
            actualpv=round(gData.PID_PV.read_value(),2)
            pvtext.set(actualpv)         
            pvtexttag.configure(state="disabled")

            actualcv=round(gData.PID_CV.read_value(),2)
            cvtext.set(actualcv)         
            cvtexttag.configure(state="disabled")

            actualsp=round(gData.PID_SP.read_value(),2)
            sptext.set(actualsp)
            sptexttag.configure(state="disabled")

            #Disable inputs if tag read is successful
            deltat.configure(state="disabled")
            ip.configure(state="disabled")
            fname.configure(state="disabled")
            button_record.configure(bg = "Green")
            button_livetrend["state"] = "normal"            

            #If successful increment read counter
            gData.ReadCount+=1

        except Exception as e:    
            if len(gData.PV>0):
                actualpv=gData.PV[-1]
            else:
                actualpv=0
            if len(gData.CV>0):
                actualcv=gData.CV[-1]
            else:
                actualcv=0
            if len(gData.SP>0):
                actualsp=gData.SP[-1]
            else:
                actualsp=0
            #If read fails update error counter
            gData.ErrCount+=1

            spstatus.set('Error: ' + str(e))  
            cvstatus.set('Error: ' + str(e))  
            pvstatus.set('Error: ' + str(e))
        
        finally:
            ec='Errors: '+ str(gData.ErrCount)
            rc='Reads: '+ str(gData.ReadCount)
            errorcount.set(ec)
            readcount.set(rc)
            #Write all values to csv file  
            row = [actualpv,actualcv,actualsp]
            gData.update(actualpv,actualcv,actualsp)            
            row.append(current_date_time)
            if gData.RunNowFlag:
                gData.CSVFileWriter.writerow(row)    
            
    def Write():
        if spsend.get() or cvsend.get():
            try:
                if gData.SetupFlag==False:
                    #Setup communnication object 
                    gData.plc(ip.get())            
                    gData.comm.connect()   
                #Setup tags to read back data
                PID_PV = gData.comm.get_node(pvtexttag.get())
                PID_CV = gData.comm.get_node(cvtexttag.get())
                PID_SP = gData.comm.get_node(sptexttag.get())
            
                #Don't write data if empty, reads back data after write
                if spsend.get(): 
                    sp = float(spsend.get())                    
                    PID_SP.write_attribute(ua.AttributeIds.Value, ua.DataValue(sp))
                    sptext.set(round(PID_SP.read_value(),2))
                if cvsend.get():
                    cv=float(cvsend.get())
                    PID_CV.write_attribute(ua.AttributeIds.Value, ua.DataValue(cv))                
                    cvtext.set(round(PID_CV.read_value(),2))

            except Exception as e:    
                spstatus.set('Write Error: ' + str(e))  
                cvstatus.set('Write Error: ' + str(e))          

    def TrendFileData():
        try:
            if gData.RunNowFlag:
                gData.CSVFile.flush()        
            df = pd.read_csv(fname.get(), sep=';',quoting=csv.QUOTE_NONE, escapechar="\\", encoding="utf-8")
            headers=list(df)
            df['TimeStamp'] = pd.to_datetime(df['TimeStamp'],format='%d-%m-%Y %H:%M:%S.%f')
            plt.figure()
            plt.plot(df['TimeStamp'],df[headers[0]], color="#1f77b4", linewidth=2, label=headers[0])
            plt.plot(df['TimeStamp'],df[headers[1]], color="#ff7f0e",linewidth=2,label=headers[1])
            plt.plot(df['TimeStamp'],df[headers[2]], color="#2ca02c",linewidth=2,label=headers[2])
            plt.ylabel('EU')                   
            plt.xlabel("Time")
            plt.title(fname.get())
            plt.legend(loc='best')
            plt.gcf().autofmt_xdate()
            plt.show()
        
        except Exception as e:    
            pvstatus.set('CSV Read Error: ' + str(e))  
    
    def LiveTrend(): 
        #Set up the figure
        fig = plt.figure()
        ax = plt.axes(xlim=(0,100),ylim=(0, 100))
        SP, = ax.plot([], [], lw=2, label='SP')
        PV, = ax.plot([], [], lw=2, label='PV')
        CV, = ax.plot([], [], lw=2, label='CV')

        #Setup Func
        def init():
            SP.set_data([], [])
            PV.set_data([], [])
            CV.set_data([], [])
            plt.ylabel('EU')  
            plt.xlabel("Time (min)")
            plt.suptitle("Live Data")        
            plt.legend(loc='best')
            return SP,PV,CV,

        #Loop here
        def animate(i):     
            x = np.arange(len(gData.SP),dtype=int)
            scale = int(60*1000/int(deltat.get())) #Convert mS to Minutes
            x=x/scale
            ax.set_xlim(0,max(x)*1.1)
            SP.set_data(x,gData.SP)
            CV.set_data(x,gData.CV)
            PV.set_data(x,gData.PV)
            return SP,PV,CV,

        #Live Data
        if gData.RunNowFlag:
            anim = animation.FuncAnimation(fig, animate, init_func=init, frames=100, interval=1000) #, blit=True) # cant use blit with dynamic x-axis

        plt.show()

    def Stop():        
        gData.loop_record.stop()                                        
        gData.loop_record.join(0.11)
        #Enable text box entry
        sptexttag.configure(state="normal")
        pvtexttag.configure(state="normal")
        cvtexttag.configure(state="normal")
        deltat.configure(state="normal")
        ip.configure(state="normal")
        fname.configure(state="normal")        
        button_record.configure(bg = "#f0f0f0")
        button_livetrend["state"] = "disabled"
        button_record["state"] = "normal"        
        if not gData.CSVFile.closed:
            gData.CSVFile.close()
        gData.reset()
        plt.close('all')
        gData.comm.disconnect()

    #Gui
    root = tk.Tk()
    root.title('OPC-UA PID Data Logger -> CSV')
    root.resizable(True, True)
    root.geometry('650x175')

    #Text tags setup
    pvtext = tk.StringVar()
    cvtext = tk.StringVar()
    sptext = tk.StringVar()
    pvstatus = tk.StringVar()
    cvstatus = tk.StringVar()
    spstatus = tk.StringVar()
    errorcount = tk.StringVar()
    readcount = tk.StringVar()
    sptexttag = tk.Entry(root,width=25)
    pvtexttag = tk.Entry(root,width=25)
    cvtexttag = tk.Entry(root,width=25)
    spsend = tk.Entry(root,width=5)
    cvsend = tk.Entry(root,width=5)
    deltat = tk.Entry(root,width=5)
    ip = tk.Entry(root,width=25)
    fname = tk.Entry(root,width=5)

    #Column 0
    #Labels
    tk.Label(root, text="  ").grid(row=0,column=0,padx=10 ,pady=2)
    tk.Label(root, text="Tag").grid(row=0,column=0,padx=10 ,pady=2)
    tk.Label(root, text="SP:").grid(row=1,column=0,padx=10 ,pady=2)
    tk.Label(root, text="PV:").grid(row=2,column=0,padx=10 ,pady=2)
    tk.Label(root, text="CV:").grid(row=3,column=0,padx=10 ,pady=2)

    #Column 1
    #Label positions - Read
    tk.Label(root, text="Value").grid(row=0,column=1,padx=10 ,pady=2)
    tk.Label(root, textvariable=sptext).grid(row=1,column=1,padx=10 ,pady=2)
    tk.Label(root, textvariable=pvtext).grid(row=2,column=1,padx=10 ,pady=2)
    tk.Label(root, textvariable=cvtext).grid(row=3,column=1,padx=10 ,pady=2)

    #Column 2
    #Send - Write
    tk.Label(root, text="Write").grid(row=0,column=2,padx=10 ,pady=2)
    spsend.grid(row=1, column=2,padx=10 ,pady=2,sticky="NESW")
    cvsend.grid(row=3, column=2,padx=10 ,pady=2,sticky="NESW")

    #Column 3,4
    #Actual PLC TagName
    tk.Label(root, text="OPC-UA Tag").grid(row=0,column=3,padx=10 ,pady=2)
    sptexttag.grid(row=1, column=3,padx=10,columnspan=2 ,pady=2,sticky="NESW")
    pvtexttag.grid(row=2, column=3,padx=10,columnspan=2 ,pady=2,sticky="NESW")
    cvtexttag.grid(row=3, column=3,padx=10,columnspan=2 ,pady=2,sticky="NESW")
    deltat.grid(row=4, column=3,columnspan=1,padx=10 ,pady=2,sticky="NESW")
    tk.Label(root, text="mS",bg='#F0F0F0').grid(row=4,column=3,padx=10 ,pady=2,sticky="E")

    #Column 5,6
    #Actual PLC address
    tk.Label(root, text="OPC-UA PLC Address:").grid(row=0,column=5,padx=10 ,pady=2)
    ip.grid(row=1, column=5,padx=10,columnspan=2 ,pady=2,sticky="NESW")
    fname.grid(row=4, column=5,padx=10,columnspan=2 ,pady=2,sticky="NESW")

    #Column 7
    #Status
    tk.Label(root, text="Last Error:").grid(row=0,column=7,padx=10,columnspan=2 ,pady=2,sticky="W")
    tk.Label(root, textvariable=spstatus).grid(row=1,column=7,padx=10,columnspan=2 ,pady=2,sticky="W")
    tk.Label(root, textvariable=pvstatus).grid(row=2,column=7,padx=10,columnspan=2 ,pady=2,sticky="W")
    tk.Label(root, textvariable=cvstatus).grid(row=3,column=7,padx=10,columnspan=2 ,pady=2,sticky="W")
    tk.Label(root, textvariable=errorcount).grid(row=4,column=7,padx=10,columnspan=2 ,pady=2,sticky="W")
    tk.Label(root, textvariable=readcount).grid(row=5,column=7,padx=10,columnspan=2 ,pady=2,sticky="W")

    #Default Values
    sptexttag.insert(0, "ns=2;s=Channel1.Device1.PID_SP")
    pvtexttag.insert(0, "ns=2;s=Channel1.Device1.PID_PV")
    cvtexttag.insert(0, "ns=2;s=Channel1.Device1.PID_CV")
    deltat.insert(0, "100")
    ip.insert(0, "opc.tcp://192.168.123.100:49320")
    fname.insert(0,"D:\Trend.csv")

    #Buttons
    #Record Button Placement
    button_record = tk.Button(root, text="Record Data",disabledforeground="white", command=lambda :[thread_record()])
    button_record.grid(row=4,column=0,columnspan=2,padx=10 ,pady=2,sticky="NESW")

    #Write Button Placement
    button_write = tk.Button(root, text="Write", command=lambda :[Write()])
    button_write.grid(row=4,column=2,columnspan=1,padx=10 ,pady=2,sticky="NESW")

    #Live Trend Button Placement
    button_livetrend = tk.Button(root, text="Live Plot", command=lambda :[LiveTrend()])
    button_livetrend.grid(row=5,column=3,columnspan=1,padx=10 ,pady=2,sticky="NESW")
    button_livetrend["state"] = "disabled"

    #Stop Trends Button Placement
    button_stop = tk.Button(root, text="Stop Recording", command=lambda :[Stop()])
    button_stop.grid(row=5,column=0,columnspan=3,padx=10 ,pady=2,sticky="NESW")

    #Trend Button Placement
    button_TrendFileData = tk.Button(root, text="Plot Data From CSV", command=lambda :[TrendFileData()])
    button_TrendFileData.grid(row=5,column=4,columnspan=1,padx=10 ,pady=2,sticky="NESW")

    #Class init
    gData=data()
    root.mainloop()

if __name__ == '__main__':
    main()