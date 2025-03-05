from flask import Flask, request, send_file, jsonify
from flask_cors import CORS  # Add this
from PIL import Image
import io

app = Flask(__name__)
CORS(app)  # Enable CORS

@app.route('/convert', methods=['POST'])
def convert():
    try:
        if 'files' not in request.files:
            return jsonify({"error": "No files uploaded"}), 400

        files = request.files.getlist('files')
        if not files:
            return jsonify({"error": "No files selected"}), 400

        images = []
        for file in files:
            if file.filename == '':
                return jsonify({"error": "Empty filename"}), 400
            img = Image.open(file.stream)
            images.append(img)

        pdf_bytes = io.BytesIO()
        images[0].save(
            pdf_bytes,
            save_all=True,
            append_images=images[1:],
            format='PDF'
        )
        pdf_bytes.seek(0)
        return send_file(pdf_bytes, mimetype='application/pdf', download_name='converted.pdf')

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)