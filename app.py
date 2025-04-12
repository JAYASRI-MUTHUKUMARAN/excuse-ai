from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)


HUGGINGFACE_API_KEY = "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"
HUGGINGFACE_MODEL_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/generate', methods=['POST'])
def generate():
    category = request.form['category']
    reason = request.form['reason']
    
    prompt = f"Write a formal excuse letter for missing {category} because {reason}."

    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
    }

    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 150}
    }

    response = requests.post(HUGGINGFACE_MODEL_URL, headers=headers, json=payload)
    
    try:
        result = response.json()
        if isinstance(result, list) and 'generated_text' in result[0]:
            return jsonify({'excuse': result[0]['generated_text']})
        elif isinstance(result, dict) and 'generated_text' in result:
            return jsonify({'excuse': result['generated_text']})
        elif 'error' in result:
            return jsonify({'excuse': f"API Error: {result['error']}"}), 500
        else:
            return jsonify({'excuse': "Sorry, the model did not return a valid response."}), 500
    except Exception as e:
        return jsonify({'excuse': f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
