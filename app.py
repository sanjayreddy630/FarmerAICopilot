import os
import sys

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

from llm.answer_engine import FarmerAICopilot

# Add project root to Python path
PROJECT_ROOT = os.path.dirname(
    os.path.abspath(__file__)
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ============================================================
# IMPORT IMAGE PREDICTOR
# ============================================================

try:

    from ml.predict import predict_image

    IMAGE_MODEL_AVAILABLE = True

    print("✅ Pest image model loaded")

except Exception as e:

    IMAGE_MODEL_AVAILABLE = False

    print(
        "⚠️ Pest image model unavailable:",
        e
    )


# ============================================================
# FLASK
# ============================================================

app = Flask(__name__)

CORS(app)


# ============================================================
# COPILOT
# ============================================================

copilot = FarmerAICopilot()


# ============================================================
# UPLOAD CONFIGURATION
# ============================================================

UPLOAD_FOLDER = os.path.join(
    PROJECT_ROOT,
    "uploads"
)

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


ALLOWED_EXTENSIONS = {

    "jpg",
    "jpeg",
    "png",

    "pdf",
    "txt",
    "csv",
    "xlsx",

}


IMAGE_EXTENSIONS = {

    "jpg",
    "jpeg",
    "png",

}


def allowed_file(
    filename
):

    return (

        "." in filename

        and

        filename.rsplit(
            ".",
            1
        )[1].lower()

        in ALLOWED_EXTENSIONS

    )


def allowed_image(
    filename
):

    return (

        "." in filename

        and

        filename.rsplit(
            ".",
            1
        )[1].lower()

        in IMAGE_EXTENSIONS

    )


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    return jsonify({

        "status":
            "online",

        "message":
            "Farmer AI Copilot API is running",

        "image_model":
            IMAGE_MODEL_AVAILABLE,

    })


# ============================================================
# ASK FARMER AI
# ============================================================

@app.route(
    "/api/ask",
    methods=["POST"]
)
def ask():

    try:

        data = request.get_json()

        if not data:

            return jsonify({

                "success":
                    False,

                "error":
                    "Invalid JSON request"

            }), 400


        question = (
            data.get(
                "question",
                ""
            )
            .strip()
        )


        language = data.get(
            "language",
            "English"
        )


        if not question:

            return jsonify({

                "success":
                    False,

                "error":
                    "Please provide a question"

            }), 400


        # Add language instruction
        if language != "English":

            question_for_ai = (
                f"Answer the following farming "
                f"question in {language}.\n\n"
                f"{question}"
            )

        else:

            question_for_ai = question


        result = copilot.ask(
            question_for_ai
        )


        return jsonify({

            "success":
                True,

            "question":
                question,

            "answer":
                result.get(
                    "answer",
                    ""
                ),

            "citations":
                result.get(
                    "citations",
                    []
                ),

        })


    except Exception as e:

        print(
            "ASK ERROR:",
            e
        )

        return jsonify({

            "success":
                False,

            "error":
                str(e)

        }), 500


# ============================================================
# GENERAL FILE UPLOAD
# ============================================================

@app.route(
    "/api/upload",
    methods=["POST"]
)
def upload_file():

    try:

        if "file" not in request.files:

            return jsonify({

                "success":
                    False,

                "error":
                    "No file provided"

            }), 400


        file = request.files["file"]


        if file.filename == "":

            return jsonify({

                "success":
                    False,

                "error":
                    "No file selected"

            }), 400


        if not allowed_file(
            file.filename
        ):

            return jsonify({

                "success":
                    False,

                "error":
                    (
                        "Unsupported file type. "
                        "Allowed: JPG, JPEG, PNG, "
                        "PDF, TXT, CSV, XLSX"
                    )

            }), 400


        filename = secure_filename(
            file.filename
        )


        filepath = os.path.join(
            UPLOAD_FOLDER,
            filename
        )


        file.save(
            filepath
        )


        print(
            f"📎 File uploaded: {filename}"
        )


        return jsonify({

            "success":
                True,

            "message":
                "File uploaded successfully",

            "filename":
                filename,

            "file_type":
                filename.rsplit(
                    ".",
                    1
                )[1].lower(),

            "path":
                filepath,

        })


    except Exception as e:

        print(
            "UPLOAD ERROR:",
            e
        )


        return jsonify({

            "success":
                False,

            "error":
                str(e)

        }), 500


# ============================================================
# IMAGE ANALYSIS
# ============================================================

@app.route(
    "/api/analyze-image",
    methods=["POST"]
)
def analyze_image():

    try:

        # ----------------------------------------------------
        # Check model
        # ----------------------------------------------------

        if not IMAGE_MODEL_AVAILABLE:

            return jsonify({

                "success":
                    False,

                "error":
                    (
                        "Pest image model is "
                        "not available."
                    )

            }), 503


        # ----------------------------------------------------
        # Check file
        # ----------------------------------------------------

        if "file" not in request.files:

            return jsonify({

                "success":
                    False,

                "error":
                    "No image provided"

            }), 400


        file = request.files["file"]


        if file.filename == "":

            return jsonify({

                "success":
                    False,

                "error":
                    "No image selected"

            }), 400


        # ----------------------------------------------------
        # Check image extension
        # ----------------------------------------------------

        if not allowed_image(
            file.filename
        ):

            return jsonify({

                "success":
                    False,

                "error":
                    (
                        "Please upload a JPG, "
                        "JPEG or PNG image."
                    )

            }), 400


        # ----------------------------------------------------
        # Save image
        # ----------------------------------------------------

        filename = secure_filename(
            file.filename
        )


        filepath = os.path.join(
            UPLOAD_FOLDER,
            filename
        )


        file.save(
            filepath
        )


        print()
        print(
            "📷 Image received:"
        )

        print(
            filepath
        )


        # ----------------------------------------------------
        # Predict
        # ----------------------------------------------------

        predictions = predict_image(
            filepath,
            top_k=3
        )


        # ----------------------------------------------------
        # Main prediction
        # ----------------------------------------------------

        if predictions:

            main_prediction = (
                predictions[0]
            )

        else:

            main_prediction = {

                "pest":
                    "Unknown",

                "confidence":
                    0,

            }


        # ----------------------------------------------------
        # Confidence interpretation
        # ----------------------------------------------------

        confidence = float(
            main_prediction.get(
                "confidence",
                0
            )
        )


        if confidence >= 70:

            confidence_level = (
                "High"
            )

        elif confidence >= 40:

            confidence_level = (
                "Medium"
            )

        else:

            confidence_level = (
                "Low"
            )


        # ----------------------------------------------------
        # Response
        # ----------------------------------------------------

        return jsonify({

            "success":
                True,

            "type":
                "pest_analysis",

            "image":
                filename,

            "prediction":
                main_prediction,

            "confidence_level":
                confidence_level,

            "top_predictions":
                predictions,

            "message":
                (
                    "This is an AI-assisted "
                    "image prediction. "
                    "For low-confidence results, "
                    "verify the pest with a "
                    "local agricultural expert."
                ),

        })


    except Exception as e:

        print()
        print(
            "❌ IMAGE ANALYSIS ERROR:"
        )

        print(
            str(e)
        )


        return jsonify({

            "success":
                False,

            "error":
                str(e)

        }), 500


# ============================================================
# SERVER
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 70)

    print(
        "🌾 FARMER AI COPILOT"
    )

    print("=" * 70)

    print(
        "Server:"
    )

    print(
        "http://127.0.0.1:5000"
    )

    print()

    print(
        "Text API:"
    )

    print(
        "POST /api/ask"
    )

    print()

    print(
        "File API:"
    )

    print(
        "POST /api/upload"
    )

    print()

    print(
        "Image AI:"
    )

    print(
        "POST /api/analyze-image"
    )

    print()

    print(
        "Pest model:"
    )

    print(
        "AVAILABLE"
        if IMAGE_MODEL_AVAILABLE
        else "NOT AVAILABLE"
    )

    print("=" * 70)


    app.run(

        host="127.0.0.1",

        port=5000,

        debug=False,

        use_reloader=False,

    )