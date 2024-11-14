from flask import Flask, request, send_file
import barcode
from barcode.writer import ImageWriter
import qrcode
from io import BytesIO

app = Flask(__name__)

@app.route('/generate-barcode', methods=['GET'])
def generate_barcode():
    text = request.args.get('text')
    barcode_type = request.args.get('type', 'code128')

    if barcode_type == 'qrcode':
        # Generate QR code
        qr = qrcode.make(text)
        img_io = BytesIO()
        qr.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')
    else:
        # Generate barcode
        barcode_class = barcode.get_barcode_class(barcode_type)
        img_io = BytesIO()
        barcode_class(text, writer=ImageWriter()).write(img_io)
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
