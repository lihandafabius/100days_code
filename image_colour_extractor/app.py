from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import os
import cv2
import numpy as np
from collections import Counter
from sklearn.cluster import KMeans
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.secret_key = 'your_secret_key'  # Replace with a secure key in production

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_top_colors(image_path, num_colors=10):
    # Load the image and convert it to RGB
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Optionally reduce resolution here if needed
    # (Handled separately in the `reduce_image_resolution` function)

    # Reshape the image to a 2D array of pixels
    pixels = image.reshape((-1, 3))

    # Perform K-Means clustering to group colors
    kmeans = KMeans(n_clusters=num_colors, random_state=42)
    kmeans.fit(pixels)

    # Get the colors (cluster centers) and their respective counts
    colors = kmeans.cluster_centers_
    labels = kmeans.labels_

    # Count how many pixels belong to each cluster
    counts = Counter(labels)

    # Convert colors from floats to integers and ensure native Python int types
    colors = np.round(colors).astype(int).tolist()  # Now a list of lists

    # Calculate percentage of each color
    total_pixels = len(labels)
    percentages = [(count / total_pixels) * 100 for count in counts.values()]

    # Get the most common colors along with their percentages
    top_colors = []
    for i in counts.keys():
        # Convert each color component to native Python int
        r, g, b = colors[i]
        top_colors.append(((int(r), int(g), int(b)), round(percentages[i], 2)))

    return top_colors


def reduce_image_resolution(image, scale_percent=100):
    if scale_percent == 100:
        return image
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']
        num_colors = request.form.get('num_colors', 10)
        scale_percent = request.form.get('scale', 100)

        # Validate and convert inputs
        try:
            num_colors = int(num_colors)
            if not (1 <= num_colors <= 20):
                num_colors = 10  # Default value
        except ValueError:
            num_colors = 10  # Default value

        try:
            scale_percent = int(scale_percent)
            if not (10 <= scale_percent <= 100):
                scale_percent = 100  # Default value
        except ValueError:
            scale_percent = 100  # Default value

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Read the image
            image = cv2.imread(filepath)

            # Reduce image resolution if needed
            reduced_image = reduce_image_resolution(image, scale_percent)
            cv2.imwrite(filepath, reduced_image)

            # Extract top colors
            top_colors = get_top_colors(filepath, num_colors)

            # Save the colors to session for later download
            # Convert tuples to lists for JSON serialization
            serializable_colors = [({'r': color[0], 'g': color[1], 'b': color[2]}, percentage) for color, percentage in
                                   top_colors]
            session['colors'] = serializable_colors

            return render_template('index.html', colors=top_colors, uploaded_image=filename, num_colors=num_colors)

    return render_template('index.html')


@app.route('/download_palette', methods=['GET'])
def download_palette():
    colors = session.get('colors', [])
    color_palette = [{'color': f'#{c["r"]:02x}{c["g"]:02x}{c["b"]:02x}', 'percentage': f'{p:.2f}%'}
                     for c, p in colors]
    return jsonify(color_palette)


if __name__ == '__main__':
    # Ensure the upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
