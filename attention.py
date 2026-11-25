"""One causal self-attention head over eight pitch tokens, trained on next-note loss."""
from functools import lru_cache
import math
import random


def softmax(logits):
    peak = max(logits)
    weights = [math.exp(x - peak) for x in logits]
    total = sum(weights)
    return [w / total for w in weights]


class PitchHead:
    def __init__(self, vocab):
        self.vocab = vocab
        self.index = {p:i for i,p in enumerate(vocab)}
        self.keys = [[0.] * len(vocab) for _ in vocab]
        self.values = [[0.] * len(vocab) for _ in vocab]
        self.bias = [0.] * 4

    def forward(self, prefix):
        tokens = [self.index[p] for p in prefix[-4:]]
        query = tokens[-1]
        # Dotting a fixed one-hot query with a learned key selects one component.
        scores = [self.keys[t][query] + self.bias[len(tokens)-1-i] for i,t in enumerate(tokens)]
        attention = softmax(scores)
        logits = [sum(a*self.values[t][j] for t,a in zip(tokens,attention)) for j in range(len(self.vocab))]
        return tokens, attention, softmax(logits)

    def update(self, prefix, target, rate):
        tokens, attention, probs = self.forward(prefix)
        probs[self.index[target]] -= 1  # cross-entropy gradient wrt logits
        grad = [sum(g*v for g,v in zip(probs,self.values[t])) for t in tokens]
        average = sum(a*g for a,g in zip(attention,grad))
        for i,(t,a,g) in enumerate(zip(tokens,attention,grad)):
            step = rate*a*(g-average)
            self.keys[t][tokens[-1]] -= step
            self.bias[len(tokens)-1-i] -= step
            for j,error in enumerate(probs):
                self.values[t][j] -= rate*a*error


@lru_cache(maxsize=4)
def train(phrases, vocab):
    model = PitchHead(vocab)
    examples = [(p[:i],p[i]) for p in phrases for i in range(1,len(p))]
    rng = random.Random(17)
    for _ in range(35):
        rng.shuffle(examples)
        for prefix,target in examples:
            model.update(prefix,target,.08)
    return model
