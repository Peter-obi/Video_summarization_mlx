import os
import spacy
import tiktoken
from mlx_lm import load, generate

PROMPT = """
Create a bullet point summary of the text that will follow after the heading `TEXT:`. 

Do not just list the general topic, but the actual facts that were shared.

For example, if a speaker claims that "a dosage of X increases Y", do not
just write "the speaker disusses the effects of X", instead write "a dosage 
of X increases Y".

Use '- ' for bullet points:

After you have made all bullet points, add one last bullet point that 
summarizes the main message of the content, like so:

- Main message: [MAIN MESSAGE HERE]

---

TEXT TITLE: {title}

TEXT:
{chunk}


"""

MODEL_MAX_TOKENS = 8192  # Maximum tokens for prompt and response
WINDOW_SIZE = 4096  # Maximum tokens for the input

def count_tokens(text, tokenizer):
    """Count tokens in a text string using the MLX model's tokenizer."""
    tokens = tokenizer.encode(text)
    return len(tokens)

# Load MLX model and tokenizer
model, tokenizer = load("mlx-community/Mistral-7B-Instruct-v0.2-4bit-mlx")

def split_text(text_path=None, title=None):
    """
    Split text into chunks considering the MLX model's window size.
    """
    prompt_tokens = count_tokens(PROMPT.format(chunk="", title=title), tokenizer)
    max_tokens = WINDOW_SIZE - prompt_tokens

    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("sentencizer")

    with open(text_path, "r") as f:
        text = f.read()

    doc = nlp(text, disable=["tagger", "parser", "ner", "lemmatizer", "textcat"])
    chunks = []
    current_chunk = []

    for sent in doc.sents:
        sent_text = sent.text.strip()
        sent_tokens = count_tokens(sent_text, tokenizer)

        if sum(count_tokens(chunk, tokenizer) for chunk in current_chunk) + sent_tokens > max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sent_text]
        else:
            current_chunk.append(sent_text)

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def summarize_with_mlx(chunk=None, title=None):
    """
    Generates a summary for a chunk of text using the MLX model.
    """
    prompt = PROMPT.format(chunk=chunk, title=title)
    print("Generating summary with MLX model...")
    return generate(model, tokenizer, prompt=prompt, max_tokens=MODEL_MAX_TOKENS - count_tokens(prompt, tokenizer))

def summarize_in_parallel(chunks):
    """
    Calls the MLX model to summarize each chunk of text.
    """
    summaries = [summarize_with_mlx(chunk) for chunk in chunks]
    return summaries

def save_summaries(summaries, filename_only, output_dir="files/summaries"):
    # Add the following lines to create the directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    summary_path = os.path.join(output_dir, f"{filename_only}.txt")
    with open(summary_path, "w") as f:
        for summary in summaries:
            f.write(summary)
            f.write("\n\n")
    return summary_path
