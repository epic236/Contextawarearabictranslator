# Complete Setup Guide - Context-Aware Arabic Translator

Follow these steps to get the full application running.

## Prerequisites

Install these first:
- **Python 3.8+** (with pip)
- **Node.js 18+** and **pnpm**

## Step-by-Step Setup

### Part 1: Backend Setup

#### 1. Navigate to backend directory
```bash
cd backend
```

#### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

**Expected time**: 2-5 minutes

**What happens**: 
- Installs Flask, scikit-learn, transformers, PyTorch
- First run downloads Helsinki-NLP model (~300MB)

#### 3. Add your training data

Place these CSV files in the `backend/` directory:
- `dart_ready_train.csv`
- `dart_ready_test.csv`

**CSV Format Required**:
```csv
text,dialect
"مش عارف",EGY
"بدي أروح",LEV
"أبي ماي",GLF
```

Columns:
- `text` = Arabic text
- `dialect` = One of: EGY, LEV, GLF, IRQ, MGH

#### 4. Train the dialect detector
```bash
python train_model.py
```

**Expected time**: 2-5 minutes

**What happens**:
- Normalizes Arabic text
- Trains TF-IDF vectorizer
- Trains Logistic Regression classifier
- Evaluates on test set
- Creates:
  - `vectorizer.pkl`
  - `dialect_model.pkl`
  - `confusion_matrix.png`

**Expected output**:
```
Loading datasets...
Training samples: 20000
Test samples: 5000
Normalizing text...
Vectorizing text...
Training model...
Evaluating model...

Overall Test Accuracy: 0.8742

✓ Models saved successfully!
```

#### 5. Start the backend server
```bash
python api.py
```

**Keep this terminal open and running.**

You should see:
```
✓ Models loaded successfully
✓ Translation model loaded successfully on cpu
Running on: http://localhost:5000
```

Test it works:
```bash
curl http://localhost:5000/health
```

Expected response:
```json
{
  "status": "ok",
  "dialect_detector_loaded": true,
  "translation_model_loaded": true
}
```

---

### Part 2: Frontend Setup

#### 1. Open a NEW terminal

Don't close the backend terminal.

#### 2. Navigate to project root
```bash
cd /path/to/your/project
```

#### 3. Install frontend dependencies
```bash
pnpm install
```

**Expected time**: 1-3 minutes

#### 4. Start the frontend dev server
```bash
pnpm run dev
```

**Keep this terminal open too.**

You should see:
```
VITE v6.3.5  ready in 500 ms
➜  Local:   http://localhost:5173/
```

#### 5. Open in browser

Navigate to: **http://localhost:5173**

---

## Verification Checklist

✅ **Backend running**: Terminal 1 shows "Running on: http://localhost:5000"  
✅ **Frontend running**: Terminal 2 shows "Local: http://localhost:5173/"  
✅ **Browser open**: Shows "Context-Aware Arabic Translator" page  
✅ **Files exist**: `backend/vectorizer.pkl` and `backend/dialect_model.pkl`  

## Test the Application

### Test 1: Egyptian Dialect
```
Input: مش عارف أعمل إيه
```

Expected results:
- Dialect: Egyptian
- Confidence: High (>80%)
- Translation: English text
- Shows normalization rules

### Test 2: Levantine Dialect
```
Input: بدي أروح على البيت
```

Expected results:
- Dialect: Levantine
- Shows normalization: بدي → أريد

### Test 3: Gulf Dialect
```
Input: أبي ماي بارد
```

Expected results:
- Dialect: Gulf
- Shows normalization: أبي → أريد

## Common Issues and Fixes

### Issue: "Models not loaded"

**Solution**:
```bash
cd backend
python train_model.py
ls *.pkl  # Should show vectorizer.pkl and dialect_model.pkl
```

### Issue: "Translation failed"

**Check**:
1. Backend is running: `curl http://localhost:5000/health`
2. Check backend terminal for errors
3. Restart backend: Ctrl+C, then `python api.py`

### Issue: "Port 5000 already in use"

**Solution**:
```bash
# Find what's using port 5000
lsof -i :5000  # Mac/Linux
netstat -ano | findstr :5000  # Windows

# Kill it or change port in api.py:
app.run(port=5001, debug=True)
# Then update frontend: src/app/components/TranslatorInput.tsx
# Change: http://localhost:5000 → http://localhost:5001
```

### Issue: "pnpm not found"

**Solution**:
```bash
npm install -g pnpm
```

### Issue: Translation model download fails

**Solution**:
```bash
# Check internet connection, then:
pip install --upgrade transformers
# Or manually download from:
# https://huggingface.co/Helsinki-NLP/opus-mt-ar-en
```

## File Structure After Setup

```
your-project/
├── backend/
│   ├── api.py
│   ├── dialect_detector.py
│   ├── translator.py
│   ├── train_model.py
│   ├── requirements.txt
│   ├── dart_ready_train.csv          ← You provide
│   ├── dart_ready_test.csv           ← You provide
│   ├── vectorizer.pkl                ← Generated
│   ├── dialect_model.pkl             ← Generated
│   └── confusion_matrix.png          ← Generated
├── src/
│   └── app/
│       ├── App.tsx
│       └── components/
│           ├── TranslatorInput.tsx
│           └── TranslatorResult.tsx
├── package.json
└── README.md
```

## Running After Initial Setup

Once everything is set up, you only need:

**Terminal 1**:
```bash
cd backend
python api.py
```

**Terminal 2**:
```bash
pnpm run dev
```

**Browser**:
```
http://localhost:5173
```

## Stopping the Application

1. **Frontend**: Press `Ctrl+C` in Terminal 2
2. **Backend**: Press `Ctrl+C` in Terminal 1

## Need Help?

- Backend issues: See `backend/README.md`
- Frontend issues: See `LOCAL_SETUP.md`
- Full documentation: See `README.md`
