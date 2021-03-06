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

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.success_html_writer_params = [
            {
                KEY_INPUT: ['google.com'],
                KEY_EXPECTED: "<a href=https://google.com>google.com</a>",
            },
            {
                KEY_INPUT: ['.jpg'],
                KEY_EXPECTED: "<img src=.jpg className='chat-pictures' height= 90%; />",
            },
            {
                KEY_INPUT: ['https://google.com'],
                KEY_EXPECTED: "<a href=https://google.com>https://google.com</a>",
            }
        ]
        self.success_about_params = [
            {
                KEY_INPUT: 'about',
                KEY_EXPECTED: "~/ I am the Verminlord.",
            }
        ]
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
        self.success_auth_user_params = [
            {
                KEY_INPUT: {
                    "name": 'Billy',
                    "email": 'email@google.com',
                    "picurl": 'url'
                },
                KEY_EXPECTED: tables.AuthUser('Billy', tables.AuthUserType.GOOGLE, 'email@google.com', 'url')
            }
        ]
        self.success_chat_log_params = [
            {
                KEY_INPUT: {
                    "content": 'message content',
                    "user": 'Billy',
                    "picurl": 'url'
                },
                KEY_EXPECTED: tables.ChatLog('message content', 'Billy', 'url')
            }
        ]
        self.success_bot_white_space_params = [
            {
                KEY_INPUT: 'about ',
                KEY_EXPECTED: "~/ I am the Verminlord.",
            },
            {
                KEY_INPUT: ' about ',
                KEY_EXPECTED: "~/ I am the Verminlord.",
            },
        ]
        
        self.success_leet_command_params = [
            {
                KEY_INPUT: "1337 the quick brown fox",
                KEY_EXPECTED: "~/ 7h3 quick br0wn f0x",
            },
            {
                KEY_INPUT: "1337 Sally sells seashells",
                KEY_EXPECTED: "~/ 5411y 53115 5345h3115",
            },
            {
                KEY_INPUT: "1337Sally sells seashells",
                KEY_EXPECTED: "~/ 5411y 53115 5345h3115",
            }
        ]
        self.success_unrecognized_params = [
            {
                KEY_INPUT: "dasd",
                KEY_EXPECTED: "~/ That command was unrecognized. " +
                    "For a list of commands, type !!help",
            }
        ]
        self.success_help_params = [
            {
                KEY_INPUT: "help",
                KEY_EXPECTED: "~/ Commands: !!about; !!catfact; " +
                        "!!1337 <text>; !!funtranslate <text>; !!help;",
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
    
    def test_help_command(self):
        verminbot = Verminbot()
        for test in self.success_help_params:
            response = verminbot.handle_command(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]
            self.assertEqual(response, expected)
            
    def test_unrecognized_command(self):
        verminbot = Verminbot()
        for test in self.success_unrecognized_params:
            response = verminbot.handle_command(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]
            self.assertEqual(response, expected)
    
    def test_leet_command(self):
        verminbot = Verminbot()
        for test in self.success_leet_command_params:
            response = verminbot.handle_command(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]
            self.assertEqual(response, expected)
    
    def test_bot_success(self):
        verminbot = Verminbot()
        for test in self.success_about_params:
            response = verminbot.handle_command(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]
            self.assertEqual(response, expected)
            
    def test_bot_white_space_success(self):
        verminbot = Verminbot()
        for test in self.success_bot_white_space_params:
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
    
    def test_html_writer_success(self):
        htmlWriter = html_strings.HTMLStrings()
        for test in self.success_html_writer_params:
            messages = test[KEY_INPUT]
            htmlWriter.format_html(messages)
            expected = test[KEY_EXPECTED]
            self.assertEqual(messages[0], expected)

    def test_auth_user_entry(self):
        for test in self.success_auth_user_params:
            response = tables.AuthUser(test[KEY_INPUT]["name"], tables.AuthUserType.GOOGLE, test[KEY_INPUT]["email"], test[KEY_INPUT]["picurl"])
            expected = self.success_auth_user_params[0][KEY_EXPECTED]
            self.assertEqual(response.name, expected.name)
            self.assertEqual(response.auth_type, expected.auth_type)
            self.assertEqual(response.email, expected.email)
            self.assertEqual(response.picture_url, expected.picture_url)

    def test_chat_log_entry(self):
        for test in self.success_chat_log_params:
            response = tables.ChatLog(test[KEY_INPUT]["content"], test[KEY_INPUT]["user"], test[KEY_INPUT]["picurl"])
            expected = self.success_chat_log_params[0][KEY_EXPECTED]
            self.assertEqual(response.user, expected.user)
            self.assertEqual(response.content, expected.content)
            self.assertEqual(response.picture_url, expected.picture_url)
            
if __name__ == '__main__':
    unittest.main()