import torch
import logging
from transformers import pipeline, Pipeline
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

class AccentClassificationError(Exception):
    """Raised when accent classification fails."""

class AccentClassifier:
    """
    Uses a Hugging Face audio-classification pipeline to predict English accents.
    """

    def __init__(
        self,
        model_name: str = "dima806/english_accents_classification",
        device: int = None,
        top_k: int = 3
    ) -> None:
        device = device if device is not None else (0 if torch.cuda.is_available() else -1)
        try:
            self._pipe: Pipeline[Any, Any] = pipeline(
                task="audio-classification",
                model=model_name,
                device=device,
                top_k=top_k
            )
            logger.info("Loaded model %s on device %s", model_name, device)
        except Exception as e:
            logger.error("Failed to load model %s: %s", model_name, e)
            raise AccentClassificationError(f"Model init failed: {e}")

    def classify(self, wav_path: str) -> Dict[str, Any]:
        """
        Return a dict with:
          - accent: best label
          - confidence: best score * 100
          - top_n: list of top-K {"accent", "probability"}
          - info: model ID
        """
        try:
            results: List[Dict[str, float]] = self._pipe(wav_path)
            top_n = [
                {"accent": r["label"], "probability": r["score"] * 100.0}
                for r in results
            ]
            best = top_n[0]
            return {
                "accent": best["accent"],
                "confidence": best["probability"],
                "top_n": top_n,
                "info": f"Model: {self._pipe.model.name_or_path}"
            }
        except Exception as e:
            logger.error("Classification failed on %s: %s", wav_path, e)
            raise AccentClassificationError(f"Classification failed: {e}")
