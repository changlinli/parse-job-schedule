import parse
import unittest

class TestParse(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_assets/test.xml"

    def test_partition_functon(self):
        test_list = [1, 2]
        partition = parse.binary_partition(test_list, lambda x: x == 1)
        self.assertEqual(partition, [[1], [2]])

    def test_returns_not_empty_list(self):
        companies = parse.gen_companies(self.test_file)
        self.assertNotEqual(companies, [])

    def test_view_already_applied_status(self):
        companies_partition = parse.gen_companies(self.test_file)
        self.assertNotEqual(companies_partition[0], [])
        already_applied = companies_partition[0]
        self.assertEqual(already_applied[0].find('name').text, 'Blah2')

if __name__ == "__main__":
    unittest.main()
