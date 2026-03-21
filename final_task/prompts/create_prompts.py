"""
Создание нескольких версий промптов в MLflow Prompt Storage.
Запускать при поднятом MLflow: MLFLOW_TRACKING_URI=http://localhost:5000
"""

import mlflow

mlflow.set_tracking_uri("http://localhost:5000")

# Версия 1
mlflow.register_prompt(
    name="classification_prompt",
    template="Classify the following text into one of the categories: {categories}.\n\nText: {text}\n\nCategory:",
    commit_message="v1: basic classification prompt",
)

# Версия 2, с instruction
mlflow.register_prompt(
    name="classification_prompt",
    template=(
        "You are a helpful assistant. "
        "Classify the following text into exactly one of the categories: {categories}.\n\n"
        "Text: {text}\n\n"
        "Respond with only the category name."
    ),
    commit_message="v2: added system instruction and strict output format",
)

# Версия 3, с few-shot
mlflow.register_prompt(
    name="classification_prompt",
    template=(
        "You are a helpful assistant. "
        "Classify the following text into exactly one of the categories: {categories}.\n\n"
        "Examples:\n"
        '- "I love this product" -> Positive\n'
        '- "Terrible experience" -> Negative\n\n'
        "Text: {text}\n\n"
        "Category:"
    ),
    commit_message="v3: added few-shot examples",
)

# Отдельный промпт для суммаризации
mlflow.register_prompt(
    name="summarization_prompt",
    template="Summarize the following text in {max_sentences} sentences:\n\n{text}\n\nSummary:",
    commit_message="v1: basic summarization prompt",
)

print("Успех!")