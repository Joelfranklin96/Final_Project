import unittest
from document_analyzer import summarize_text, extract_keywords

class TestDocumentAnalyzer(unittest.TestCase):

    def test_summarize_text(self):
        content = "This is a test document. It has some text in it for testing purposes. We will test the summarizer function with this text."
        summary = summarize_text(content)
        self.assertIsNotNone(summary)
        self.assertTrue(isinstance(summary, str))
        self.assertTrue(len(summary) > 0)

    def test_extract_keywords(self):
        content = "This is another test document. It has some different text in it for testing purposes. We will test the keywords extraction function with this text."
        keywords = extract_keywords(content)
        self.assertIsNotNone(keywords)
        self.assertTrue(isinstance(keywords, list))
        self.assertTrue(len(keywords) > 0)

# Run the tests
if __name__ == '__main__':
    unittest.main()
