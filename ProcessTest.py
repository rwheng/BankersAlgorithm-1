import unittest
from Process import Process as p


class ProcessTestCases(unittest.TestCase):
    def setUp(self):
        self.p = p([0, 1, 0], [10, 5, 3])

    def test_process_calculate_need(self):
        """Test if the process can correctly calculate need
        """
        self.assertEqual(self.p.needs, [10, 4, 3])

    def test_process_can_run(self):
        """Test that the process can correcty check if it can run, given
        a set of resources
        """
        # Check that the process can run with enough resources
        self.assertTrue(self.p.can_run([10, 4, 3]))

        # Check that the process can't run without enough resources
        self.assertFalse(self.p.can_run([9, 4, 3]))

        # Check that the process doesn't run if finished
        self.p.is_finished = True
        self.assertFalse(self.p.can_run([10, 4, 3]))

    def test_process_allocate_resources(self):
        """Test that the process can correctly determine if it should
        be allocated resources
        """
        # Assert that if the request goes over process max then it won't work
        self.assertFalse(self.p.request([11, 0, 1], [100, 100, 100]))
        # Assert that if the request goes over system max then it won't work
        self.assertFalse(self.p.request([10, 0, 0], [9, 0, 0]))
        # Assert that if a request put the process under 0 allocated resources
        # it wont work
        self.assertFalse(self.p.request([-1, 0, 0], [10, 10, 10]))

        # Assert that process request that passes both checks works and
        # changes the process allocation and need array
        self.assertTrue(self.p.request([10, 0, 0], [10, 0, 0]))
        self.assertEqual(self.p.resources, [10, 1, 0])


if __name__ == "__main__":
    unittest.main()
