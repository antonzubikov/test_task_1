from flask import Flask, request, jsonify, send_file
from PIL import Image
from io import BytesIO
import base64
import os

app = Flask(__name__)

API_KEY = "YOUR_API_KEY"  # Замените на ваш API-ключ

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'bmp'}

def allowed_file(filename):
    return '.' in filename and
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_image(image_data, operation, **kwargs):
    image = Image.open(BytesIO(base64.b64decode(image_data)))

    if operation == 'resize':
        width = kwargs.get('width')
        height = kwargs.get('height')
        if width and height:
            image = image.resize((width, height))
        elif width:
            image = image.resize((width, int(image.height * width / image.width)))
        elif height:
            image = image.resize((int(image.width * height / image.height), height))
    elif operation == 'compress':
        quality = kwargs.get('quality')
        image = image.convert('RGB')  # Убираем alpha-канал для JPEG
        output = BytesIO()
        image.save(output, 'JPEG', quality=quality)
        image.close()
        return output.getvalue()
    elif operation == 'watermark':
        watermark = Image.open(BytesIO(base64.b64decode(kwargs.get('watermark'))))
        opacity = kwargs.get('opacity')
        position = kwargs.get('position')
        watermark = watermark.convert("RGBA")
        watermark = watermark.resize((int(image.width/5), int(image.height/5)))
        watermark = watermark.convert("RGBA")  # Ensure alpha channel for transparency
        watermark.putalpha(opacity)
        if position == 'center':
            x = (image.width - watermark.width) // 2
            y = (image.height - watermark.height) // 2
        else:
            x = 0
            y = 0  # Default top-left corner
        image.paste(watermark, (x, y), mask=watermark)
        output = BytesIO()
        image.save(output, image.format)
        image.close()
        return output.getvalue()

@app.route('/process', methods=['POST'])
def process():
    if 'api_key' not in request.headers or request.headers['api_key'] != API_KEY:
        return jsonify({'error': 'Invalid API key'}), 401

    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        image_data = file.read()
        image_data = base64.b64encode(image_data).decode('utf-8')

        operation = request.form.get('operation')
        if operation == 'resize':
            width = int(request.form.get('width', 0))
            height = int(request.form.get('height', 0))
            processed_data = process_image(image_data, operation, width=width, height=height)
        elif operation == 'compress':
            quality = int(request.form.get('quality', 80))
            processed_data = process_image(image_data, operation, quality=quality)
        elif operation == 'watermark':
            watermark_data = request.form.get('watermark')
            opacity = int(request.form.get('opacity', 128))
            position = request.form.get('position', 'center')
            processed_data = process_image(image_data, operation, watermark=watermark_data, opacity=opacity, position=position)
        else:
            return jsonify({'error': 'Invalid operation'}), 400

        if processed_data:
            response = send_file(BytesIO(processed_data), mimetype='image/' + file.filename.rsplit('.', 1)[1].lower(), as_attachment=True, download_name='processed_' + file.filename)
            return response
        else:
            return jsonify({'error': 'Error processing image'}), 500
    else:
        return jsonify({'error': 'File type not allowed'}), 400


if __name__ == '__main__':
    app.run(debug=True)