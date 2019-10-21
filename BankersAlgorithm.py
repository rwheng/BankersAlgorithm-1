from typing import List



class BankersAlgorithm:
    def __init__(self, num_proc: int, num_rec: int, resources: List[int],
                 allocation: List[List[int]], maximum: List[List[int]]):
        self.num_proc = num_proc
        self.num_rec = num_rec
        self.resources = resources
        self.allocation = allocation
        self.maximum = maximum
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

    def safety(self):
        finish = [False] * self.num_proc
        work = self.calculate_available()
        need = self.calculate_need()
        done = False

        # Loop while all of finish is not true
        while(not done):
            # Find an index i such that both finish[i] == false and need[i] <= work
            found_i = False
            for i in range(self.num_proc):
                if not finish[i] and need[i] <= work[i]:
                    work[i] = [self.allocation[i][j] + work[i][j] for j in len(self.allocation[i])]
                    found_i = True

            if not found_i: 
                done = True

        print(finish)





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
