import torch
from pytorch_pretrained_bert import BertTokenizer, BertModel, BertForMaskedLM


# Original/standard pre-trained model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased') 

# Sciencey pre-trained model
# tokenizer = BertTokenizer.from_pretrained('/Users/katy/Documents/Grad/tech-tweets/data/scibert_scivocab_uncased')
# model = BertModel.from_pretrained('/Users/katy/Documents/Grad/tech-tweets/data/scibert_scivocab_uncased')

# Put the model in "evaluation" mode, meaning feed-forward operation.
model.eval()

def prep_sentence(plaintext, pprint=False):
    """Take plain text and return indexed tokens and segment ids."""

    # Add the special tokens.
    marked_text = "[CLS] " + plaintext + " [SEP]"
    # Split the sentence into tokens.
    tokenized_text = tokenizer.tokenize(marked_text)
    if pprint:
        print(tokenized_text)
    # Map the token strings to their vocabulary indeces.
    indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)
    # Mark each of the 22 tokens as belonging to sentence "1".
    segments_ids = [1] * len(tokenized_text)

    return indexed_tokens, segments_ids


def get_embeddings(indexed_tokens, segments_ids, pprint=False):
    """Return tensor of embeddings. [# tokens, # layers, # hidden units]"""

    # Convert inputs to PyTorch tensors
    tokens_tensor = torch.tensor([indexed_tokens])
    segments_tensors = torch.tensor([segments_ids])

    # Predict hidden states features for each layer
    with torch.no_grad():
        encoded_layers, _ = model(tokens_tensor, segments_tensors)

    # Current dimensions:
    # [# layers, # batches, # tokens, # features]
    # Desired dimensions:
    # [# tokens, # layers, # features]

    # Concatenate the tensors for all layers. We use `stack` here to
    # create a new dimension in the tensor.
    token_embeddings = torch.stack(encoded_layers, dim=0)
    # Remove dimension 1, the "batches".
    token_embeddings = torch.squeeze(token_embeddings, dim=1)
    # Swap dimensions 0 and 1.
    token_embeddings = token_embeddings.permute(1,0,2)

    return token_embeddings


def get_sentvector(token_embeddings):
    """Return one embedding for whole sentence."""
    # `token_embeddings` has shape [22, 12, 768]

    # `token_vecs` is a tensor with shape [22 x 768]
    # select second to last layer
    token_vecs = token_embeddings.select(1,11)

    # Calculate the average of all 22 token vectors.
    sentence_embedding = torch.mean(token_vecs, dim=0)
    return sentence_embedding


def sent_emb_from_text(plaintext, pprint=False):
    indexed_tokens, segments_ids = prep_sentence(plaintext, pprint=pprint)
    token_embeddings = get_embeddings(indexed_tokens, segments_ids)
    return get_sentvector(token_embeddings)
