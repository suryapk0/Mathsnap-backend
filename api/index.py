from flask import Flask, request, jsonify
from flask_cors import CORS
from sympy import sympify, solve, integrate, diff, latex
import pytesseract
from PIL import Image
import io

app = Flask(__name__)
CORS(app)   # सब डोमेन से काम करेगा

@app.route('/api/solve', methods=['POST'])
def solve():
    text = request.form.get('text', '')
    file = request.files.get('image')

    if file:
        img = Image.open(io.BytesIO(file.read()))
        text = pytesseract.image_to_string(img, config='--psm 6') or "x+1"

    try:
        expr = sympify(text.replace('^', '**'))
        if 'int' in text.lower():
            ans = integrate(expr)
        elif 'diff' in text.lower():
            ans = diff(expr)
        else:
            ans = solve(expr)
        steps = [f"सवाल: {text}", f"उत्तर: {latex(ans)}"]
        return jsonify({"steps": steps, "answer": str(ans), "voice": "उत्तर है " + str(ans)})
    except:
        return jsonify({"steps": ["समझ नहीं आया"], "answer": "Error", "voice": "गलत सवाल"})

if __name__ == "__main__":
    app.run()
