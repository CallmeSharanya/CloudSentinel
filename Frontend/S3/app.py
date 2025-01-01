import boto3
from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from HE_and_Stego.main_ops import *
from werkzeug.datastructures import FileStorage
from PIL import Image
import io

ALLOWED_EXTENSIONS = {'xlsx'}

def allowed_file(filename): # Check if the file has an allowed extension
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

db = SQLAlchemy()  # Initialize the SQLAlchemy object

class File(db.Model): # Database model to store file metadata
    id = db.Column(db.Integer, primary_key=True)
    original_filename = db.Column(db.String(100))
    filename = db.Column(db.String(100))
    bucket = db.Column(db.String(100))
    region = db.Column(db.String(100))

def create_file_storage_obj(encoded_img_paths):
    file_objs = []
    for encoded_img in encoded_img_paths:
        image = Image.open(encoded_img)
        # Step 2: Save the image to an in-memory file
        memory_file = io.BytesIO()
        image.save(memory_file, format="PNG")  # Save image in PNG format
        memory_file.seek(0)  # Reset the file pointer to the beginning

        # Step 3: Wrap the in-memory file in a FileStorage object
        file_objs.append(
            FileStorage(
                stream=memory_file,
                filename=encoded_img.split("\\")[-1],  # Name of the image file
                content_type="image/png"  # MIME type
            )
        )

    return file_objs

def create_app(): # Factory function to create and configure the Flask app
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["S3_BUCKET"] = "flask-onion"  # Replace with your actual bucket name
    app.config["S3_REGION"] = "ap-southeast-2"  # Replace with your AWS S3 region

    db.init_app(app)

    @app.route("/", methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            # Check if a file is part of the request
            if "file-to-save" not in request.files:
                return "No file part in the request!"

            uploaded_file = request.files["file-to-save"]
            if uploaded_file.filename == "":
                return "No file selected!"
            if not allowed_file(uploaded_file.filename):
                return "File type not allowed!"
            
            images_directory = r"C:\RVCE\College_SEM3\SEM 3 EL\Trials\flask-s3-file-upload\images"
            encoded_imgs_directory = r"C:\RVCE\College_SEM3\SEM 3 EL\Trials\flask-s3-file-upload\encoded_imgs"
            public_key, private_key = generate_keys_to_json()
            
            encoded_img_paths = encrypt_HE_and_stego(public_key, uploaded_file, images_directory, encoded_imgs_directory)
            print(encoded_img_paths)
            file_objs = create_file_storage_obj(encoded_img_paths)



            try:
                # Upload the file to S3
                s3 = boto3.resource("s3")
                bucket_name = app.config["S3_BUCKET"]
                region = app.config["S3_REGION"]
                for file in file_objs:
                    s3.Bucket(bucket_name).upload_fileobj(file.stream, file.filename)

                # Save file metadata to the database
                new_file = File(
                    original_filename=uploaded_file.filename,
                    filename=uploaded_file.filename,
                    bucket=bucket_name,
                    region=region
                )
                db.session.add(new_file)
                db.session.commit()

            except Exception as e:
                return f"Failed to upload file: {str(e)}"

            return redirect(url_for("index"))

        # Fetch all files from the database to display on the webpage
        files = File.query.all()
        return render_template("index.html", files=files)

    return app