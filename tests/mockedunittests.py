import unittest
import unittest.mock as mock
import sys
sys.path.insert(1, '../')
from verminbot import Verminbot
import html_strings
import tables

KEY_INPUT = "input"
KEY_EXPECTED = "expected"
KEY_CATFACT = "catfact"
KEY_TRANSLATED = "translated"
LONG_WORD = ""
for i in range (0, 196):
    LONG_WORD += 'i'
class AppTestCase(unittest.TestCase):
    def setUp(self):

        self.success_catfact_params = [
            {
                KEY_INPUT: "catfact",
                KEY_EXPECTED: "~/ This is a catfact.",
                KEY_CATFACT: "This is a catfact."
            }
        ]
        self.success_translate_params = [
            {
                KEY_INPUT: "funtranslate hello there",
                KEY_EXPECTED: '~/ "su cuy\'gar ogir"',
                KEY_TRANSLATED: '"su cuy\'gar ogir"'
            }
        ]
        self.success_long_translate_params = [
            {
                KEY_INPUT: "funtranslate",
                KEY_EXPECTED: "~/ Translation exceeded message capacity :(",
                KEY_TRANSLATED: LONG_WORD
            }    
        ]
        self.success_translate_error_params = [
            {
                KEY_INPUT: "funtranslate",
                KEY_EXPECTED: "~/ Too many translations, try again later"
            }
        ]

    def mocked_cat_request(self, response):
        json_response_mock = mock.Mock()
        json_response_mock().json.return_value = {"all" : [{"text" : response}] }
        return json_response_mock

    def mocked_translate_request(self, response):
        json_response_mock = mock.Mock()
        json_response_mock().json.return_value = {"contents" : {"translated" : response} }
        return json_response_mock
    
    def mocked_random_choice(self, values):
        return values[0]
        
    def mocked_translate_error_request(self):
        json_response_mock = mock.Mock()
        json_response_mock().json.return_value = {"KeyError" : "wrong"}
        return json_response_mock
        
    def test_too_many_translations(self):
        verminbot = Verminbot()
        for test in self.success_translate_error_params:
            with mock.patch('requests.get', self.mocked_translate_error_request()):
                response = verminbot.handle_command(test[KEY_INPUT])
                expected = test[KEY_EXPECTED]
                self.assertEqual(response, expected)
        
    def test_long_translation(self):
        verminbot = Verminbot()
        for test in self.success_long_translate_params:
            with mock.patch('requests.get', self.mocked_translate_request(test[KEY_TRANSLATED])):
                response = verminbot.handle_command(test[KEY_INPUT])
                expected = test[KEY_EXPECTED]
                self.assertEqual(response, expected)
        
    def test_catfact_success(self):
        verminbot = Verminbot()
        for test in self.success_catfact_params:
            with mock.patch('requests.get', self.mocked_cat_request(test[KEY_CATFACT])):
                response = verminbot.handle_command(test[KEY_INPUT])
                expected = test[KEY_EXPECTED]
                self.assertEqual(response, expected)
                
    def test_translate_success(self):
        verminbot = Verminbot()
        for test in self.success_translate_params:
            with mock.patch('requests.get', self.mocked_translate_request(test[KEY_TRANSLATED])):
                response = verminbot.handle_command(test[KEY_INPUT])
                expected = test[KEY_EXPECTED]
                self.assertEqual(response, expected)
                
if __name__ == '__main__':
    unittest.main()