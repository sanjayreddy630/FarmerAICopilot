import json
from pathlib import Path

import torch
import torch.nn as nn
from PIL import Image
from torchvision import models, transforms


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    PROJECT_ROOT
    / "ml"
    / "models"
    / "pest_model.pth"
)

CLASS_NAMES_PATH = (
    PROJECT_ROOT
    / "ml"
    / "models"
    / "pest_classes.json"
)


# ============================================================
# CONFIGURATION
# ============================================================

IMAGE_SIZE = 224

TOP_K = 3

DEVICE = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)


# ============================================================
# IMAGE TRANSFORMATION
# ============================================================

image_transform = transforms.Compose([

    transforms.Resize(
        (IMAGE_SIZE, IMAGE_SIZE)
    ),

    transforms.ToTensor(),

    transforms.Normalize(
        mean=[
            0.485,
            0.456,
            0.406
        ],
        std=[
            0.229,
            0.224,
            0.225
        ]
    )

])


# ============================================================
# LOAD CLASS NAMES
# ============================================================

def load_class_names():

    if not CLASS_NAMES_PATH.exists():

        raise FileNotFoundError(
            f"Class names file not found:\n"
            f"{CLASS_NAMES_PATH}"
        )

    with open(
        CLASS_NAMES_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ============================================================
# LOAD MODEL
# ============================================================

def load_model():

    if not MODEL_PATH.exists():

        raise FileNotFoundError(
            f"Model file not found:\n"
            f"{MODEL_PATH}"
        )

    class_names = load_class_names()

    # Create ResNet18
    model = models.resnet18(
        weights=None
    )

    # Replace final layer with our 132 classes
    model.fc = nn.Linear(
        model.fc.in_features,
        len(class_names)
    )

    # Load trained weights
    checkpoint = torch.load(
        MODEL_PATH,
        map_location=DEVICE
    )

    # Our training script saved a dictionary
    if isinstance(
        checkpoint,
        dict
    ) and "model_state_dict" in checkpoint:

        model.load_state_dict(
            checkpoint[
                "model_state_dict"
            ]
        )

    else:

        model.load_state_dict(
            checkpoint
        )

    model = model.to(
        DEVICE
    )

    model.eval()

    return model, class_names


# ============================================================
# PREDICT IMAGE
# ============================================================

def predict_image(
    image_path,
    top_k=TOP_K
):

    image_path = Path(
        image_path
    )

    if not image_path.exists():

        raise FileNotFoundError(
            f"Image not found:\n"
            f"{image_path}"
        )

    # Load model
    model, class_names = (
        load_model()
    )

    # Open image
    image = Image.open(
        image_path
    ).convert("RGB")

    # Transform
    image_tensor = (
        image_transform(image)
        .unsqueeze(0)
        .to(DEVICE)
    )

    # Prediction
    with torch.no_grad():

        outputs = model(
            image_tensor
        )

        probabilities = torch.softmax(
            outputs,
            dim=1
        )

        values, indices = torch.topk(
            probabilities,
            min(
                top_k,
                len(class_names)
            ),
            dim=1
        )

    results = []

    for probability, index in zip(
        values[0],
        indices[0]
    ):

        class_index = (
            index.item()
        )

        confidence = (
            probability.item()
            * 100
        )

        results.append({

            "pest": class_names[
                class_index
            ],

            "confidence": round(
                confidence,
                2
            ),

        })

    return results


# ============================================================
# SIMPLE TERMINAL TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 70)
    print("🌾 FARMER AI PEST IMAGE PREDICTOR")
    print("=" * 70)

    print(
        f"Device: {DEVICE}"
    )

    print(
        f"Model: {MODEL_PATH}"
    )

    print()


    image_input = input(
        "Enter image path: "
    ).strip().strip('"')


    if not image_input:

        print(
            "❌ No image path provided."
        )

        raise SystemExit(1)


    try:

        predictions = predict_image(
            image_input
        )


        print()
        print("=" * 70)
        print("TOP 3 PREDICTIONS")
        print("=" * 70)


        for number, prediction in enumerate(
            predictions,
            start=1
        ):

            print(
                f"{number}. "
                f"{prediction['pest']} "
                f"— "
                f"{prediction['confidence']}%"
            )


        print()
        print(
            "✅ Prediction complete."
        )


    except Exception as error:

        print()
        print(
            "❌ Prediction failed:"
        )

        print(
            error
        )