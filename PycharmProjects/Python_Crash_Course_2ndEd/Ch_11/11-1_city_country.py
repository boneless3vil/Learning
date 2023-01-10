
import unittest
from city_functions import get_city_country


class TestCityCountry(unittest.TestCase):
    def test_city_country(self):
        laguna_america = get_city_country('laguna Niguel', 'america')

        self.assertEqual(laguna_america, 'Laguna Niguel, America')


if __name__ == '__main__':
    unittest.main()
