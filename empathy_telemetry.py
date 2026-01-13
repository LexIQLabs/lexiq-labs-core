# empathy_telemetry.py

import re
from typing import Dict

# ─────────────────────────────────────────
# Configuration (tunable, explicit)

NEGATIVE_KEYWORDS = [
    "frustrated", "angry", "upset", "annoyed", "ridiculous",
    "unacceptable", "disappointed", "terrible", "worst",
    "waste", "complaint", "issue", "problem", "fed up",
    "not happy", "unsatisfied", "irritated"
]

MAX_SCORE = 100


# ─────────────────────────────────────────
# Helper functions

def _count_excess_punctuation(text: str) -> int:
    """Counts emotionally charged punctuation."""
    return len(re.findall(r"[!?]{2,}", text))


def _count_all_caps_words(text: str) -> int:
    """Counts ALL CAPS words longer than 2 letters."""
    return len(re.findall(r"\b[A-Z]{3,}\b", text))


def _average_sentence_length(text: str) -> float:
    sentences = re.split(r"[.!?]+", text)
    sentences = [s.strip() for s in sentences if s.strip()]
    if not sentences:
        return 0.0
    return sum(len(s.split()) for s in sentences) / len(sentences)


def _negative_keyword_hits(text: str) -> int:
    text_lc = text.lower()
    return sum(1 for kw in NEGATIVE_KEYWORDS if kw in text_lc)


# ─────────────────────────────────────────
# Main empathy telemetry function

def calculate_emo_score(text: str) -> Dict:
    """
    Calculates an EmoScore™ (0–100) indicating emotional intensity.

    Returns:
    {
        "emo_score": int,
        "level": "low" | "medium" | "high",
        "signals": {
            "punctuation": int,
            "all_caps": int,
            "negative_keywords": int,
            "sentence_length": float
        }
    }
    """

    if not text or not text.strip():
        return {
            "emo_score": 0,
            "level": "low",
            "signals": {}
        }

    punctuation_hits = _count_excess_punctuation(text)
    caps_hits = _count_all_caps_words(text)
    neg_hits = _negative_keyword_hits(text)
    avg_sentence_len = _average_sentence_length(text)

    score = 0

    # Punctuation intensity
    score += min(punctuation_hits * 8, 25)

    # ALL CAPS intensity
    score += min(caps_hits * 10, 30)

    # Negative emotion language
    score += min(neg_hits * 12, 35)

    # Sentence spikiness (short abrupt sentences)
    if avg_sentence_len and avg_sentence_len < 6:
        score += 10

    score = min(score, MAX_SCORE)

    if score >= 65:
        level = "high"
    elif score >= 35:
        level = "medium"
    else:
        level = "low"

    return {
        "emo_score": score,
        "level": level,
        "signals": {
            "punctuation": punctuation_hits,
            "all_caps": caps_hits,
            "negative_keywords": neg_hits,
            "sentence_length": round(avg_sentence_len, 1)
        }
    }
