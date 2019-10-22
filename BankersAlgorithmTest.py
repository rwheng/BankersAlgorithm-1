import unittest
from BankersAlgorithm import BankersAlgorithm as ba


class BankersAlgorithmTestCases(unittest.TestCase):
    def setUp(self):
        """Set up the Bankers Algorithm object with the data from the
        text file given to us by Dr. Kim
        """
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

    def test_need_calculation_is_valid(self):
        """Test that the calculation for the need array is producing the
        correct response
        """
        # Define the correct array response
        correct_need_array = [[7, 4, 3],
                              [1, 2, 2],
                              [6, 0, 0],
                              [0, 1, 1],
                              [4, 3, 1]]

        # Assert that they are equal
        self.assertEqual(self.b.calculate_need(), correct_need_array)

    def test_available_calculation_is_valid(self):
        """Test that the calculation for the available array is producing
        correct response
        """
        # Define the correct array response
        correct_available_array = [3, 3, 2]

        # Assert that they are equal
        self.assertEqual(self.b.calculate_available(), correct_available_array)

    def test_invalid_process_number_in_request(self):
        """Test that giving an invalid (read: out of range) process number
        will raise a ValueError
        """
        with self.assertRaises(ValueError):
            # Out of range above
            self.b.request(3, [1, 0, 0])
            # Out of range below
            self.b.request(-1, [1, 0, 0])

    def test_invalid_resource_length_in_request(self):
        """Test that giving an invalid (read: wrong length) array will raise
        a ValueError
        """
        with self.assertRaises(ValueError):
            # Too long
            self.b.request(0, [0, 1, 1, 1])
            # Too short
            self.b.request(0, [0, 1])

    def test_request_exceeds_process_maximum_allocation(self):
        """Test that giving a process request that exceeds the given
        maximal process resources will return false and not request
        those resources
        """
        # Assert that an invalid request returns false because
        # it goes above the maximum allocation
        self.assertFalse(self.b.request(0, [8, 0, 0])[0])
        # Assert that the allocation for process 0 didn't go through
        self.assertEqual(self.b.allocation[0], [0, 1, 0])

    def test_request_deceeds_zero(self):
        """Test that a request that brings the current allocation
        for a process below zero throws a ValueError
        """
        # Assert that a request that would put the resource allocation
        # below zero returns false
        self.assertFalse(self.b.request(0, [-1, 0, 0])[0])
        # Assert that the invalid allocation didn't go through
        self.assertEqual(self.b.allocation[0], [0, 1, 0])

    def test_request_puts_system_in_unsafe_state(self):
        """Test that a request that puts the system into an unsafe
        state will not be carried out
        """
        self.assertFalse(self.b.request(4, [3, 3, 0])[0])
        self.assertEqual(self.b.allocation[4], [0, 0, 2])

    def test_valid_request(self):
        """Test that giving a valid request changes the allocation,
        available, and need arrays correctly
        """
        # Assert that the correct request returns true
        self.assertTrue(self.b.request(0, [0, 2, 0]))
        # Assert that the allocation has been reflected in the object
        self.assertEqual(self.b.allocation[0], [0, 3, 0])

    def test_safe_safety_sequence(self):
        """Test that a safe sequence does exist for the current Bankers
        Algorithm configuration and that it is in fact a valid sequence
        """
        # Query the safety of the configuration
        is_safe, safe_seq, _ = self.b.safety()

        # Assert that the configuration is tested as safe
        self.assertTrue(is_safe)

        # Check if the sequence can actually run
        for process in safe_seq:
            # For each allocation for process p assert that each of
            # the allocations are less than the current available
            # system resources
            for i in range(self.b.num_res):
                self.assertLess(self.b.allocation[process][i],
                                self.b.resources[i])

            # When the process is complete free the process resources
            # into the system pool
            for i in range(self.b.num_res):
                self.b.resources[i] += self.b.allocation[process][i]

    def test_num_proc_must_be_int(self):
        with self.assertRaises(ValueError):
            self.b = ba("a", 3, [10, 5, 7],
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

    def test_num_res_must_be_int(self):
        with self.assertRaises(ValueError):
            self.b = ba(5, "a", [10, 5, 7],
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

    def test_res_array_must_be_right_size(self):
        with self.assertRaises(ValueError):
            self.b = ba(5, 3, [10, 5, 7, 30],
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
        with self.assertRaises(ValueError):
            self.b = ba(5, 3, [10, 5],
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

    def test_res_array_must_be_all_ints(self):
        with self.assertRaises(ValueError):
            self.b = ba(5, 3, [10, 5, "a"],
                        [[0, 1, 0],
                         [2, 0, 0],
                         [3, 0, 2],
                         [0, 0, 2]],
                        [[7, 5, 3],
                         [3, 2, 2],
                         [9, 0, 2],
                         [2, 2, 2],
                         [4, 3, 3]])

    def test_alloc_array_must_have_proc_num_rows(self):
        with self.assertRaises(ValueError):
            self.b = ba(5, 3, [10, 5, 7, 30],
                        [[0, 1, 0],
                         [2, 0, 0],
                         [3, 0, 2],
                         [0, 0, 2]],
                        [[7, 5, 3],
                         [3, 2, 2],
                         [9, 0, 2],
                         [2, 2, 2],
                         [4, 3, 3]])

        with self.assertRaises(ValueError):
            self.b = ba(5, 3, [10, 5, 7, 30],
                        [[0, 1, 0],
                         [2, 0, 0],
                         [3, 0, 2],
                         [2, 1, 1],
                         [0, 0, 0],
                         [0, 0, 2]],
                        [[7, 5, 3],
                         [3, 2, 2],
                         [9, 0, 2],
                         [2, 2, 2],
                         [4, 3, 3]])

    def test_alloc_array_must_have_res_num_cols(self):
        with self.assertRaises(ValueError):
            self.b = ba(5, 3, [10, 5, 7],
                        [[0, 0],
                         [2, 0],
                         [3, 2],
                         [2, 1],
                         [0, 2]],
                        [[7, 5, 3],
                         [3, 2, 2],
                         [9, 0, 2],
                         [2, 2, 2],
                         [4, 3, 3]])

        with self.assertRaises(ValueError):
            self.b = ba(5, 3, [10, 5, 7],
                        [[0, 1, 1, 0],
                         [2, 1, 1, 0],
                         [3, 1, 1, 2],
                         [2, 1, 1, 1],
                         [0, 1, 1, 2]],
                        [[7, 5, 3],
                         [3, 2, 2],
                         [9, 0, 2],
                         [2, 2, 2],
                         [4, 3, 3]])

    def test_alloc_array_must_be_all_ints(self):
        with self.assertRaises(ValueError):
            self.b = ba(5, 3, [10, 5, 7],
                        [[0, 1, 0],
                         [2, 0, 0],
                         [0, 0, 0],
                         [3, "a", 2],
                         [0, 0, 2]],
                        [[7, 5, 3],
                         [3, 2, 2],
                         [9, 0, 2],
                         [2, 2, 2],
                         [4, 3, 3]])

    def test_max_array_must_have_proc_num_rows(self):
        with self.assertRaises(ValueError):
            self.b = ba(5, 3, [10, 5, 7],
                        [[0, 1, 0],
                         [2, 0, 0],
                         [3, 0, 2],
                         [2, 1, 1],
                         [0, 0, 2]],
                        [[7, 5, 3],
                         [3, 2, 2],
                         [9, 0, 2],
                         [0, 0, 0],
                         [2, 2, 2],
                         [4, 3, 3]])

        with self.assertRaises(ValueError):
            self.b = ba(5, 3, [10, 5, 7],
                        [[0, 1, 0],
                         [2, 0, 0],
                         [3, 0, 2],
                         [2, 1, 1],
                         [0, 0, 2]],
                        [[7, 5, 3],
                         [3, 2, 2],
                         [2, 2, 2],
                         [4, 3, 3]])

    def test_max_array_must_have_res_num_cols(self):
        with self.assertRaises(ValueError):
            self.b = ba(5, 3, [10, 5, 7],
                        [[0, 1, 0],
                         [2, 0, 0],
                         [3, 0, 2],
                         [2, 1, 1],
                         [0, 0, 2]],
                        [[7, 5, 0, 3],
                         [3, 2, 0, 2],
                         [9, 0, 0, 2],
                         [2, 2, 0, 2],
                         [4, 3, 0, 3]])
        with self.assertRaises(ValueError):
            self.b = ba(5, 3, [10, 5, 7],
                        [[0, 1, 0],
                         [2, 0, 0],
                         [3, 0, 2],
                         [2, 1, 1],
                         [0, 0, 2]],
                        [[7, 3],
                         [3, 2],
                         [9, 2],
                         [2, 2],
                         [4, 3]])

    def test_max_array_must_be_all_ints(self):
        with self.assertRaises(ValueError):
            self.b = ba(5, 3, [10, 5, 7],
                        [[0, 1, 0],
                         [2, 0, 0],
                         [3, 0, 2],
                         [0, 0, 0],
                         [0, 0, 2]],
                        [[7, 5, 3],
                         [3, 2, 2],
                         [9, "A", 2],
                         [2, 2, 2],
                         [4, 3, 3]])


if __name__ == "__main__":
    unittest.main()
