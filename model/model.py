import textblob
import numpy as np
import pickle 

def get_result(message):
    print(message)
    # 모델 불러오기
    f = open('/Users/hee/git/metaverse_patrol/model/forest_model.pickle', 'rb')
    forest_model = pickle.load(f)
    f.close()

    # 입력 형식 맞추기
    lst = [0] * 504
    lst[0] = textblob.TextBlob(message).sentiment.polarity
    lst[1] = textblob.TextBlob(message).sentiment.subjectivity
    lst[2] = int(np.where(message.lower().__contains__("you"), 1, 0))
    lst[3] = len(message)
    # lst[indexofbad] = 1
    lst = np.array(lst)
    insult_transformed = lst.reshape(1, -1)
    
    result = forest_model.predict(insult_transformed)[0]
    xwords = ["kiss", "sex", "body", "secret", "underwear", "fuck"]
    if any ((c in xwords) for c in message):
        result = 1
    return result
    