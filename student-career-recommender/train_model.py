"""
Train the Machine Learning model for Career Path Recommendation.

This script:
1. Loads the CSV dataset
2. Preprocesses features (numeric + categorical)
3. Trains a RandomForestClassifier
4. Evaluates model performance
5. Saves the trained model and label encoder to disk
"""

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "dataset", "student_career_dataset.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "career_model.pkl")
ENCODER_PATH = os.path.join(MODEL_DIR, "label_encoder.pkl")


def load_dataset():
    """Load and return the student career dataset."""
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(
            f"Dataset not found at {DATASET_PATH}. "
            "Run generate_dataset.py first."
        )
    df = pd.read_csv(DATASET_PATH)
    print(f"Dataset loaded: {len(df)} rows, {len(df.columns)} columns")
    return df


def preprocess_data(df):
    """
    Preprocess the dataset for model training.

    - Encode categorical features using LabelEncoder
    - Separate features (X) and target (y)
    - Return X, y, and fitted encoders for categorical columns
    """
    df = df.copy()

    # Encode categorical columns
    categorical_encoders = {}
    categorical_cols = ["preferred_subject", "career_goal"]

    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        categorical_encoders[col] = le

    # Encode target variable
    target_encoder = LabelEncoder()
    df["recommended_path"] = target_encoder.fit_transform(df["recommended_path"])

    # Separate features and target
    feature_columns = [
        "math_score",
        "programming_score",
        "communication_score",
        "problem_solving_score",
        "web_interest",
        "mobile_interest",
        "ai_interest",
        "database_interest",
        "networking_interest",
        "cloud_interest",
        "design_interest",
        "preferred_subject",
        "career_goal",
    ]

    X = df[feature_columns].values
    y = df["recommended_path"].values

    return X, y, target_encoder, categorical_encoders


def train_model(X_train, y_train):
    """Train and return a RandomForestClassifier."""
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test, target_encoder):
    """Print model evaluation metrics."""
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nModel Accuracy: {accuracy * 100:.2f}%")
    print(f"\nClassification Report:")
    print(
        classification_report(
            y_test, y_pred, target_names=target_encoder.classes_
        )
    )
    return accuracy


def save_model(model, target_encoder):
    """Save the trained model and label encoder to disk."""
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(target_encoder, ENCODER_PATH)
    print(f"\nModel saved to: {MODEL_PATH}")
    print(f"Label encoder saved to: {ENCODER_PATH}")


def main():
    """Main training pipeline."""
    print("=" * 60)
    print("Student Career Path Recommendation - Model Training")
    print("=" * 60)

    # Step 1: Load dataset
    print("\n[1/5] Loading dataset...")
    df = load_dataset()

    # Step 2: Preprocess data
    print("\n[2/5] Preprocessing data...")
    X, y, target_encoder, categorical_encoders = preprocess_data(df)
    print(f"Features shape: {X.shape}")
    print(f"Target classes: {len(target_encoder.classes_)}")

    # Step 3: Split data
    print("\n[3/5] Splitting data (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")

    # Step 4: Train model
    print("\n[4/5] Training RandomForestClassifier...")
    model = train_model(X_train, y_train)

    # Step 5: Evaluate
    print("\n[5/5] Evaluating model...")
    accuracy = evaluate_model(model, X_test, y_test, target_encoder)

    # Save model
    save_model(model, target_encoder)

    print("\n" + "=" * 60)
    print("Training complete!")
    print(f"Final Accuracy: {accuracy * 100:.2f}%")
    print("=" * 60)


if __name__ == "__main__":
    main()
