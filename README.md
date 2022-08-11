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








To launch use:
```
from pytuneOPC.pidlogger import plclogger

clxlogger.main()
    
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







Reverse Acting:







To launch use:
```
from pytunelogix.simulate import simulator

simulator.main()
    
```


_________________________________________________________________________________________________________________________
**FOPDT Process Simulator (PID Simulator) for PLC using OPC-UA**


Simulates a Process:






To launch use:
```
from pytuneOPC.plcpidsim import clxsim

plcsim.main()
    
```


Windows Exe:


![Pytunelogix](https://user-images.githubusercontent.com/92536730/183046630-5fb861b3-9824-4276-b7f5-1afa51b1236c.PNG)
