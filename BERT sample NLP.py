#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import torch
from transformers import BertTokenizer, BertForTokenClassification

# Load the pre-trained BERT model
model = BertForTokenClassification.from_pretrained("bert-base-cased")
tokenizer = BertTokenizer.from_pretrained("bert-base-cased")

# Encode the input text
text = "In Paris, the Louvre Museum is one of the largest art museums in the world."
input_ids = torch.tensor([tokenizer.encode(text, add_special_tokens=True)])

# Generate the attention masks to indicate which tokens are actual words
attention_masks = torch.where(input_ids != 0, torch.tensor(1), torch.tensor(0))

# Pass the input to the BERT model for entity recognition
outputs = model(input_ids, attention_mask=attention_masks)

# Get the predicted entity labels for each token
predicted_labels = torch.argmax(outputs[0], dim=2)

# Convert the predicted labels back to their original string representation
label_map = {i: label for i, label in enumerate(model.config.id2label)}
predicted_labels = [label_map[p.item()] for p in predicted_labels[0]]

# Print the predicted entities for each word in the input text
for word, label in zip(text.split(), predicted_labels):
    print(f"{word}: {label}")


# In[ ]:




