import unittest
from app import app, API_KEY
from io import BytesIO
from PIL import Image
import base64

class ImageProcessingTests(unittest.TestCase):

    def test_process_resize(self):
        with app.test_client() as client:
            with open('tests/test.jpg', 'rb') as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
            response = client.post('/process',
                                headers={'api_key': API_KEY},
                                data={'image': (BytesIO(base64.b64decode(image_data)), 'test.jpg'), 'operation': 'resize', 'width': 100, 'height': 100},
                                content_type='multipart/form-data')
            self.assertEqual(response.status_code, 200)
            self.assertIn('image/jpeg', response.headers['Content-Type'])

    def test_process_compress(self):
        with app.test_client() as client:
            with open('tests/test.jpg', 'rb') as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
            response = client.post('/process',
                                headers={'api_key': API_KEY},
                                data={'image': (BytesIO(base64.b64decode(image_data)), 'test.jpg'), 'operation': 'compress', 'quality': 50},
                                content_type='multipart/form-data')
            self.assertEqual(response.status_code, 200)
            self.assertIn('image/jpeg', response.headers['Content-Type'])

    def test_process_watermark(self):
        with app.test_client() as client:
            with open('tests/test.jpg', 'rb') as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
            with open('tests/watermark.png', 'rb') as wf:
                watermark_data = base64.b64encode(wf.read()).decode('utf-8')
            response = client.post('/process',
                                headers={'api_key': API_KEY},
                                data={'image': (BytesIO(base64.b64decode(image_data)), 'test.jpg'), 'operation': 'watermark', 'watermark': watermark_data, 'opacity': 128, 'position': 'center'},
                                content_type='multipart/form-data')
            self.assertEqual(response.status_code, 200)
            self.assertIn('image/jpeg', response.headers['Content-Type'])

    def test_process_invalid_api_key(self):
        with app.test_client() as client:
            with open('tests/test.jpg', 'rb') as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
            response = client.post('/process',
                                data={'image': (BytesIO(base64.b64decode(image_data)), 'test.jpg'), 'operation': 'resize', 'width': 100, 'height': 100},
                                content_type='multipart/form-data')
            self.assertEqual(response.status_code, 401)

    def test_process_no_image(self):
        with app.test_client() as client:
            response = client.post('/process',
                                headers={'api_key': API_KEY},
                                data={'operation': 'resize', 'width': 100, 'height': 100},
                                content_type='multipart/form-data')
            self.assertEqual(response.status_code, 400)

    def test_process_invalid_file_type(self):
        with app.test_client() as client:
            with open('tests/test.txt', 'rb') as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
            response = client.post('/process',
                                headers={'api_key': API_KEY},
                                data={'image': (BytesIO(base64.b64decode(image_data)), 'test.txt'), 'operation': 'resize', 'width': 100, 'height': 100},
                                content_type='multipart/form-data')
            self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
