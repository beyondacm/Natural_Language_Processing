import math, collections

class CustomLanguageModel:


  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    # TODO your code here
      
    self.uniGramCounts = collections.defaultdict( lambda : 0)
    self.biGramCounts = collections.defaultdict( lambda : 0)
    
    self.afterWordCounts = collections.defaultdict( lambda: 0)
    self.beforeWordCounts = collections.defaultdict( lambda: 0)
    
    self.total = 0
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    # TODO your code here
    
    for sentence in corpus.corpus:
        datums = sentence.data
        for i in range(len(datums)):
            self.total += 1
            token_i = datums[i].word
            self.uniGramCounts[token_i] += 1
            if i >= 1:
                token_i_1 = datums[i-1].word
                bi_key = token_i_1 + ',' + token_i
                self.biGramCounts[bi_key] += 1
    
    for token in self.uniGramCounts.keys():
        self.afterWordCounts[token] = self.countAfterKeyPartInDict(self.biGramCounts, token)
        self.beforeWordCounts[token] = self.countBeforeKeyPartInDict(self.beforeWordCounts, token)
    
    pass

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    # TODO your code here
    score = 0
    d = 0.75
    for i in range(len(sentence)) :
        if i >= 1:
            bi_key = sentence[i-1] + ',' + sentence[i]
            count_bigram = self.biGramCounts[bi_key]
            if count_bigram > 0:
                count_afterword = self.afterWordCounts[ sentence[i-1] ]
                count_beforeword = self.beforeWordCounts[ sentence[i] ] 
                count_unigram = self.uniGramCounts[ sentence[i-1] ] 
                # count lambda
                if count_unigram == 0:
                    lambda_i_1 = d * 0.1
                else :
                    lambda_i_1 = (d / float(count_unigram)) * float(count_afterword)
    
                # count p_continuation
                p_continuation = float(count_beforeword + 1) / (float(len(self.biGramCounts)) * 2)
                

                score = float((count_bigram -d)) / float(count_unigram) + lambda_i_1 * p_continuation
                score = math.log(score)
            else :
                count_unigram = self.uniGramCounts[ sentence[i] ] 
                score += math.log(count_unigram + 1)
                self.total += 1
                score -= math.log(self.total)
                score += math.log(0.4)
    
    return score
    #return 0.0
  

  def countAfterKeyPartInDict(self, dict, key_first_part):
    num = 0
    # TODO
        
    return num

  def countBeforeKeyPartInDict(self, dict, key_last_part):
     num = 0
     # TODO

     return num 
        

