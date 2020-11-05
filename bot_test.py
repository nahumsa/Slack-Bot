import unittest
import bot

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
        self.assertEqual(200, response.status_code, msg="Testing Endpoint")

    def test_parse_text_greeting(self):
        for text, expected in self.text_test:
            self.assertEqual(bot.parse_text_greeting(text), expected, msg="Testing parse_text_greeting")

if __name__ == '__main__':
    unittest.main()