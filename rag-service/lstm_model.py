import torch
from transformers import AutoTokenizer
import os
import model_inteface

DEVICE = os.getenv("device", "cuda" if torch.cuda.is_available() else "cpu")
MODEL_FILE = os.getenv("model_path", "model.pt")

class Attention(torch.nn.Module):
    def __init__(self, hidden_size):
        super(Attention, self).__init__()
        self.attention = torch.nn.Linear(hidden_size, 1, bias=False)

    def forward(self, lstm_output):
        # lstm_output: (batch_size, seq_len, hidden_size)
        scores = self.attention(lstm_output).squeeze(-1)  # (batch_size, seq_len)
        weights = torch.nn.functional.softmax(scores, dim=1)  # (batch_size, seq_len)
        context = torch.sum(weights.unsqueeze(-1) * lstm_output, dim=1)  # (batch_size, hidden_size)
        return context, weights
    
class LSTMModel(torch.nn.Module):
        
    def __init__(self, vocab_size, hidden_dim, encoding_dim, num_layers = 1, dropout=0.1,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.embeder = torch.nn.Embedding(vocab_size, hidden_dim, padding_idx=vocab_size-1 )
        self.lstm = torch.nn.LSTM(hidden_dim, hidden_size=hidden_dim, num_layers=num_layers,dropout=dropout, batch_first=True)
        self.fc = torch.nn.Linear(hidden_dim * 2, encoding_dim)
        self.attention = Attention(hidden_dim)
        
    def forward(self, X, mask=None):
        emb = self.embeder(X)
        out, (hidden, c) = self.lstm(emb)
        
        attention_res, _  = self.attention(hidden.permute(1,0,2))
        return self.fc(torch.cat([hidden[-1], attention_res], dim=1))
    

class LSTMDecorator(model_inteface.Model):

    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct")
        hidden = 512
        embed = 256

        self.model = LSTMModel(self.tokenizer.vocab_size+1, hidden, embed, 2)
        self.model.load_state_dict(torch.load(MODEL_FILE, weights_only=True, map_location=torch.device(DEVICE)))

        for param in self.model.parameters():
            param.requires_grad = False
            
        self.model.eval()

    @torch.no_grad()
    def embed_batch(self, x):
        tokenized = self.tokenizer.batch_encode_plus(x, padding=True, max_length=1024, truncation=True, return_tensors="pt", return_length=False)["input_ids"]
        embeded = self.model(tokenized)
        return embeded.cpu().numpy()

    @torch.no_grad()
    def embed(self, x):
        tokenized = self.tokenizer(x, return_tensors="pt")["input_ids"]
        embeded = self.model(tokenized)[0]
        return embeded.cpu().numpy()
    
    def get_device(self):
        return DEVICE
