# Context-Aware Arabic Translator

A full-stack web application that detects Arabic dialects, normalizes them to Modern Standard Arabic (MSA), and translates to English with context-aware processing.

## Features

### Dialect Detection
- Classifies Arabic text into 5 regional dialects:
  - **Egyptian (EGY)** - مصري
  - **Levantine (LEV)** - شامي
  - **Gulf (GLF)** - خليجي
  - **Iraqi (IRQ)** - عراقي
  - **Maghrebi (MGH)** - مغربي
- Confidence scores for all dialects
- Trained on DART dataset

### Dialect-Aware Translation
- **Normalization Layer**: Converts dialectal words to MSA equivalents
- **Translation**: Uses Helsinki-NLP/opus-mt-ar-en model
- **Transparency**: Shows applied normalization rules
- **Ambiguity Detection**: Flags words with multiple meanings

### User Interface
- Clean, responsive design
- Visual confidence bars for all dialects
- Shows normalization process step-by-step
- Highlights ambiguous words

## Quick Start

### Prerequisites

- **Python** 3.8+
- **Node.js** 18+ and **pnpm**
- **Training data**: `dart_ready_train.csv` and `dart_ready_test.csv`

### Backend Setup

1. **Install Python dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

2. **Place training data:**
Put your CSV files in the `backend/` directory:
- `dart_ready_train.csv`
- `dart_ready_test.csv`

3. **Train the dialect detector:**
```bash
python train_model.py
```

4. **Start the backend:**
```bash
python api.py
```

Backend runs on `http://localhost:5000`

### Frontend Setup

1. **Install dependencies:**
```bash
pnpm install
```

2. **Start the dev server:**
```bash
pnpm run dev
```

Frontend runs on `http://localhost:5173`

## Usage

1. Open `http://localhost:5173` in your browser
2. Enter Arabic text (any dialect)
3. Click "Translate"
4. View results:
   - Detected dialect with confidence
   - All dialect probabilities
   - Original text
   - Normalization rules applied
   - Normalized MSA text
   - English translation
   - Ambiguity warnings (if any)

## Example

**Input (Egyptian):**
```
حد يقدر يقول غير كدة
```

**Output:**
- **Dialect**: Egyptian (89% confidence)
- **Normalized**: حد يقدر يقول غير كده
- **Rules Applied**: كدة → كده
- **Translation**: Can anyone say otherwise?

## Technology Stack

### Frontend
- React 18.3.1 + TypeScript
- React Router 7.13.0
- Tailwind CSS 4.1.12
- Vite 6.3.5

### Backend
- Python 3.8+
- Flask 3.0.0 (API server)
- scikit-learn 1.5.0 (dialect detection)
- transformers 4.36.0 (translation)
- PyTorch 2.1.0 (model inference)

### Models
- **Dialect Detector**: TF-IDF + Logistic Regression (custom-trained)
- **Translator**: Helsinki-NLP/opus-mt-ar-en (pre-trained)

## Project Structure

```
.
├── src/                        # Frontend code
│   ├── app/
│   │   ├── App.tsx            # Main app
│   │   ├── routes.tsx         # Routing
│   │   └── components/
│   │       ├── TranslatorInput.tsx
│   │       └── TranslatorResult.tsx
│   └── styles/
│
├── backend/                    # Backend code
│   ├── api.py                 # Flask API
│   ├── dialect_detector.py    # Dialect classification
│   ├── translator.py          # Translation logic
│   ├── train_model.py         # Training script
│   ├── requirements.txt       # Python deps
│   └── README.md              # Backend docs
│
├── package.json               # Frontend deps
└── README.md                  # This file
```

## Training Data Format

Your CSV files should have these columns:

| text | dialect |
|------|---------|
| مش عارف | EGY |
| بدي أروح | LEV |
| أبي ماي | GLF |

## How It Works

1. **Input**: User enters Arabic text
2. **Detection**: TF-IDF vectorizer + Logistic Regression classifies dialect
3. **Normalization**: Dialect-specific rules convert to MSA
4. **Translation**: MarianMT model translates MSA to English
5. **Explanation**: Shows normalization rules and ambiguities

## Performance

- **Dialect Detection**: ~85-90% accuracy on DART test set
- **Translation Speed**: 1-3 seconds per request
- **Model Size**: 
  - Dialect detector: ~5-10 MB
  - Translation model: ~300 MB (auto-downloaded)

## Known Limitations

- Normalization rules are basic (can be expanded)
- Translation quality depends on MSA normalization accuracy
- Mixed-dialect text uses majority dialect
- Code-switching (Arabic-English mix) not fully supported

## Troubleshooting

See [backend/README.md](backend/README.md) for detailed troubleshooting.

**Common Issues:**

- **"Models not loaded"**: Run `python train_model.py` first
- **Translation fails**: Check internet connection (first run downloads model)
- **Low accuracy**: Verify training data format and balance
- **CORS errors**: Ensure backend is running on port 5000

## Future Enhancements

- [ ] Expand normalization dictionaries
- [ ] Add user feedback for improving rules
- [ ] Support code-switching detection
- [ ] Add more translation targets (French, Spanish, etc.)
- [ ] Fine-tune translation model on dialectal data
- [ ] API rate limiting and caching

## Credits

- **DART Dataset**: For dialect-labeled training data
- **Helsinki-NLP**: For opus-mt-ar-en translation model
- Built for CS 329 coursework

## License

[Add your license here]
