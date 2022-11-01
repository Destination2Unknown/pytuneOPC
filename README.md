# pytuneOPC
**Python PID Tuner using OPC-UA**

![PyPI](https://img.shields.io/pypi/v/pytuneOPC?label=pypi%20package)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pytuneOPC)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytuneOPC)
![GitHub repo size](https://img.shields.io/github/repo-size/destination2unknown/pytuneOPC)
![PyPI - License](https://img.shields.io/pypi/l/pytuneOPC)

Windows Exe (no install required) ->https://github.com/Destination2Unknown/pytuneOPC/releases

To install use:

```
pip install pytuneOPC
```


PID tuning in 4 Steps:
```
A-> Record PRC using Logger
B-> Tune using PID Tuner
C-> Refine tune using PID Simulator
D-> Test tune with FOPDT Simulator for PLC using OPC-UA
```


Create a launch file:

```
examplelaunch.pyw #use pyw for no console
```

_________________________________________________________________________________________________________________________
**PID Logger**



![OPCuaLog](https://user-images.githubusercontent.com/92536730/184158600-54fcf55c-1fe2-457d-a677-1b4664894b96.png)




To launch use:
```
from pytuneOPC.pidlogger import plclogger

plclogger.main()
    
```


_________________________________________________________________________________________________________________________
**Stage 1 - PID Tuner based on a CSV file of a Process Reaction Curve (PRC)**

> ***Notes and Limitations:***
>
> - _Assumes CV and PV data stored at 1 second intervals._
>
> - _Assumes there is a single step in CV._
>
> - _Ambient is calculated as an average of the PV prior to the step change._
>
> - _Doesn't work correctly with a ramp in CV or with multiple CV steps._
>
>


To launch use:
```
from pytuneOPC.stage1 import csvtuner

csvtuner.main()

```

Direct Acting:

![U_Tune](https://user-images.githubusercontent.com/92536730/179394923-8757a7b9-d1d6-482b-8bd3-8b4769937206.PNG)



Reverse Acting:

![U_TuneR](https://user-images.githubusercontent.com/92536730/179394927-d35f3e2f-943c-41cc-bfff-cfee028a821f.PNG)



_________________________________________________________________________________________________________________________
**PID Simulator**


Direct Acting:




![SimA](https://user-images.githubusercontent.com/92536730/184158772-930a5a03-c6c9-4587-91f7-919cd2301f4b.PNG)





![SimB](https://user-images.githubusercontent.com/92536730/184158750-bdf044b2-5514-4ce0-a170-abfeb8f3bc2f.PNG)






To launch use:
```
from pytuneOPC.simulate import simulator

simulator.main()
    
```


_________________________________________________________________________________________________________________________
**FOPDT Process Simulator (PID Simulator) for PLC using OPC-UA**


Simulates a Process:




![OPCuaSim](https://user-images.githubusercontent.com/92536730/184160541-6ea3234d-af96-4b89-81db-92dc13a68329.PNG)


To launch use:
```
from pytuneOPC.plcpidsim import plcsim

plcsim.main()
    
```


_________________________________________________________________________________________________________________________

Windows Exe:




![image](https://user-images.githubusercontent.com/92536730/199230955-83c7ec09-d215-4a93-9e5e-548147804698.png)

