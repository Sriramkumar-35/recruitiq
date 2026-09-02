from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel
import torch
from pyngrok import ngrok
import json
import os

app = Flask(__name__)

# ===== PATHS =====
LORA_PATH = r"C:\Users\23ad113\Clone\recruitiq\recruitiq-lora-v2"
BASE_MODEL = "unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit"

print("Step 1: Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(LORA_PATH)
print("Tokenizer loaded!")

print("Step 2: Loading base model with 4-bit quantization...")
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
)

model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True,
)
print("Base model loaded!")

print("Step 3: Loading LoRA adapter...")
model = PeftModel.from_pretrained(model, LORA_PATH)
model.eval()
print("LoRA adapter loaded!")
print("\n===== MODEL READY =====\n")

# ===== SCORING FUNCTION =====
def score_resume(resume_text, jd_text):
    prompt = "### Instruction:\n"
    prompt += "You are an expert recruiter. Score the resume against the job description on a scale of 0-100.\n\n"
    prompt += "JOB DESCRIPTION:\n" + jd_text[:1000] + "\n\n"
    prompt += "RESUME:\n" + resume_text[:1000] + "\n\n"
    prompt += "Respond with:\nScore: <number>\nReasoning: <explanation>\n\n### Response:"

    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=150,
            temperature=0.1,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
        )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    response_text = response.split("### Response:")[-1].strip()

    score = 0
    reasoning = ""
    key_matches = []
    key_gaps = []

    for line in response_text.split('\n'):
        if line.startswith('Score:'):
            try:
                score = int(''.join(filter(str.isdigit,
                    line.replace('Score:', '').strip()))[:3])
            except:
                score = 0
        if line.startswith('Reasoning:'):
            reasoning = line.replace('Reasoning:', '').strip()

    return {
        "score": max(0, min(100, score)),
        "reasoning": reasoning,
        "key_matches": key_matches,
        "key_gaps": key_gaps,
        "model_used": "fine-tuned-lora-v2"
    }

# ===== ROUTES =====
@app.route('/score_local', methods=['POST'])
def score_endpoint():
    try:
        data = request.json
        resume_text = data.get('resume', '')
        jd_text = data.get('jd', '')

        if not resume_text or not jd_text:
            return jsonify({'error': 'Missing resume or jd'})

        result = score_resume(resume_text, jd_text)
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'running',
        'model': 'recruitiq-lora-v2',
        'device': 'cuda' if torch.cuda.is_available() else 'cpu'
    })

@app.route('/test', methods=['GET'])
def test():
    test_resume = "Software Engineer with 3 years Python, Django, REST APIs, AWS, Docker."
    test_jd = "Looking for Python Developer with Django, REST APIs, AWS, Docker. 2+ years."
    result = score_resume(test_resume, test_jd)
    return jsonify(result)

# Add this route — gives a clear message at /
@app.route('/', methods=['GET'])
def root():
    return jsonify({
        'service': 'RecruitIQ Local Model Server',
        'model': 'recruitiq-lora-v2',
        'endpoints': {
            'POST /score_local': 'Score a resume against a JD',
            'GET /health': 'Health check',
            'GET /test': 'Test with sample data'
        }
    })

# Add this after_request handler — adds ngrok bypass header to all responses
@app.after_request
def add_headers(response):
    response.headers['ngrok-skip-browser-warning'] = 'true'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, ngrok-skip-browser-warning'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response

# ===== START SERVER =====
if __name__ == '__main__':
    print("Starting ngrok tunnel...")
    public_url = ngrok.connect(5001)
    print(f"\n{'='*55}")
    print(f"Fine-tuned model is publicly accessible!")
    print(f"Public URL: {public_url}")
    print(f"{'='*55}")
    print(f"Add this to your .env file:")
    print(f"LOCAL_MODEL_URL={public_url}")
    print(f"{'='*55}\n")
    print("Test your model at:")
    print(f"  {public_url}/health")
    print(f"  {public_url}/test")
    print(f"{'='*55}\n")

    app.run(port=5001, debug=False, use_reloader=False)


    