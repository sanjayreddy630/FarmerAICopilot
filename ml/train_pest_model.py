import json
import random
from pathlib import Path

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, random_split, WeightedRandomSampler
from torchvision import datasets, transforms, models


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_DIR = (
    PROJECT_ROOT
    / "data"
    / "agriculture_dataset"
    / "Agriculture Dataset for a RAG"
    / "dataset"
    / "dataset"
    / "Pest"
)

MODEL_DIR = PROJECT_ROOT / "ml" / "models"

MODEL_PATH = MODEL_DIR / "pest_model.pth"

CLASS_NAMES_PATH = MODEL_DIR / "pest_classes.json"

IMAGE_SIZE = 224

BATCH_SIZE = 8

EPOCHS = 1

VALIDATION_SPLIT = 0.20

LEARNING_RATE = 0.0001

SEED = 42

NUM_WORKERS = 0

# ============================================================
# SAFE TEST MODE
# ============================================================
# We are NOT training all 55K images yet.
# This makes a small test first.

TEST_MODE = True

TEST_LIMIT = 2000


# ============================================================
# RANDOM SEED
# ============================================================

random.seed(SEED)

torch.manual_seed(SEED)


# ============================================================
# DEVICE
# ============================================================

DEVICE = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)


# ============================================================
# TRANSFORMS
# ============================================================

train_transform = transforms.Compose([

    transforms.Resize(
        (IMAGE_SIZE, IMAGE_SIZE)
    ),

    transforms.RandomHorizontalFlip(
        p=0.5
    ),

    transforms.RandomRotation(
        10
    ),

    transforms.ColorJitter(
        brightness=0.2,
        contrast=0.2,
        saturation=0.2
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


validation_transform = transforms.Compose([

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
# LOAD DATASET
# ============================================================

def load_dataset():

    print()
    print("=" * 70)
    print("LOADING PEST DATASET")
    print("=" * 70)

    print(
        f"Dataset path:\n{DATASET_DIR}"
    )

    if not DATASET_DIR.exists():

        raise FileNotFoundError(
            f"\nDataset not found:\n{DATASET_DIR}"
        )

    dataset = datasets.ImageFolder(
        root=str(DATASET_DIR),
        transform=train_transform
    )

    print(
        f"Total images found: {len(dataset)}"
    )

    print(
        f"Total classes found: {len(dataset.classes)}"
    )

    return dataset


# ============================================================
# SAVE CLASS NAMES
# ============================================================

def save_class_names(
    class_names
):

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        CLASS_NAMES_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            class_names,
            file,
            indent=2,
            ensure_ascii=False
        )

    print(
        f"\nClass names saved:\n"
        f"{CLASS_NAMES_PATH}"
    )


# ============================================================
# CREATE SMALL TEST DATASET
# ============================================================

def create_test_dataset(
    dataset
):

    if not TEST_MODE:

        return dataset

    if len(dataset) <= TEST_LIMIT:

        return dataset

    print()
    print("=" * 70)
    print("⚠️ SAFE TEST MODE")
    print("=" * 70)

    print(
        f"Using only {TEST_LIMIT} images "
        f"out of {len(dataset)}"
    )

    generator = (
        torch.Generator()
        .manual_seed(SEED)
    )

    test_dataset, _ = random_split(

        dataset,

        [
            TEST_LIMIT,
            len(dataset) - TEST_LIMIT
        ],

        generator=generator

    )

    return test_dataset


# ============================================================
# TRAIN / VALIDATION SPLIT
# ============================================================

def split_dataset(
    dataset
):

    validation_size = int(
        len(dataset)
        * VALIDATION_SPLIT
    )

    train_size = (
        len(dataset)
        - validation_size
    )

    generator = (
        torch.Generator()
        .manual_seed(SEED)
    )

    train_dataset, validation_dataset = (
        random_split(
            dataset,
            [
                train_size,
                validation_size
            ],
            generator=generator
        )
    )

    return (
        train_dataset,
        validation_dataset
    )


# ============================================================
# MODEL
# ============================================================

def create_model(
    number_of_classes
):

    print()
    print("=" * 70)
    print("CREATING RESNET18 MODEL")
    print("=" * 70)

    print(
        f"Classes: {number_of_classes}"
    )

    print(
        f"Device: {DEVICE}"
    )

    weights = (
        models.ResNet18_Weights.DEFAULT
    )

    model = models.resnet18(
        weights=weights
    )

    # Freeze pretrained layers
    for parameter in model.parameters():

        parameter.requires_grad = False

    # Replace final classifier
    model.fc = nn.Linear(
        model.fc.in_features,
        number_of_classes
    )

    # Train classifier
    for parameter in model.fc.parameters():

        parameter.requires_grad = True

    model = model.to(
        DEVICE
    )

    return model


# ============================================================
# TRAIN
# ============================================================

def train_one_epoch(
    model,
    loader,
    criterion,
    optimizer
):

    model.train()

    total_loss = 0.0

    correct = 0

    total = 0

    for batch_number, (
        images,
        labels
    ) in enumerate(loader):

        images = images.to(
            DEVICE
        )

        labels = labels.to(
            DEVICE
        )

        optimizer.zero_grad()

        outputs = model(
            images
        )

        loss = criterion(
            outputs,
            labels
        )

        loss.backward()

        optimizer.step()

        total_loss += (
            loss.item()
            * images.size(0)
        )

        predictions = (
            outputs.argmax(
                dim=1
            )
        )

        correct += (
            predictions == labels
        ).sum().item()

        total += labels.size(0)

        if (
            batch_number + 1
        ) % 20 == 0:

            print(
                f"  Batch "
                f"{batch_number + 1}"
                f"/"
                f"{len(loader)}"
            )

    loss_value = (
        total_loss / total
        if total
        else 0
    )

    accuracy = (
        correct / total
        if total
        else 0
    )

    return (
        loss_value,
        accuracy
    )


# ============================================================
# VALIDATE
# ============================================================

def validate(
    model,
    loader,
    criterion
):

    model.eval()

    total_loss = 0.0

    correct = 0

    total = 0

    with torch.no_grad():

        for images, labels in loader:

            images = images.to(
                DEVICE
            )

            labels = labels.to(
                DEVICE
            )

            outputs = model(
                images
            )

            loss = criterion(
                outputs,
                labels
            )

            total_loss += (
                loss.item()
                * images.size(0)
            )

            predictions = (
                outputs.argmax(
                    dim=1
                )
            )

            correct += (
                predictions == labels
            ).sum().item()

            total += labels.size(0)

    loss_value = (
        total_loss / total
        if total
        else 0
    )

    accuracy = (
        correct / total
        if total
        else 0
    )

    return (
        loss_value,
        accuracy
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 70)
    print("🌾 FARMER AI PEST MODEL")
    print("=" * 70)

    print(
        f"Device: {DEVICE}"
    )

    print(
        f"CPU training: "
        f"{DEVICE.type == 'cpu'}"
    )

    # --------------------------------------------------------
    # Load complete dataset
    # --------------------------------------------------------

    full_dataset = load_dataset()

    original_class_names = (
        full_dataset.classes
    )

    save_class_names(
        original_class_names
    )

    # --------------------------------------------------------
    # Small test subset
    # --------------------------------------------------------

    dataset = create_test_dataset(
        full_dataset
    )

    print()
    print(
        f"Images used for this run: "
        f"{len(dataset)}"
    )

    # --------------------------------------------------------
    # Split
    # --------------------------------------------------------

    train_dataset, validation_dataset = (
        split_dataset(
            dataset
        )
    )

    print(
        f"Training images: "
        f"{len(train_dataset)}"
    )

    print(
        f"Validation images: "
        f"{len(validation_dataset)}"
    )

    # --------------------------------------------------------
    # Data loaders
    # --------------------------------------------------------

    train_loader = DataLoader(

        train_dataset,

        batch_size=BATCH_SIZE,

        shuffle=True,

        num_workers=NUM_WORKERS

    )

    validation_loader = DataLoader(

        validation_dataset,

        batch_size=BATCH_SIZE,

        shuffle=False,

        num_workers=NUM_WORKERS

    )

    # --------------------------------------------------------
    # Model
    # --------------------------------------------------------

    model = create_model(
        len(original_class_names)
    )

    # --------------------------------------------------------
    # Loss
    # --------------------------------------------------------

    criterion = nn.CrossEntropyLoss()

    # --------------------------------------------------------
    # Optimizer
    # --------------------------------------------------------

    optimizer = torch.optim.Adam(

        model.fc.parameters(),

        lr=LEARNING_RATE

    )

    # --------------------------------------------------------
    # Training
    # --------------------------------------------------------

    best_accuracy = 0.0

    for epoch in range(
        EPOCHS
    ):

        print()
        print("=" * 70)

        print(
            f"EPOCH "
            f"{epoch + 1}"
            f"/"
            f"{EPOCHS}"
        )

        print(
            "=" * 70
        )

        train_loss, train_accuracy = (
            train_one_epoch(
                model,
                train_loader,
                criterion,
                optimizer
            )
        )

        validation_loss, validation_accuracy = (
            validate(
                model,
                validation_loader,
                criterion
            )
        )

        print()
        print(
            f"Train loss: "
            f"{train_loss:.4f}"
        )

        print(
            f"Train accuracy: "
            f"{train_accuracy * 100:.2f}%"
        )

        print(
            f"Validation loss: "
            f"{validation_loss:.4f}"
        )

        print(
            f"Validation accuracy: "
            f"{validation_accuracy * 100:.2f}%"
        )

        # ----------------------------------------------------
        # Save best model
        # ----------------------------------------------------

        if (
            validation_accuracy
            > best_accuracy
        ):

            best_accuracy = (
                validation_accuracy
            )

            MODEL_DIR.mkdir(
                parents=True,
                exist_ok=True
            )

            torch.save(

                {
                    "model_state_dict":
                        model.state_dict(),

                    "class_names":
                        original_class_names,

                    "image_size":
                        IMAGE_SIZE,

                    "validation_accuracy":
                        validation_accuracy

                },

                MODEL_PATH

            )

            print()
            print(
                "✅ BEST MODEL SAVED"
            )

            print(
                f"Path:\n{MODEL_PATH}"
            )

    # --------------------------------------------------------
    # Complete
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("✅ TEST TRAINING COMPLETE")
    print("=" * 70)

    print(
        f"Best validation accuracy: "
        f"{best_accuracy * 100:.2f}%"
    )

    print()
    print(
        "Model:"
    )

    print(
        MODEL_PATH
    )

    print()
    print(
        "Classes:"
    )

    print(
        CLASS_NAMES_PATH
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()