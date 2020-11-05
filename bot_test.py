import unittest
import bot
import helpers

class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.text_test = [('Hello',"Hi, Human!"), 
                          ('Hello.', "Hi, Human!"), 
                          ('Hello, friend.', "Hi, Human!"), 
                          ('Hello!', "Hi, Human!"),
                          ('onsdaionsad', "I can't Understand you."), 
                          ('Oi', "I can't Understand you.")]
        
        bot.app.testing = True
        self.app = bot.app.test_client()
    
    def test_message_count(self):
        response = self.app.get('/message-count')
        self.assertEqual(200, response.status_code, msg="Status Code Fail")

    def test_parse_text_greeting(self):
        for text, expected in self.text_test:
            self.assertEqual(helpers.parse_text_greeting(text), expected, msg="parse_text_greeting Fail")

if __name__ == '__main__':
    unittest.main()