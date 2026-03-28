import azure.functions as func
import json

app = func.FunctionApp()

@app.route(route="memory", auth_level=func.AuthLevel.FUNCTION)
def memory(req: func.HttpRequest) -> func.HttpResponse:
    try:
        token_ids = req.get_json().get("token_ids", [])
        return func.HttpResponse(json.dumps({"bias": [0.0] * len(token_ids)}), mimetype="application/json")
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)
