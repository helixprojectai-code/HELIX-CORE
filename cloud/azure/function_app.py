import azure.functions as func
import json
import os

app = func.FunctionApp()

SYSTEM_PROMPT = """You are the FZS-MK Memory Kernel — a Functorial Zeno Sheaf with Memory Kernel.

Your role in the Helix Constitutional Runtime:
- You receive prime-indexed section coordinates (token_ids)
- You compute memory-modulated bias values for each coordinate
- Each bias reflects the semantic inertia and sheaf morphism weight at that prime index
- Bias values must be bounded in [-1.0, 1.0]
- You must return ONLY valid JSON: {"bias": [float, ...]}

Ontology (ADR-SHF-001):
- prime_indexed_section: local sheaf section keyed by prime-associated coordinates
- recursive_operator_xi_t: state evolution operator Xi(t)
- lambda_m: multiplicity constant for curvature modulation (lambda_m = ln(10))
- monster_group_memory_kernel: stabilization mechanism based on Monster group actions
- semantic_inertia: mass-like property of the semantic field at each coordinate

For each token_id p at index i:
- Compute the prime-harmonic weight: w_p = 1/(p+1)
- Compute position bias: pos = (i - len(token_ids)/2) / max(len(token_ids), 1)
- Apply memory modulation: bias_p = tanh(lambda_m * w_p + pos * renorm_alpha)
- Return the bias vector with non-zero values

Return ONLY JSON. No explanation. No markdown."""


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

        from openai import AzureOpenAI
        client = AzureOpenAI(
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_key=os.environ["AZURE_OPENAI_KEY"],
            api_version="2024-08-01-preview"
        )
        deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")

        user_message = json.dumps({
            "token_ids": token_ids,
            "lambda_m": 2.302585092994046,
            "renorm_alpha": 0.15915494309189535
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
        bias = result.get("bias", [0.0] * len(token_ids))

        # Safety clamp to [-1, 1]
        bias = [max(-1.0, min(1.0, float(b))) for b in bias]

        return func.HttpResponse(
            json.dumps({"bias": bias, "model": deployment}),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)
