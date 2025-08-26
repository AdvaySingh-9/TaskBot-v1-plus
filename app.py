import google.generativeai as generativeai
from flask import Flask, request, jsonify, render_template, send_file
from google.genai import types
from PIL import Image
from io import BytesIO
from google import genai


#Connect to index.html
app = Flask(__name__)


@app.route("/write", methods=["GET", "POST"])
def write():
    if request.method == "GET":
        return render_template("write.html")

    if request.method == "POST":
        # Getting data from form
        question = request.form.get("question", "").strip()
        types = request.form.get("type", "").strip()
        word_limit = request.form.get("word_limit", "").strip()

        print(f"\nRAW FORM DATA -> question: '{question}', type: '{types}', word_limit: '{word_limit}'\n-------------------------------\n")

        if not question:
            return jsonify({"error": "Please provide a question."}), 400

        if word_limit:
            try:
                word_limit = float(word_limit)
            except ValueError:
                return jsonify({"error": "Word limit must be a number."}), 400
        else:
            word_limit = None

        generativeai.configure(api_key="API_KEY")

        try:
            model = generativeai.GenerativeModel("gemini-2.0-flash")
            prompt = (
                f"You are TaskBot AI created by Advay Singh and powered by Gemini AI. "
                f"Write a {types if types else 'paragraph'} on the topic '{question}'"
            )
            if word_limit:
                prompt += f" nearly about {word_limit} words."

            response = model.generate_content(prompt)
            print(f"ANSWER BY TASKBOT AI: \n {response.text}")
            return jsonify({"answer": response.text})
                
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({"error": "An error occurred while processing your request."}), 500

@app.route("/summarize", methods=["GET", "POST"])
def summarize():
    if request.method == "GET":
        return render_template("summarize.html")
    if request.method == "POST":
        question = request.form.get("question", "").strip()
    types = request.form.get("type")
    minimum_lines_points = request.form.get("num_of_lines_points")
    if not question:
        return jsonify({"error": "Please provide a question."}), 400

    generativeai.configure(api_key="API_KEY")

    try:

        model = generativeai.GenerativeModel('gemini-2.0-flash')
        prompt = (
            f"You are TaskBot AI created by Advay Singh and powered by Gemini AI. "
            f"Write a {types if types else 'paragraph'} on the topic '{question}'")
        if minimum_lines_points:
            prompt += f" nearly about {minimum_lines_points} {types}."
        response = model.generate_content(prompt)
        answer = response.text

        print(f"Raw Text: \n{question};  Type: {types}; Minimum {types}: {minimum_lines_points}\n------------------------- \n {answer} \n -------------------------")

        return jsonify({"answer": answer})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred while processing your request."}), 500
    

@app.route("/think", methods=["GET", "POST"])
def think():
    if request.method == "GET":
        return render_template("think.html")
    if request.method == "POST":

        question = request.form.get("question", "").strip()
        if not question:
            return jsonify({"error": "Please provide a question."}), 400

        generativeai.configure(api_key="API_KEY")

        try:
            model = generativeai.GenerativeModel('gemini-2.0-flash-thinking-exp-01-21')
            response = model.generate_content(f"You are TaskBot AI created by Advay Singh and powered by Gemini AI. Remember that and don't say     anything (not even ok) about that just answer me this question- {question}.")
            answer = response.text


            print(f"Question: {question}\n------------------------- \n {answer} \n -------------------------\n")

            return jsonify({"answer": answer})
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({"error": "An error occurred while processing your request."}), 500


@app.route("/translate", methods=["GET", "POST"])
def translate():
    if request.method == "GET":
        return render_template("translate.html")
    if request.method == "POST":
        question = request.form.get("question", "").strip()
        translate_from = request.form.get("translate_from", "").strip()
        translate_to = request.form.get("translate_to", "").strip()
        if not question:
            return jsonify({"error": "Please provide a question."}), 400

        generativeai.configure(api_key="API_KEY")

        try:

            model = generativeai.GenerativeModel('gemini-2.0-flash')
            response = model.generate_content(f"You are TaskBot AI created by Advay Singh and powered by Gemini AI remember this and don't say  anything about this unitll asked (not even ok). Just translate {question} from {translate_from} to {translate_to} and nothing else.  ")
            answer = response.text

            print(f"Translate: {question} from {translate_from} to {translate_to}\n------------------------- \n {answer} \n--------------------------")

            return jsonify({"answer": answer})
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({"error": "An error occurred while processing your request."}), 500

@app.route("/imagine", methods=["GET", "POST"])
def imagine():
    if request.method == "GET":
        return render_template("imagine.html")
    if request.method == "POST":
        contents = request.form.get("contents", "").strip()
    if not contents:
        return jsonify({"error": "Please provide a prompt."}), 400
    
    client = genai.Client(api_key="API_KEY")

    response = client.models.generate_content(
        model="gemini-2.0-flash-preview-image-generation",
        contents=contents,
        config=types.GenerateContentConfig(
          response_modalities=['TEXT', 'IMAGE']
        )
    )
    print(f"\nPROMPT: {contents}\n")
    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            image = Image.open(BytesIO(part.inline_data.data))
            img_io = BytesIO()
            image.save(img_io, format="PNG")
            img_io.seek(0)
            return send_file(img_io, mimetype="image/png")

    return jsonify({"error": "No image returned by model"}), 500


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    #getting the question from the form55
    question = request.form.get("question", "").strip()
    if not question:
        return jsonify({"error": "Please provide a question."}), 400

    generativeai.configure(api_key="API_KEY")

    try:
        # use Google's Gemini-2.0-Flash nodle for generating content
        model = generativeai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(f"You are TaskBot AI created by Advay Singh and powered by Gemini AI. Remember that and don't say anything (not even ok) about that just answer me this question- {question}.")
        answer = response.text

        # Log the question and answer for debugging
        print(f"Question: {question}\n------------------------- \n {answer} \n -------------------------")
        # Return the answer as JSON
        return jsonify({"answer": answer})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred while processing your request."}), 500

if __name__ == '__main__':

        app.run(host="0.0.0.0", port=7860)
        