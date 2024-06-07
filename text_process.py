def text_processing_pipeline(text):
    def Tok_nize(text):  
        return text.split()
    
    def rmv_stopwrd(tokens, stopwords): 
        cleaned_tokens = []
        
        print("Tokens after stopword removal:", cleaned_tokens)
    
    def calc_Freq(tokens): 
        frequency = {}
        for token in tokens:
            if token in frequency:
                frequency[token] += 1
            else:
                frequency[token] = 1
        # missing return statement
        print("Token frequency:", frequency)
    
    def detect_sentiment(text):  
        print("Sentiment detection not implemented")
        return "Neutral"  

    # Main processing steps
    tokens = Tok_nize(text)
    stopwords = ["the", "and", "is", "in", "to", "of"]  
    rmv_stopwrd(tokens, stopwords)
    calc_Freq(tokens)
    sentiment = detect_sentiment(text)
    
    print("Processed tokens:", tokens)
    print("Sentiment:", sentiment)
