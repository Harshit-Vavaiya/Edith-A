import random
import json
import requests
import torch
from bs4 import BeautifulSoup
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from search import search
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')



def getResponse(q='hi'):
  with open('intents.json', 'r') as json_data:
      intents = json.load(json_data)

  FILE = "data.pth"
  data = torch.load(FILE)

  input_size = data["input_size"]
  hidden_size = data["hidden_size"]
  output_size = data["output_size"]
  all_words = data['all_words']
  tags = data['tags']
  model_state = data["model_state"]

  model = NeuralNet(input_size, hidden_size, output_size).to(device)
  model.load_state_dict(model_state)
  model.eval()

  bot_name = "Edith"
  print("Let's chat! (type 'quit' to exit)")
 
  sentence = tokenize(q)
  X = bag_of_words(sentence, all_words)
  X = X.reshape(1, X.shape[0])
  X = torch.from_numpy(X).to(device)

  output = model(X)
  _, predicted = torch.max(output, dim=1)

  tag = tags[predicted.item()]

  probs = torch.softmax(output, dim=1)
  prob = probs[0][predicted.item()]
  if prob.item() > 0.75:
    if tag == 'search':
      return search(sentence)     
      
    else:
      for intent in intents['intents']:
          if tag == intent["tag"]:
              return {'response': random.choice(intent['responses']) }
  else:
    return { 'response' : 'I do not understand...'}