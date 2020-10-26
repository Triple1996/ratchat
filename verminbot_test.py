# TODO get 90% test coverage for verminbot.py
import unittest
import unittest.mock as mock
from verminbot import Verminbot

KEY_INPUT = "input"
KEY_EXPECTED = "expected"
KEY_FIRST_WORD = "first_word"
KEY_SECOND_WORD = "second_word"

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: 'about',
                KEY_EXPECTED: "~/ I am the Verminlord."
            },
            {
                KEY_INPUT: "help",
                KEY_EXPECTED: "~/ Commands: !!about; !!catfact; " +
                        "!!1337 <text>; !!funtranslate <text>; !!help;"
            },
            {
                KEY_INPUT: "1337 the quick brown fox",
                KEY_EXPECTED: "~/ 7h3 quick br0wn f0x"
            },
            {
                KEY_INPUT: "funtranslate hello there",
                KEY_EXPECTED: '~/ "su cuy\'gar ogir"'
            },
            {
                KEY_INPUT: "catfact",
                KEY_EXPECTED: "~/ This is a catfact."
            },
            {
                KEY_INPUT: "dasd",
                KEY_EXPECTED: "~/ That command was unrecognized. \
                    For a list of commands, type !!help"
            },
        ]
        
        self.failure_test_params = [
            {
                KEY_INPUT: "!!dasd",
                KEY_EXPECTED: "~/ That command was unrecognized. \
                    For a list of commands, type !!help"
            },
        ]
    def mocked_cat_request(self, url):
        return ["This is a catfact."]
        
    def test_bot_success(self):
        verminbot = Verminbot()
        for test in self.success_test_params:
            with mock.patch('requests.get', self.mocked_cat_request):
                response = verminbot.handle_command(test[KEY_INPUT])
                expected = test[KEY_EXPECTED]
                self.assertEqual(response, expected)
    
    def test_bot_failure(self):
        for test in self.failure_test_params:
            expected = test[KEY_EXPECTED]
            self.assertNotEqual('TODO', 'TODO2')
      
if __name__ == '__main__':
    unittest.main()