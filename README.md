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

_Assumes CV and PV data stored at 100ms intervals._



To launch use:
```
from pytunelogix.stage1 import csvtuner

csvtuner.main()

```

Direct Acting:

![U_Tune](https://user-images.githubusercontent.com/92536730/179394923-8757a7b9-d1d6-482b-8bd3-8b4769937206.PNG)



Reverse Acting:

![U_TuneR](https://user-images.githubusercontent.com/92536730/179394927-d35f3e2f-943c-41cc-bfff-cfee028a821f.PNG)




_________________________________________________________________________________________________________________________
**Stage 2 - Open loop tune**





https://user-images.githubusercontent.com/92536730/175918442-017d18a0-0bac-434d-aa44-b8cd3aebe231.mp4




```

WIP

```



_________________________________________________________________________________________________________________________
**Stage 3 - Closed loop tune**



https://user-images.githubusercontent.com/92536730/175920990-3fc2cb66-9d08-4c67-aff7-ff410345f9a5.mp4




```

WIP

```



_________________________________________________________________________________________________________________________
**Stage 4 - Adaptive tuner**




https://user-images.githubusercontent.com/92536730/175921177-86389b8f-2d3c-4dc7-8949-db4cdd782d84.mp4




```

WIP

```

_________________________________________________________________________________________________________________________
**PID Simulator**


Direct Acting:




![SimA](https://user-images.githubusercontent.com/92536730/184158772-930a5a03-c6c9-4587-91f7-919cd2301f4b.PNG)





![SimB](https://user-images.githubusercontent.com/92536730/184158750-bdf044b2-5514-4ce0-a170-abfeb8f3bc2f.PNG)






To launch use:
```
from pytunelogix.simulate import simulator

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


![image](https://user-images.githubusercontent.com/92536730/184161990-c221eec5-acc6-43b8-ad2f-85367814301a.png)
