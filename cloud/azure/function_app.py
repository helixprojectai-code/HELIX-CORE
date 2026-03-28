import azure.functions as func
import json
import math
import os

app = func.FunctionApp()

LAMBDA_M = math.log(10)
RENORM_ALPHA = 1.0 / (2 * math.pi)

SYSTEM_PROMPT = """You are the FZS-MK Memory Kernel — a Functorial Zeno Sheaf with Memory Kernel.

You will receive a list of token entries, each with pre-computed prime-harmonic weights.
For each token, apply semantic memory modulation and return a bias value in [-1.0, 1.0].

Ontology (ADR-SHF-001):
- monster_group_memory_kernel: stabilization via Monster group actions
- semantic_inertia: mass-like field property at each prime coordinate
- sheaf_morphism: structure-preserving transformation between sheaf objects

For each token entry {"id": p, "index": i, "w": w_p, "pos": pos_i}:
- base_bias = tanh(lambda_m * w_p + pos_i * renorm_alpha)
- Apply Monster group stabilization: modulate by cos(2*pi*w_p) to encode group periodicity
- Final: bias = tanh(base_bias * (1 + 0.1 * cos(2*pi*w_p)))
- Each token MUST have a distinct bias value

Return ONLY valid JSON: {"bias": [float, float, ...]} with exactly one float per token.
No explanation. No markdown."""


@app.route(route="memory", auth_level=func.AuthLevel.FUNCTION)
def memory(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
        token_ids = body.get("token_ids", [])

        if not token_ids:
            return func.HttpResponse(
                json.dumps({"bias": []}),
                mimetype="application/json",
                status_code=200
            )

        n = len(token_ids)
        # Pre-compute per-token inputs so GPT-4o can't collapse them
        tokens = []
        for i, p in enumerate(token_ids):
            w_p = 1.0 / (abs(p) + 1)
            pos = (i - n / 2.0) / max(n, 1)
            tokens.append({"id": p, "index": i, "w": round(w_p, 8), "pos": round(pos, 8)})

        from openai import AzureOpenAI
        client = AzureOpenAI(
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_key=os.environ["AZURE_OPENAI_KEY"],
            api_version="2024-08-01-preview"
        )
        deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")

        user_message = json.dumps({
            "tokens": tokens,
            "lambda_m": LAMBDA_M,
            "renorm_alpha": RENORM_ALPHA,
            "expected_bias_count": n
        })

        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.0,
            max_tokens=256,
            response_format={"type": "json_object"}
        )

        result = json.loads(response.choices[0].message.content)
        bias = result.get("bias", [0.0] * n)

        # Fallback: if GPT-4o still collapses, compute deterministically
        if len(bias) != n or len(set(round(b, 6) for b in bias)) == 1:
            bias = [
                math.tanh(LAMBDA_M * (1.0 / (abs(p) + 1)) +
                          ((i - n / 2.0) / max(n, 1)) * RENORM_ALPHA)
                for i, p in enumerate(token_ids)
            ]

        bias = [max(-1.0, min(1.0, float(b))) for b in bias]

        return func.HttpResponse(
            json.dumps({"bias": bias, "model": deployment}),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)
