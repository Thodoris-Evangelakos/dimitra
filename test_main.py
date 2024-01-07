import unittest
from unittest.mock import patch, MagicMock
import main

class TestFindSeismoiPoints(unittest.TestCase):
    @patch('main.openSeismoiFile')
    @patch('main.loadPerifereies')
    def test_findSeismoiPoints(self, mock_loadPerifereies, mock_openSeismoiFile):
        # Mock the data returned by openSeismoiFile and loadPerifereies
        mock_seismos = [main.Seismos("-550", "0000000000.00", 1.5, 1.5, "0.", "6.8")]
        mock_openSeismoiFile.return_value = mock_seismos

        mock_perifereia = main.Perifereia("FID", "AREA", [((1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (1.0, 1.0))])
        mock_loadPerifereies.return_value = [mock_perifereia]

        # Redirect stdout to a string buffer to capture print statements
        with patch('builtins.print') as mock_print:
            main.findSeismoiPoints()

        # Check if the function prints the correct seismos, perifereia, and polygon
        mock_print.assert_any_call(mock_seismos[0])
        mock_print.assert_any_call(mock_perifereia)
        mock_print.assert_any_call(((1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (1.0, 1.0)))

if __name__ == '__main__':
    unittest.main()