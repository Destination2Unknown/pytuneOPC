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
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import random
import threading
import time
from matplotlib import animation
from scipy.integrate import odeint
from asyncua.sync import Client,ua
from pytunelogix.common import generalclasses as g

def main():
    class data(object):
        def __init__(self):      
            self.PV = np.zeros(0)
            self.CV = np.zeros(0)
            self.SP = np.zeros(0)
            self.livetrend=0
            self.scanCount=0
            self.PID_PV=0
            self.PID_SP=0
            self.PID_CV=0
            self.looper=0
        def storereads(self,CV,SP):
            self.CV=np.append(self.CV,CV)
            self.SP=np.append(self.SP,SP)
        def storepv(self,PV):
            self.PV=np.append(self.PV,PV)       
        def reset(self):
            self.PV = np.zeros(0)
            self.CV = np.zeros(0)
            self.SP = np.zeros(0)
            self.scanCount=0
        def plc(self,ip):
            self.comm = Client(ip)

    def fopdtsetup():
        process.Gain=float(modelgain.get())
        process.TimeConstant=float(modeltc.get())*10
        process.DeadTime=float(modeldt.get())*10
        process.Bias=float(ambient.get())
        process.t=0
        gData.reset()
        gData.livetrend=1
        spstatus.set("")
        pvstatus.set("")
        cvstatus.set("")
        gData.plc(ip.get())            
        gData.comm.connect() 
        button_start["state"] = "disabled"
        button_stop["state"] = "normal"
        button_trend["state"] = "normal"
        button_save["state"] = "normal"
        ip.configure(state="disabled")
        modelgain.configure(state="disabled")
        modeltc.configure(state="disabled")
        modeldt.configure(state="disabled")
        ambient.configure(state="disabled")
        gData.PID_PV = gData.comm.get_node(pvtag.get())
        gData.PID_CV = gData.comm.get_node(cvtag.get())
        gData.PID_SP = gData.comm.get_node(sptag.get())

    def thread_start():    
        gData.looper = g.PeriodicInterval(start, 0.1)

    def start():
        try:
            #Setup tags to read        
            gData.PID_CV.read_value()
            gData.PID_SP.read_value()            

            actualcv=round(gData.PID_CV.read_value(),2)
            cvtext.set(actualcv)         
            cvtag.configure(state="disabled")

            actualsp=round(gData.PID_SP.read_value(),2)
            sptext.set(actualsp)
            sptag.configure(state="disabled")

            #Send CV to Process
            process.CV=gData.CV
            #Store Data when it is read
            gData.storereads(actualcv,actualsp)
            ts=[gData.scanCount,gData.scanCount+1]

            #Get new PV value
            if gData.PV.size>1:
                pv=process.update(gData.PV[-1],ts)
            else:
                pv=process.update(float(ambient.get()),ts)
            #Add Noise between -0.1 and 0.1
            noise=(random.randint(0,10)/100)-0.05
            #Store PV
            gData.storepv(pv[0]+noise)
            #Write PV to PLC   
            pv=float(pv[0])
            gData.PID_PV.write_attribute(ua.AttributeIds.Value, ua.DataValue(pv))
            pvtext.set(round(gData.PID_PV.read_value(),2))         
            pvtag.configure(state="disabled")

            gData.scanCount+=1
        
        except Exception as e:
            spstatus.set('An exception occurred: {}'.format(e))     
            pvstatus.set('An exception occurred: {}'.format(e))     
            cvstatus.set('An exception occurred: {}'.format(e))     
        
    def stop():
        gData.looper.stop()
        gData.looper.join(0.1)
        button_start["state"] = "normal"
        button_stop["state"] = "disabled"
        ip.configure(state="normal")
        modelgain.configure(state="normal")
        modeltc.configure(state="normal")
        modeldt.configure(state="normal")
        pvtag.configure(state="normal")
        cvtag.configure(state="normal")
        sptag.configure(state="normal")
        ambient.configure(state="normal")       
        gData.livetrend=0
        gData.comm.disconnect()
        
    def livetrend(): 
        #Set up the figure
        fig = plt.figure()
        ax = plt.axes(xlim=(0,100),ylim=(0, 100))
        SP, = ax.plot([], [], lw=2, color="Red", label='SP')
        CV, = ax.plot([], [], lw=2, color="Green", label='CV')
        PV, = ax.plot([], [], lw=2, color="Blue", label='PV')

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
            scale = 600 #Convert mS to Minutes
            x=x/scale
            ax.set_xlim(0,max(x)*1.1)
            max_y=max(max(gData.PV),max(gData.CV),max(gData.SP))
            min_y=min(min(gData.PV),min(gData.CV),min(gData.SP))
            ax.set_ylim(min_y-1,max_y+1)
            SP.set_data(x,gData.SP)
            CV.set_data(x,gData.CV)
            PV.set_data(x,gData.PV)
            return SP,PV,CV,

        #Live Data
        if gData.livetrend:
            anim = animation.FuncAnimation(fig, animate, init_func=init, frames=100, interval=1000) #, blit=True) # cant use blit with dynamic x-axis

        plt.show()
    
    def save():            
        if len(gData.PV):
            now=time.strftime("%Y%m%d_%H%M%S")
            np.savetxt("SimData_" + now + ".csv", np.transpose((gData.PV,gData.CV,gData.SP)), header="PV;CV;SP", comments='', fmt='%1.3f', delimiter = ";")
        else:
            button_save["state"] = "disabled"
    #Gui
    root = tk.Tk()
    root.title('OPC-UA PID Process Simulator using a FOPDT Model')
    root.resizable(True, True)
    root.geometry('520x325')

    #Text tags setup
    pvtext = tk.StringVar()
    cvtext = tk.StringVar()
    sptext = tk.StringVar()
    pvstatus = tk.StringVar()
    cvstatus = tk.StringVar()
    spstatus = tk.StringVar()
    pvtag = tk.Entry(root,width=25)
    cvtag = tk.Entry(root,width=25)
    sptag = tk.Entry(root,width=25)
    ip = tk.Entry(root,width=25)
    modelgain = tk.Entry(root,width=5)
    modeltc = tk.Entry(root,width=5)
    modeldt = tk.Entry(root,width=5)
    ambient = tk.Entry(root,width=5)

    #Column 0
    #Labels
    tk.Label(root, text="Tag").grid(row=0,column=0,padx=10 ,pady=2,sticky="NESW")
    tk.Label(root, text="SP:").grid(row=1,column=0,padx=10 ,pady=2,sticky="NESW")
    tk.Label(root, text="PV:").grid(row=2,column=0,padx=10 ,pady=2,sticky="NESW")
    tk.Label(root, text="CV:").grid(row=3,column=0,padx=10 ,pady=2,sticky="NESW")
    #Row 4 = Button
    #Row 5 = Button
    tk.Label(root, text="PLC OPC-UA Address:").grid(row=6,column=0,padx=10 ,pady=2)
    tk.Label(root, text="Model Gain:").grid(row=7,column=0,padx=10 ,pady=2,sticky="NESW")
    tk.Label(root, text="Model TimeConstant(s):").grid(row=8,column=0,padx=10 ,pady=2,sticky="NESW")
    tk.Label(root, text="Model DeadTime(s):").grid(row=9,column=0,padx=10 ,pady=2,sticky="NESW")
    tk.Label(root, text="Model Ambient:").grid(row=10,column=0,padx=10 ,pady=2,sticky="NESW")

    #Column 1
    #Labels
    tk.Label(root, text="Value").grid(row=0,column=1,padx=10 ,pady=2,sticky="NESW")
    tk.Label(root, textvariable=sptext).grid(row=1,column=1,padx=10 ,pady=2,sticky="NESW")
    tk.Label(root, textvariable=pvtext).grid(row=2,column=1,padx=10 ,pady=2,sticky="NESW")
    tk.Label(root, textvariable=cvtext).grid(row=3,column=1,padx=10 ,pady=2,sticky="NESW")
    #Row 4 = Button
    #Row 5 = Button
    ip.grid(row=6, column=1,columnspan=2,padx=10 ,pady=2,sticky="NESW")
    modelgain.grid(row=7, column=1,columnspan=1,padx=10 ,pady=2,sticky="NESW")
    modeltc.grid(row=8, column=1,columnspan=1,padx=10 ,pady=2,sticky="NESW")
    modeldt.grid(row=9, column=1,columnspan=1,padx=10 ,pady=2,sticky="NESW")
    ambient.grid(row=10, column=1,columnspan=1,padx=10 ,pady=2,sticky="NESW")

    #Column 2
    #Actual PLC TagName
    tk.Label(root, text="OPC-UA Tagname").grid(row=0,column=2,padx=10 ,pady=2)
    sptag.grid(row=1, column=2,padx=10 ,pady=2,sticky="NESW")
    pvtag.grid(row=2, column=2,padx=10 ,pady=2,sticky="NESW")
    cvtag.grid(row=3, column=2,padx=10 ,pady=2,sticky="NESW")

    #Column 3
    #Status
    tk.Label(root, text="Last Error:").grid(row=0,column=3,padx=10,columnspan=3 ,pady=2,sticky="W")
    tk.Label(root, textvariable=spstatus).grid(row=1,column=3,padx=10,columnspan=3 ,pady=2,sticky="W")
    tk.Label(root, textvariable=pvstatus).grid(row=2,column=3,padx=10,columnspan=3 ,pady=2,sticky="W")
    tk.Label(root, textvariable=cvstatus).grid(row=3,column=3,padx=10,columnspan=3 ,pady=2,sticky="W")

    #Default Values
    sptag.insert(0, "ns=2;s=Channel1.Device1.PID_SP")
    pvtag.insert(0, "ns=2;s=Channel1.Device1.PID_PV")
    cvtag.insert(0, "ns=2;s=Channel1.Device1.PID_CV")
    ip.insert(0, "opc.tcp://192.168.123.100:49320")    
    modelgain.insert(0, "1.75")
    modeltc.insert(0, "75.5")
    modeldt.insert(0, "17.66")
    ambient.insert(0, "13.5")

    #Buttons
    #Start Button Placement
    button_start = tk.Button(root, text="Start Simulator", command=lambda :[fopdtsetup(),thread_start()])
    button_start.grid(row=4,column=0,columnspan=1,padx=10 ,pady=2,sticky="NESW")

    #Stop Button Placement
    button_stop = tk.Button(root, text="Stop Simulator", command=lambda :[stop()])
    button_stop.grid(row=4,column=1,columnspan=1,padx=10 ,pady=2,sticky="NESW")
    button_stop["state"] = "disabled"

    #Trend Button Placement
    button_trend = tk.Button(root, text="Show Trend", command=lambda :[livetrend()])
    button_trend.grid(row=5,column=0,columnspan=2,padx=10 ,pady=2,sticky="NESW")
    button_trend["state"] = "disabled"

    button_save = tk.Button(root, text="Save as CSV", command=lambda :[save()])
    button_save.grid(row=11,column=2,columnspan=1,padx=10 ,pady=2,sticky="NESW")
    button_save["state"] = "disabled"

    #default setup 
    params=0
    model= (modelgain.get(),modeltc.get()*10,modeldt.get()*10,13.1)
    process=g.FOPDTModel(params, model)
    gData=data()

    root.mainloop()

if __name__ == '__main__':
    main()