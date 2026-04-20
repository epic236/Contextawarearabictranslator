from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback

# Import our custom modules
from dialect_detector import load_models, detect_dialect, get_dialect_confidence
from translator import (
    load_translation_model,
    normalize_dialect,
    translate_ar_to_en,
    get_ambiguity_notes
)

app = Flask(__name__)
CORS(app)  # Allow frontend to call this API

# Load models on startup
print("\n" + "="*60)
print("Initializing Arabic Dialect-Aware Translator")
print("="*60)

models_loaded = False
translation_loaded = False

print("\n[1/2] Loading dialect detection models...")
models_loaded = load_models()

print("\n[2/2] Loading translation model...")
translation_loaded = load_translation_model()

if models_loaded and translation_loaded:
    print("\n" + "="*60)
    print("✓ All models loaded successfully - API ready!")
    print("="*60 + "\n")
else:
    print("\n" + "="*60)
    print("⚠ WARNING: Some models failed to load")
    print("="*60 + "\n")

# Dialect name mapping
DIALECT_NAMES = {
    'EGY': 'Egyptian',
    'LEV': 'Levantine',
    'GLF': 'Gulf',
    'IRQ': 'Iraqi',
    'MGH': 'Maghrebi'
}

@app.route('/translate', methods=['POST'])
def dialect_aware_translate():
    """
    Main translation endpoint
    Performs: dialect detection → normalization → translation → explanations
    """
    if not models_loaded or not translation_loaded:
        return jsonify({
            'error': 'Models not loaded. Please train dialect detector and ensure translation model is available.'
        }), 500

    data = request.json
    text = data.get('text', '').strip()

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    try:
        # Step 1: Detect dialect with confidence scores
        dialect_info = get_dialect_confidence(text)
        dialect = dialect_info['dialect']

        # Step 2: Normalize dialect to MSA
        normalized_text, applied_rules = normalize_dialect(text, dialect)

        # Step 3: Translate to English
        translation = translate_ar_to_en(normalized_text)

        # Step 4: Get ambiguity notes
        ambiguity_notes = get_ambiguity_notes(text)

        # Build response
        return jsonify({
            'input_text': text,
            'detected_dialect': DIALECT_NAMES.get(dialect, dialect),
            'dialect_code': dialect,
            'confidence': dialect_info['confidence'],
            'all_probabilities': {
                DIALECT_NAMES.get(d, d): prob
                for d, prob in dialect_info['all_probabilities'].items()
            },
            'normalized_text': normalized_text,
            'applied_normalization_rules': applied_rules,
            'translation': translation,
            'ambiguities': ambiguity_notes
        })

    except Exception as e:
        print(f"Translation error: {e}")
        traceback.print_exc()
        return jsonify({'error': f'Translation failed: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Check if API and models are ready"""
    return jsonify({
        'status': 'ok' if (models_loaded and translation_loaded) else 'degraded',
        'dialect_detector_loaded': models_loaded,
        'translation_model_loaded': translation_loaded
    })

@app.route('/test', methods=['POST'])
def test_translation():
    """Test endpoint with example"""
    example_text = "حد يقدر يقول غير كدة"

    try:
        dialect_info = get_dialect_confidence(example_text)
        dialect = dialect_info['dialect']
        normalized_text, applied_rules = normalize_dialect(example_text, dialect)
        translation = translate_ar_to_en(normalized_text)

        return jsonify({
            'test_text': example_text,
            'dialect': DIALECT_NAMES.get(dialect, dialect),
            'normalized': normalized_text,
            'translation': translation,
            'rules_applied': applied_rules
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Context-Aware Arabic Translator API")
    print("="*60)
    print("Running on: http://localhost:5000")
    print("\nEndpoints:")
    print("  POST /translate  - Translate Arabic text with dialect detection")
    print("  GET  /health     - Health check")
    print("  POST /test       - Test with example")
    print("\nRequired files:")
    print("  ✓ vectorizer.pkl (dialect detector)")
    print("  ✓ dialect_model.pkl (dialect detector)")
    print("  ✓ Helsinki-NLP/opus-mt-ar-en (auto-downloaded)")
    print("="*60 + "\n")

    app.run(port=5000, debug=True)
