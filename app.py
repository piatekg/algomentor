from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import openai
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/problems')
def problems():
    return render_template('problems.html')

@app.route('/get_ai_help', methods=['POST'])
def get_ai_help():
    user_input = request.json.get('problem_description', '')

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a programming tutor helping students debug and improve their own code. Do not solve the problem for them. Instead, identify any mistakes, ask guiding questions, and suggest what they should look into or try next. Your goal is to teach, not to give the final answer."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=500
        )
        ai_response = response.choices[0].message.content.strip()
        return jsonify({'response': ai_response})

    except openai.OpenAIError as e:
        return jsonify({'ai_response': f"Error from OpenAI API: {str(e)}"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)