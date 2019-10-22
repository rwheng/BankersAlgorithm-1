from typing import List


class Process:
    def __init__(self, resource_allocation: List[int],
                 maximum_allocation: List[int]):
        """Initilize a process

        Args:
            resource_allocation (List[int]): Currently used resources
            maximum_allocation (List[int]): Maximum amount of resources
        """
        # Set the datamembers that are passed in
        self.resources = resource_allocation
        self.maximums = maximum_allocation

        # Calculate the need array
        self.needs = [self.maximums[i] - self.resources[i]
                      for i in range(len(self.maximums))]

        # Assume the process is not finished on initialization
        self.is_finished = False

    def can_run(self, available_resources: List[int]) -> bool:
        """Check if the process can run

        Args:
            available_resources (List[int]): Resources unallocated in system

        Returns:
            bool: If the process can currently run
        """
        # If the process is finished it cannot run
        if self.is_finished:
            return False

        # If any of the need variables exceed the available system resources
        # then return false
        for i in range(len(self.maximums)):
            if self.needs[i] > available_resources[i]:
                return False

        # If both of the checks pass then return true
        return True

    def request(self, request: List[int],
                available_resources: List[int]) -> bool:
        """Request new resources for the current process

        Args:
            request (List[int]): Request for the process
            available_resources (List[int]): Current system free resources

        Returns:
            bool: If the request was fulfilled
        """

        # If not all values in the array that contains the boolean expression
        # request_i <= available_i and request_i + resources_i <= maximum_i
        # and request_i + resources_i <= maximum_i >= 0
        # for all i in request are true then the request is invalid
        if not all([request[i] <= available_resources[i] and
                    request[i] + self.resources[i] <= self.maximums[i] and
                    request[i] + self.resources[i] >= 0
                    for i in range(len(request))]):
            return False

        # If the request is valid update the resources and need
        self.resources = [self.resources[i] + request[i]
                          for i in range(len(request))]
        self.needs = [self.maximums[i] - self.resources[i]
                      for i in range(len(self.maximums))]

        # Return true
        return True
