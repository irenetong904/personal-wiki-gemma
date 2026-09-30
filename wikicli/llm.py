"""Thin wrapper around the local Ollama server. The model only sees what we pass in `messages`."""
import time

from . import config


class ModelUnavailable(RuntimeError):
    pass


def _client():
    import ollama
    return ollama.Client(host=config.OLLAMA_HOST)


def check_model() -> None:
    """Fail early with an actionable message if Ollama or the model is missing."""
    try:
        models = _client().list()
    except Exception as e:  # connection refused, etc.
        raise ModelUnavailable(
            f"Cannot reach Ollama at {config.OLLAMA_HOST} ({e.__class__.__name__}).\n"
            "Start it with:  brew services start ollama   (or: ollama serve)"
        ) from e
    names = {m.model for m in models.models}
    if config.MODEL not in names:
        raise ModelUnavailable(
            f"Model '{config.MODEL}' is not downloaded. Run (while online):  ollama pull {config.MODEL}"
        )


def chat(messages, temperature=0.2, json_format=False):
    """Send messages to local Gemma. Returns (text, stats dict)."""
    check_model()
    t0 = time.perf_counter()
    resp = _client().chat(
        model=config.MODEL,
        messages=messages,
        format="json" if json_format else None,
        options={"temperature": temperature, "num_ctx": config.NUM_CTX},
        keep_alive="10m",
    )
    elapsed = time.perf_counter() - t0
    stats = {
        "model": config.MODEL,
        "execution": "local",
        "seconds": round(elapsed, 2),
        "prompt_tokens": resp.get("prompt_eval_count"),
        "output_tokens": resp.get("eval_count"),
    }
    return resp["message"]["content"], stats
