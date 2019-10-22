from typing import List
from typing import Tuple
import logging

logging.basicConfig(level=logging.DEBUG)


class BankersAlgorithm:
    def __init__(self, num_proc: int, num_res: int, resources: List[int],
                 allocation: List[List[int]], maximum: List[List[int]]):
        """Initialize the Bankers Algorithm

        Args:
            num_proc (int): Number of processes
            num_res (int): Number of resources
            resources (List[int]): Quantity of resources available
            allocation (List[List[int]]): Current resource allocation
                                          for processes
            maximum (List[List[int]]): Maximum possible resource allocation
        """

        # Update all of the datamembers
        self.num_proc = num_proc
        self.num_res = num_res
        self.resources = resources
        self.allocation = allocation
        self.maximum = maximum

    def calculate_available(self) -> List[int]:
        """Calculate the available array. This contains the number of
        free resources that are not allocated to a process. available[i] = k
        means that there are k instances of resource i free

        Returns:
            List[int]: a List, num_res long, that contains the avaiable
                       resource count
        """

        # Seed the list with all 0s
        available = [0] * self.num_res

        # Loop over all of the resources
        for i in range(self.num_res):
            # Set the available_i equal to the number of unallocated resources
            available[i] = (self.resources[i] -
                            sum([allocation[i] for allocation
                                 in self.allocation]))

        # Return the available array
        return available

    def calculate_need(self) -> List[List[int]]:
        """Calculate the need array. This contains the number of resources
        that a process could request. need[i][j] = k means that process i
        could request k more instances of resource j

        Returns:
            List[List[int]]: The need array
        """
        # Return Mat(maximum) - Mat(allocation)
        return [[self.maximum[i][j] - self.allocation[i][j]
                 for j in range(self.num_res)] for i in range(self.num_proc)]

    def request(self, proc_num: int, resource_req: List[int]) -> Tuple[bool, List[int], List[str]]:
        """Request for a process to be allocated extra resources

        Args:
            proc_num (int): Process number that the request is being made on
            resource_req (List[int]): Number of extra resources requested

        Returns:
            bool: If the request was carried out and the system is currently
                  in a safe state

        Raises:
            ValueError: If either the process number is out of range
        """
        # Check that the process number is not out of range
        if proc_num >= self.num_proc or proc_num < 0:
            raise ValueError("Requested process number: " +
                             f"{proc_num} is invalid")

        # Check that the resource request is of the correct size
        if len(resource_req) != self.num_res:
            raise ValueError("Length of resource request " +
                             f"{len(resource_req)} is not {self.num_res}")

        # Start logs for request
        logs = []

        # Calculate the need and available arrays
        need = self.calculate_need()
        available = self.calculate_available()

        # Set the flag for valid request to true
        valid_request = True

        # Check if any of the values of the request either go above
        # the maximum bound for the process or exceed the number
        # of available resources for the system
        for i in range(self.num_res):
            if (resource_req[i] > need[proc_num][i] or
                    resource_req[i] > available[i]):
                # If the request is invalid then log and set the flag
                valid_request = False
                break

        # If the request is valid then add the resources to the allocation
        # for that process. No need to update the need or available arrays
        # because they are recalculated during at each function where they
        # may be modified
        if valid_request:
            for i in range(self.num_res):
                self.allocation[proc_num][i] += resource_req[i]

        # Check if any of the allocations are below zero and that
        # the system is currently in a safe state
        is_safe, safe_seq, safety_logs = self.safety()
        if min(self.allocation[proc_num]) < 0 or not is_safe:
            # If the system is not safe then unset the valid flag and reset the
            # requested resources
            valid_request = False
            for i in range(self.num_res):
                self.allocation[proc_num][i] -= resource_req[i]

        # Return if the request was valid and the system is in a current safe
        # state
        return valid_request, safe_seq, logs + safety_logs

    def safety(self) -> Tuple[bool, List[int], List[str]]:
        """Check the safety of the current state of the system.

        Returns:
            Tuple[bool, List[int], List[str]]: 3-tuple containing if the
                                               system is safe, and if so
                                               the safe process order,
                                               and the logs to print on
                                               the screen
        """
        # Start all processes out as unfinished
        finish = [False] * self.num_proc

        # Calculate the current avaliable resources
        work = self.calculate_available()

        # Caclulate the number of resources each process could request
        need = self.calculate_need()

        # Set the flag for the loop
        done = False

        # Create a queue to store the process order
        process_order = []

        # Loop while the done flag is unset
        while(not done):
            # Find an index i such that both finish[i] == false and
            # need[i] <= work[i] for all i in need and work

            found_i = False
            for i in range(self.num_proc):
                if finish[i]:
                    continue

                can_do = True
                for j in range(self.num_res):
                    if need[i][j] <= work[j]:
                        continue
                    else:
                        can_do = False
                        break

                if can_do:
                    found_i = True
                    process_order.append(i)
                    finish[i] = True
                    for j in range(self.num_res):
                        work[j] += self.allocation[i][j]
                    break

            if not found_i or min(finish):
                done = True

        return min(finish), process_order, ["Testing"]
