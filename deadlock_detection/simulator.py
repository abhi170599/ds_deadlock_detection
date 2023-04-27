"""
Python program to simulate resource sharing in a
Distributred Environment and apply Chandy-Misra-Haas Deadlock Detection Algorithm.
"""

import logging as log

from typing import List, Dict, Any

from time import time, sleep
from threading import Thread, Lock
from queue import Queue, Empty
from collections import namedtuple
from random import randint

PROCESS_NODE_RUN_TIME = 60
RESOURCE_REQUEST_TIMEOUT = 5
RESOURCE_USAGE_TIME = 10
PROCESS_SLEEP_TIME = 5

LOG_PATH = "simulation.log"
log.basicConfig(
    filename=LOG_PATH, level=log.DEBUG, format="%(asctime)s %(message)s", filemode="w"
)

ProbeMessage = namedtuple(
    typename="ProbeMessage", field_names=["initiator", "sender", "receiver"]
)

is_deadlock_detection_running = False
deadlock_detection_run_lock = Lock()


class Resource:
    """
    Class representing a resource in the Distributed Environment.
    """
    def __init__(self, resource_id: int) -> None:
        self.resource_id = resource_id
        self.assigned_to_process: ProcessNode = None
        self.lock = Lock()

    def assign_to_process_if_free(self, process: "ProcessNode") -> bool:
        """
        Assign resource to the given process if its free.
        """
        assigned = False
        with self.lock:
            if not self.assigned_to_process:
                log.info(f"assigning resource {self} to process {process}")
                self.assigned_to_process = process
                assigned = True

        return assigned

    def __str__(self) -> str:
        return f"(Resource {self.resource_id})"

    def get_holding_process(self) -> "ProcessNode":
        """
        Get the process instance that is currently using the resource.
        """
        with self.lock:
            process = self.assigned_to_process
        return process

    def release(self) -> None:
        """
        Release the process.
        """
        with self.lock:
            self.assigned_to_process = None


class ResourceRequest:
    """
    Class representing a resource reqeust made by a process.
    """

    def __init__(self, resource: Resource) -> None:
        self.resource = resource
        self.created_timestamp = time()

    def has_timedout(self) -> bool:
        """
        Check if this resource request has timedout
        """
        return (time() - self.created_timestamp) > RESOURCE_REQUEST_TIMEOUT


class ProcessNode(Thread):
    """
    Class to represent a process in the Distributed Environment.
    """

    def __init__(self, pid: int, available_resources: List[Resource]) -> None:
        super(ProcessNode, self).__init__()

        self.pid = pid
        self.message_queue = Queue()
        self.available_resources = available_resources
        self.resource_requests: List[ResourceRequest] = []

    def set_process_map(self, process_map: Dict[int, "ProcessNode"]) -> None:
        """
        add the global knowledge of existing processes to the ProcessNode.
        """
        self.process_map = process_map

    def _send_probe_message(self, pid_initiator, pid_receiver) -> None:
        """
        Simulate sending a probe message to the dependent tasks.
        """
        receiver_process_instance = self.process_map[pid_receiver]
        receiver_process_instance.add_message_to_queue(
            ProbeMessage(
                initiator=pid_initiator, sender=self.pid, receiver=pid_receiver
            )
        )

    def add_message_to_queue(self, message: ProbeMessage):
        """
        Function to add a message to the processes' message queue.
        """
        self.message_queue.put(message)

    def _get_random_resources(self) -> List[Resource]:
        """
        Get a list of random resources from the available resources.
        """
        num_resources = randint(0, len(self.available_resources) - 1)
        resources: List[Resource] = []
        index = randint(0, num_resources)
        for i in range(num_resources):
            resource = self.available_resources[index]
            resources.append(resource)
            index = (index + 1) % len(self.available_resources)

        return resources

    def request_random_resources(self) -> None:
        """
        Create request for random resources.
        """
        if not self.resource_requests:
            requested_resources = self._get_random_resources()
            for resource in requested_resources:
                log.info(f"{self} has requested for resource {resource}")
                self.resource_requests.append(ResourceRequest(resource))

    def release_resources(self, force=False) -> None:
        """
        Release the resources whose usage has been completed.
        if force is True, release the resources regardless of their usage status
        """
        if not self.resource_requests:
            return
        for resource_request in self.resource_requests:
            if force or (
                resource_request.resource.get_holding_process() == self
                and time() - resource_request.created_timestamp > RESOURCE_USAGE_TIME
            ):
                log.info(f"{self} has released reource {resource_request.resource}")
                resource_request.resource.release()
                self.resource_requests.remove(resource_request)

    def _send_probes_to_neighbours(self, initiator: int) -> None:
        """
        Send probe messages to all the neighbour processes.
        """
        # in Chandy-Misra-Haas algorithm, a neighbouring process is the one
        # that is holding the resource reqeusted by the current process.
        
        # Determine the neighbour processes and send a probe message to them
        for resource_request in self.resource_requests:
            if resource_request.has_timedout():
                holding_process = resource_request.resource.get_holding_process()
                log.info(f"{self} sending probe message to {holding_process}")
                self._send_probe_message(initiator, holding_process.pid)

    def initiate_deadlock_detection(self) -> None:
        """
        Initiate the Chandy-Misra-Haas Deadlock Detection algorithm.
        """

        skip = True
        with deadlock_detection_run_lock:
            global is_deadlock_detection_running
            if not is_deadlock_detection_running:
                is_deadlock_detection_running = True
                skip = False
        # if a deadlock detection algorithm instance is currently running
        # do not initate, skip.
        if skip:
            return

        print(f"process {self.pid} initiating deadlock detection")
        self._send_probes_to_neighbours(self.pid)

    def handle_probe_messages(self) -> bool:
        """
        Handle the incoming probe messages.
        """
        try:
            # receive a probe message
            probe_message: ProbeMessage = self.message_queue.get_nowait()
            log.info(f"{self} has received probe {probe_message}")

            # according the Chandy-Misra-Haas algorithm, if the 
            # initiator process receives back a probe message, then
            # the system is in deadlock as there is a cycle in the
            # WaitForGraph
            if probe_message.initiator == self.pid:
                print(f"Deadlock detected by process {self.pid}")
                with deadlock_detection_run_lock:
                    global is_deadlock_detection_running
                    is_deadlock_detection_running = False
                return True
            else:
                self._send_probes_to_neighbours(probe_message.initiator)
                return False
        except Empty:
            return False

    def harakiri(self) -> None:
        """
        To break the deadlock, let the initiator process perform Harakiri
        """
        # one of the ways to break the deadlock is to allow the initiator process to
        # kill itself, hence releasing its resources
        print(f"process {self.pid} performing Harakiri to break the deadlock")
        self.release_resources(force=True)

    def run(self) -> None:
        """
        Run the process node, simulating its behaviour in the distributed environment
        """
        node_start_time = time()
        log.info(f"starting process {self.pid}")
        while time() - node_start_time < PROCESS_NODE_RUN_TIME:
            # request random resources.
            self.request_random_resources()
            
            # handle incoming probe messages
            if self.handle_probe_messages():
                self.harakiri()
                return
            
            # flag to check if this process should start the deadlock detection algorithm.
            should_initiate_deadlock_detection = False

            # check if any resource request has timedout.
            for resource_request in self.resource_requests:
                if resource_request.resource.assign_to_process_if_free(self):
                    continue
                else:
                    if resource_request.has_timedout():
                        log.info(
                            f"{self}'s resource request for {resource_request.resource} has timedout"
                        )
                        should_initiate_deadlock_detection = True
                        break

            if should_initiate_deadlock_detection:
                self.initiate_deadlock_detection()
            else:
                self.release_resources()

            sleep(PROCESS_SLEEP_TIME)

    def __str__(self) -> str:
        return f"(Process {self.pid})"


def simulate(num_processes: int, num_resources: int) -> None:
    """
    Simualte a resource sharing session and deadlock detection
    in mocked distributed environment.
    """
    processes: List[ProcessNode] = []
    resources: List[Resource] = []

    process_map: Dict[int, ProcessNode] = {}

    # create the resources
    for i in range(num_resources):
        resource = Resource(resource_id=i + 1)
        resources.append(resource)

    print(f"created {num_resources} resources: {resources}")

    # create the processes
    for i in range(num_processes):
        process = ProcessNode(pid=i + 1, available_resources=resources)
        process_map[i + 1] = process
        processes.append(process)

    # udpate process maps for all the processes
    for process in processes:
        process.set_process_map(process_map=process_map)

    print(f"created {num_processes} processes: {processes}")

    # start the processes
    for process in processes:
        process.start()

    # wait for all the processes to end
    for process in processes:
        process.join()

