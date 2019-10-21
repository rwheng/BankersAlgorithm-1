from typing import List
from typing import Tuple


class BankersAlgorithm:
    def __init__(self, num_proc: int, num_rec: int, resources: List[int],
                 allocation: List[List[int]], maximum: List[List[int]]):
        """Initialize the Bankers Algorithm

        Args:
            num_proc (int): Number of processes
            num_rec (int): Number of resources
            resources (List[int]): Quantity of resources available
            allocation (List[List[int]]): Current resource allocation
                                          for processes
            maximum (List[List[int]]): Maximum possible resource allocation
        """

        # Update all of the datamembers
        self.num_proc = num_proc
        self.num_rec = num_rec
        self.resources = resources
        self.allocation = allocation
        self.maximum = maximum

        # Check the safety of the current configuration
        self.safety()

    def calculate_available(self):
        available = [0] * self.num_rec
        for i in range(len(available)):
            available[i] = (self.resources[i] -
                            sum([allocation[i] for allocation
                                 in self.allocation]))
        return available

    def calculate_need(self):
        return [[self.maximum[i][j] - self.allocation[i][j]
                 for j in range(self.num_rec)] for i in range(self.num_proc)]

    def request(self, proc_num: int, resource_req: List[int]) -> bool:

    def safety(self) -> Tuple[bool, List[int]]:
        """Check the safety of the current state of the system.
        
        Returns:
            Tuple[bool, List[int]]: 2-tuple containing if the system is safe,
                                    and if so the safe process order
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
                for j in range(self.num_rec):
                    if need[i][j] > work[j]:
                        can_do = False

                if can_do:
                    print("Finishing: {}".format(i))
                    found_i = True
                    process_order.append(i)
                    finish[i] = True
                    for j in range(self.num_rec):
                        work[j] += need[i][j]
                    break

            if not found_i:
                done = True

        return min(finish), process_order



# 5         (Number of processes)
# 3         (Number of resource types)
# 10 5 7 (Number of instances for R0, R1, R2))
# 0 1 0   (Allocation for P0)
# 2 0 0   (Allocation for P1)
# 3 0 2   (Allocation for P2)
# 2 1 1   (Allocation for P3)
# 0 0 2   (Allocation for P4)
# 7 5 3   (Max for P0)
# 3 2 2   (Max for P1)
# 9 0 2   (Max for P2)
# 2 2 2   (Max for P3)
# 4 3 3   (Max for P4)
BankersAlgorithm(5, 3, [10, 5, 7],

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
