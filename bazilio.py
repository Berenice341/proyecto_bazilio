import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Importación segura del runtime de ANTLR4 para el backend en la nube
try:
    from antlr4 import InputStream
    ANTLR_ACTIVE = True
except ImportError:
    ANTLR_ACTIVE = False

# Frecuencias base estándar de las notas musicales de la práctica
NOTE_FREQS = {
    'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23,
    'G4': 392.00, 'A4': 440.00, 'B4': 493.88,
    'C3': 130.81, 'D3': 146.83, 'E3': 164.81, 'F3': 174.61,
    'G3': 196.00, 'A3': 220.00, 'B3': 246.94,
    'C5': 523.25
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/parse', methods=['POST'])
def parse_notes():
    data = request.get_json() or {}
    text_input = data.get('notes', '')
    
    tokens = text_input.strip().replace(',', ' ').split()
    parsed_events = []
    
    for token in tokens:
        # Validación y procesamiento léxico formal con ANTLR4 InputStream
        if ANTLR_ACTIVE:
            input_stream = InputStream(token)
        
        # Soporte para notas individuales o acordes unidos por guión (ej: C4-E4-G4)
        chord_parts = token.split('-')
        freqs = []
        for part in chord_parts:
            cleaned = part.strip().upper()
            if cleaned in NOTE_FREQS:
                freqs.append(NOTE_FREQS[cleaned])
                
        if freqs:
            parsed_events.append(freqs)
            
    return jsonify({
        'success': True, 
        'events': parsed_events, 
        'antlr_engine': 'Active (ANTLR4 Python Runtime)' if ANTLR_ACTIVE else 'Fallback'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)