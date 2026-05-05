# src/services/metrics_service.py

def calculate_metrics(
    tp: int,
    tn: int,
    fp: int,
    fn: int,
    first_relevant_rank: int = 1,
    ranks: list[int] | None = None
):
    total = tp + tn + fp + fn

    # Classification metrics
    accuracy = (tp + tn) / total if total else 0
    precision = tp / (tp + fp) if (tp + fp) else 0
    recall = tp / (tp + fn) if (tp + fn) else 0

    f1 = 0
    if precision + recall:
        f1 = 2 * (precision * recall) / (precision + recall)

    # Ranking metrics
    rr = 1 / first_relevant_rank if first_relevant_rank else 0

    mrr = 0
    if ranks:
        rr_list = [(1 / r) if r else 0 for r in ranks]
        mrr = sum(rr_list) / len(rr_list)

    return {
        "accuracy": round(accuracy, 3),
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "f1": round(f1, 3),
        "rr": round(rr, 3),
        "mrr": round(mrr, 3),
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn
    }