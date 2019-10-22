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

        # Check that everything is valid, if not throw a value error
        # explaining what's wrong
        if(type(self.num_proc) is not int):
            raise ValueError("Number of Processes must be an integer," +
                             f"{type(self.num_proc)} is not int.")

        if(type(self.num_res) is not int):
            raise ValueError("Number of Resources must be an integer," +
                             f"{type(self.num_res)} is not int.")

        if len(self.resources) != self.num_res:
            raise ValueError("Length of resource array must equal number " +
                             f"of resources, {len(self.resources)} is not " +
                             f" {self.num_res}")

        if len(self.allocation) != self.num_proc:
            raise ValueError("Rows of allocation matrix must equal number " +
                             f"of processes, {len(self.allocation)} is not " +
                             f" {self.num_proc}")

        if len(self.maximum) != self.num_proc:
            raise ValueError("Rows of maximum matrix must equal number " +
                             f"of processes, {len(self.maximum)} is not " +
                             f" {self.num_proc}")

        for i in range(self.num_proc):
            if len(self.allocation[i]) != self.num_res:
                raise ValueError("Cols of allocation matrix must equal " +
                                 f"number of resources, " +
                                 f"{len(self.allocation)} is not" +
                                 f" {self.num_res}")
            if len(self.maximum[i]) != self.num_res:
                raise ValueError("Cols of maximum matrix must equal number " +
                                 f"of resources, {len(self.maximum)} is not " +
                                 f" {self.num_res}")

        for i in range(self.num_proc):
            for j in range(self.num_res):
                if type(self.allocation[i][j]) is not int:
                    raise ValueError("All values in allocation matrix should" +
                                     " be of type int. " +
                                     f"{type(self.allocation[i][j])}" +
                                     f" at {i},{j} is not int")
                if type(self.maximum[i][j]) is not int:
                    raise ValueError("All values in maximum matrix should" +
                                     " be of type int. " +
                                     f"{type(self.allocation[i][j])}" +
                                     f" at {i},{j} is not int")



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

    def request(self, proc_num: int,
                resource_req: List[int]) -> Tuple[bool, List[int], List[str]]:
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
                logs.append(f"Process request of resource_{i} unable " +
                            "to be fulfulled, not enough resources")
                # If the request is invalid then log and set the flag
                valid_request = False
                break

        # If the request is valid then add the resources to the allocation
        # for that process. No need to update the need or available arrays
        # because they are recalculated during at each function where they
        # may be modified
        safe_seq = []
        if valid_request:
            logs.append("Valid Request. Adding new process resources")
            for i in range(self.num_res):
                self.allocation[proc_num][i] += resource_req[i]

            # Check if any of the allocations are below zero and that
            # the system is currently in a safe state
            logs.append("Checking system safety")
            is_safe, safe_seq, safety_logs = self.safety()
            logs += safety_logs
            if min(self.allocation[proc_num]) < 0 or not is_safe:
                if not is_safe:
                    logs.append("Resource request puts system in unsafe " +
                                "state. Resetting to last known good")
                if min(self.allocation[proc_num]) < 0:
                    logs.append("Resource request allocated below 0 " +
                                "resources. Resetting to last known good")
                # If the system is not safe then unset the valid flag
                # and reset the requested resources
                valid_request = False
                for i in range(self.num_res):
                    self.allocation[proc_num][i] -= resource_req[i]

            if is_safe:
                logs.append("System is safe with new resource allocation")

        # Return if the request was valid and the system is in a current safe
        # state
        return valid_request, safe_seq, logs


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

        # Define an array for the logs
        logs = []

        # Loop while the done flag is unset
        while(not done):
            # Find an index i such that both finish[i] == false and
            # need[i] <= work[i] for all i in need and work

            found_i = False
            for i in range(self.num_proc):
                if finish[i]:
                    continue

                logs.append(f"Checking proc {i}")
                can_do = True
                for j in range(self.num_res):
                    if need[i][j] <= work[j]:
                        continue
                    else:
                        can_do = False
                        break

                if can_do:
                    logs.append(f"Executing proc {i}")
                    found_i = True
                    process_order.append(i)
                    finish[i] = True
                    for j in range(self.num_res):
                        work[j] += self.allocation[i][j]
                    break

            if not found_i or min(finish):
                if not found_i:
                    logs.append("No more processes are able to execute")
                if min(finish):
                    logs.append("All processes are finished")
                done = True

        return min(finish), process_order, logs

if __name__ == '__main__':

    self.b = ba(5, 3, [10, 5, 7],
                [[0, 1, 0],
                 [2, 0, 0],
                 [3, 0, 2],
                 [2, 1, 1],
                 [0, 0, 2]],
                [[7, 5, 3],
                 [3, 2, 2],
                 [9, 0, 2],
                 [2, 2, 2],
                 [4, 3, 3]])
