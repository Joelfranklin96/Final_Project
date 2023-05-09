import unittest
import tempfile
from document_reader import read_pdf_content, save_pdf_content_to_db
from pymongo import MongoClient
import os
from bson.objectid import ObjectId

class TestDocumentReader(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_db_name = 'test_pdf_analysis'
        cls.client = MongoClient('127.0.0.1', 27017)
        cls.db = cls.client[cls.test_db_name]

    @classmethod
    def tearDownClass(cls):
        cls.client.drop_database(cls.test_db_name)

    def test_read_pdf_content(self):
        # Create a temporary PDF file with some content
        with tempfile.NamedTemporaryFile(suffix=".pdf") as temp_pdf:
            temp_pdf.write(b"This is a test PDF file.")
            temp_pdf.seek(0)

            content = read_pdf_content(temp_pdf.name)
            self.assertIsNotNone(content)
            self.assertTrue(isinstance(content, str))
            self.assertTrue(len(content) > 0)

    def test_save_pdf_content_to_db(self):
        # Create a temporary PDF file with some content
        with tempfile.NamedTemporaryFile(suffix=".pdf") as temp_pdf:
            temp_pdf.write(b"This is another test PDF file.")
            temp_pdf.seek(0)

            document_id = save_pdf_content_to_db(temp_pdf.name, self.db)
            self.assertIsNotNone(document_id)
            self.assertTrue(isinstance(document_id, ObjectId))

            # Check if the content is saved in the database
            document = self.db.documents.find_one({"_id": document_id})
            self.assertIsNotNone(document)
            self.assertIn('content', document)
            self.assertTrue(len(document['content']) > 0)

# Run the tests
if __name__ == '__main__':
    unittest.main()