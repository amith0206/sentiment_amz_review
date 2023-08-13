from textblob import TextBlob

def get_sentiment(sentence):
    blob=TextBlob(sentence)
    
    polarity=blob.sentiment.polarity
    return polarity

def check(polarity):
     if polarity>0:
                print('Positive')
                print('Polarity :',polarity)
    
     elif polarity<0:
                print('Negative') 
                print('Polarity :',polarity)
     else:
                print('Neutral')
                print('Polarity : 0') 
    
    
if(__name__=="__main__"):
    sentence=input('Enter a sentence')
    polarity=get_sentiment(sentence) 
    check(polarity)
    while True:
        user_input=input("Do you want to continue Y/N")
        if user_input in ['Y','y','yes']:
            sentence=input('Enter a sentence')
            polarity=get_sentiment(sentence)
            check(polarity)
        else:
            print('Thank you')
            break
                   
        
        