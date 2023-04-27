
# BITS WILP Assignemnt S2-22_SSZG526 Distributed Systems - Abhishek Jha (2022MT13029)

###### The objective of this process is to simulate a mocked distributed computing environment, where multiple process share resources. The program uses the **Chandy-Misra-Haas**  Deadlock detection algorithm for AND-Model

<br>
<br>

### Requirements
---
**Programing Language** : Python 3  (>= 3.6)
**OS**                  : Any

<br>

#### Running the Simulation
---
1. Change the working directory to the project folder
```cd ds_assignment```
such that  you see the following contents in the directory
```
    ├── deadlock_detection
    │   ├── __init__.py
    │   └── simulator.py
    ├── main.py
    ├── README.md
    └── requirements.txt

    1 directory, 5 files
```

2. Install the reqeuirements
   ```pip install requirements.txt```

3. Run the simulation using the cli
   ```python main.py --num_resources <NUMBER_OF_PROCESS> --num_process <NUMBER_OF_RESOURCES>```
   script details can be obtained using the following command
   ```
    [abhi17@abhishekjha-ds-assignment ds_assignemnt]$ python3 main.py --help
    usage: main.py [-h] [-n NUM_PROCESSES] [-m NUM_RESOURCES]

    optional arguments:
    -h, --help            show this help message and exit
    -n NUM_PROCESSES, --num_processes NUM_PROCESSES
                        number of processes to be used in the simualtion
    -m NUM_RESOURCES, --num_resources NUM_RESOURCES
                        number of resources to be used in the simulation
    [abhi17@abhishekjha-ds-assignment ds_assignemnt]$ 
    ```


#### Output
---

The simulation writes the deadlock detection related messages to the stdout while the process level messages are written to the `simulation.log` file that is created in the same directory.

##### Sample STDOUT Output


```
[abhi17@abhishekjha-ds-assignment ds_assignemnt]$ python3 main.py -n 10 -m 5
created 5 resources: [<deadlock_detection.simulator.Resource object at 0x7fd1355827b8>, <deadlock_detection.simulator.Resource object at 0x7fd12d7a7e10>, <deadlock_detection.simulator.Resource object at 0x7fd12b420780>, <deadlock_detection.simulator.Resource object at 0x7fd12b420748>, <deadlock_detection.simulator.Resource object at 0x7fd12b4207b8>]
created 10 processes: [<ProcessNode(Thread-1, initial)>, <ProcessNode(Thread-2, initial)>, <ProcessNode(Thread-3, initial)>, <ProcessNode(Thread-4, initial)>, <ProcessNode(Thread-5, initial)>, <ProcessNode(Thread-6, initial)>, <ProcessNode(Thread-7, initial)>, <ProcessNode(Thread-8, initial)>, <ProcessNode(Thread-9, initial)>, <ProcessNode(Thread-10, initial)>]
process 2 initiating deadlock detection
Deadlock detected by process 2
process 2 performing Harakiri to break the deadlock
```

##### Sample log output

```
2023-04-27 16:18:26,595 starting process 1
2023-04-27 16:18:26,595 (Process 1) has requested for resource (Resource 2)
2023-04-27 16:18:26,595 assigning resource (Resource 2) to process (Process 1)
2023-04-27 16:18:26,596 starting process 2
2023-04-27 16:18:26,596 starting process 3
2023-04-27 16:18:31,601 (Process 1)'s resource request for (Resource 2) has timedout
2023-04-27 16:18:31,601 (Process 2) has requested for resource (Resource 1)
2023-04-27 16:18:31,601 assigning resource (Resource 1) to process (Process 2)
2023-04-27 16:18:31,601 (Process 1) sending probe message to (Process 1)
2023-04-27 16:18:36,604 (Process 1) has received probe ProbeMessage(initiator=1, sender=1, receiver=1)
2023-04-27 16:18:36,604 (Process 1) has released reource (Resource 2)
2023-04-27 16:18:36,606 (Process 2)'s resource request for (Resource 1) has timedout
2023-04-27 16:18:36,606 (Process 2) sending probe message to (Process 2)
2023-04-27 16:18:36,606 (Process 3) has requested for resource (Resource 2)
2023-04-27 16:18:36,606 assigning resource (Resource 2) to process (Process 3)
```





