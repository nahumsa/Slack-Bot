def parse_text_greeting(text, word='Hello'):
    """ Parse recieved text to return a greeting.

    Args:
        text (string): string recieved from slack POST.
        word (str, optional): Word that you want in your text. Defaults to 'Hello'.

    Returns:
        string: Returns a string with a greeting or another if the greeting
        is not in the text

    """
    special_characters = [' ', '!', '.', ',']
    for char in special_characters:
        if word in text.split(char):
            return "Hi, Human!"
    return "I can't Understand you."