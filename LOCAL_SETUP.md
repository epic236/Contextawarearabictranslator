# Context-Aware Arabic Translator - Local Setup Instructions

## Prerequisites

Before running this project locally, ensure you have the following installed:

- **Node.js** (version 18 or higher)
- **pnpm** package manager

To install pnpm if you don't have it:
```bash
npm install -g pnpm
```

## Installation Steps

### 1. Clone or Download the Project

Navigate to the project directory in your terminal:
```bash
cd path/to/context-aware-arabic-translator
```

### 2. Install Dependencies

Run the following command to install all required packages:
```bash
pnpm install
```

This will install all dependencies listed in `package.json`, including:
- React and React DOM
- React Router for navigation
- Tailwind CSS for styling
- Vite for development server

### 3. Start the Development Server

Run the development server:
```bash
pnpm run dev
```

The application will start and be available at:
```
http://localhost:5173
```

(The port number may vary if 5173 is already in use)

### 4. Access the Application

Open your web browser and navigate to the URL shown in your terminal (typically `http://localhost:5173`)

## Project Structure

```
src/
├── app/
│   ├── App.tsx              # Main application component with router
│   ├── routes.tsx           # Route configuration
│   └── components/
│       ├── TranslatorInput.tsx   # Input page component
│       └── TranslatorResult.tsx  # Results page component
├── styles/
│   ├── theme.css            # Theme and design tokens
│   └── fonts.css            # Font imports
└── imports/                 # Asset imports
```

## Backend Setup (Required)

### 1. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**Note**: First run will download the Helsinki-NLP translation model (~300MB). This is automatic but requires internet connection.

### 2. Prepare Training Data

Place these CSV files in the `backend/` directory:
- `dart_ready_train.csv`
- `dart_ready_test.csv`

Each CSV should have columns: `text` (Arabic text) and `dialect` (EGY, LEV, GLF, IRQ, or MGH)

### 3. Train the Dialect Detector

```bash
cd backend
python train_model.py
```

This creates:
- `vectorizer.pkl`
- `dialect_model.pkl`
- `confusion_matrix.png` (evaluation results)

### 4. Start the Backend

```bash
python api.py
```

The backend runs on `http://localhost:5000`

**Leave this terminal running.**

## Frontend Setup

### 1. Install Dependencies

In a **new terminal**:

```bash
pnpm install
```

This takes 1-3 minutes on first run.

### 2. Start the Frontend

```bash
pnpm run dev
```

The frontend runs on `http://localhost:5173`

## Using the Application

### Both Servers Must Be Running

**Terminal 1** - Backend:
```bash
cd backend
python api.py
```

**Terminal 2** - Frontend:
```bash
pnpm run dev
```

### Using the App

1. **Enter Text**: Paste or type Arabic text into the text area
2. **Translate**: Click the "Translate" button
3. **View Results**: See detailed translation results including:
   - Detected dialect with confidence scores
   - All dialect probabilities (visual bars)
   - Original Arabic text
   - Applied normalization rules
   - Normalized MSA text
   - English translation
   - Potential ambiguities
4. **Translate Another**: Click to return to input page

## Building for Production

To create a production build:
```bash
pnpm run build
```

The optimized files will be generated in the `dist/` directory.

To preview the production build locally:
```bash
pnpm run preview
```

## Notes

- **Dialect Detection**: Uses custom-trained TF-IDF + Logistic Regression model
- **Translation**: Uses Helsinki-NLP/opus-mt-ar-en pre-trained model
- **Normalization**: Converts dialectal Arabic to MSA before translation
- **Processing Time**: Typically 1-3 seconds per translation
- **First Run**: Translation model downloads automatically (~300MB)

## Troubleshooting

### Port Already in Use

**Frontend**: If port 5173 is in use, Vite auto-selects the next port. Check terminal output.

**Backend**: If port 5000 is in use, change it in `backend/api.py`:
```python
app.run(port=5001, debug=True)
```
Then update the frontend fetch URL in `src/app/components/TranslatorInput.tsx`.

### Backend Connection Error

If you see "Translation failed" alert:
1. Verify backend is running: `curl http://localhost:5000/health`
2. Check terminal for backend errors
3. Ensure models are loaded (check backend startup logs)

### Models Not Loading

If backend shows "Models not loaded":
1. Run `python train_model.py` in `backend/` directory
2. Verify `vectorizer.pkl` and `dialect_model.pkl` exist
3. Check training data CSV files are present

### Translation Model Download Fails

If Helsinki-NLP model doesn't download:
1. Check internet connection
2. Try: `pip install --upgrade transformers`
3. Manually download from: https://huggingface.co/Helsinki-NLP/opus-mt-ar-en

### Training Data Issues

If training fails:
1. Verify CSV files have columns: `text`, `dialect`
2. Check dialect labels are: EGY, LEV, GLF, IRQ, MGH
3. Ensure balanced dialect distribution

### Dependencies Not Installing
Make sure you're using pnpm instead of npm or yarn:
```bash
pnpm install
```

### Module Not Found Errors
Clear the node_modules and reinstall:
```bash
rm -rf node_modules
pnpm install
```

## Technology Stack

- **React** 18.3.1 - UI framework
- **React Router** 7.13.0 - Client-side routing
- **Tailwind CSS** 4.1.12 - Utility-first CSS framework
- **Vite** 6.3.5 - Build tool and dev server
- **TypeScript** - Type safety (via .tsx files)

## Support

For issues or questions about running this project locally, please refer to the official documentation:
- [Vite Documentation](https://vitejs.dev/)
- [React Router Documentation](https://reactrouter.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
