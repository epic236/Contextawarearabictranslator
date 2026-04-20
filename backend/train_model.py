"""
Training script for the dialect detector
Run this BEFORE starting the API to generate vectorizer.pkl and dialect_model.pkl
"""

import pandas as pd
import numpy as np
import re
import pickle
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# --- 1. LOAD SPLIT DATASETS ---
# Replace paths with your actual local file locations
print("Loading datasets...")
train_df = pd.read_csv("dart_ready_train.csv")
test_df = pd.read_csv("dart_ready_test.csv")

target_col = 'dialect'
text_col = 'text'

print(f"Training samples: {len(train_df)}")
print(f"Test samples: {len(test_df)}")

# --- 2. ARABIC NORMALIZATION ---
def normalize_arabic(text):
    text = str(text)
    text = re.sub(r"[\u064B-\u0652]", "", text)
    text = re.sub(r"[أإآ]", "ا", text)
    text = re.sub(r"ى", "ي", text)
    text = re.sub(r"ة", "ه", text)
    text = re.sub(r"[^\u0621-\u064A\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# --- 3. PIPELINE ---
print("Normalizing text...")
train_df['text_clean'] = train_df[text_col].apply(normalize_arabic)
test_df['text_clean'] = test_df[text_col].apply(normalize_arabic)

X_train = train_df['text_clean']
y_train = train_df[target_col]
X_test = test_df['text_clean']
y_test = test_df[target_col]

# Vectorization (Fit ONLY on training data)
print("Vectorizing text...")
vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(3, 5), max_features=25000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Model training
print("Training model...")
model = LogisticRegression(max_iter=1000, class_weight='balanced')
model.fit(X_train_tfidf, y_train)

# --- 4. EVALUATION ---
print("\nEvaluating model...")
y_pred = model.predict(X_test_tfidf)
labels = sorted(y_test.unique())

print(f"\n{'='*60}")
print(f"Overall Test Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print(f"{'='*60}")
print("\nRegion-Level Report:")
print(classification_report(y_test, y_pred))

# Confusion Matrix
plt.figure(figsize=(10, 6))
cm = confusion_matrix(y_test, y_pred, labels=labels)
sns.heatmap(cm, annot=True, fmt='d', xticklabels=labels, yticklabels=labels, cmap='Purples')
plt.title('DART Dataset Region Confusion Matrix')
plt.ylabel('Actual Region')
plt.xlabel('Predicted Region')
plt.savefig('confusion_matrix.png')
print("\n✓ Confusion matrix saved as confusion_matrix.png")

# --- 5. SAVE MODELS ---
print("\nSaving models...")
with open('vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

with open('dialect_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✓ Models saved successfully!")
print("  - vectorizer.pkl")
print("  - dialect_model.pkl")
print("\nYou can now run the API with: python api.py")
