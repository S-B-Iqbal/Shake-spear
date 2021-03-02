from text_stats     import *
from collections    import OrderedDict
from random         import choices

class GenerateText(TextStats):
    def __init__(self, text, word = None, max_words = 500):
        super().__init__(text)
        self.word = word
        if isinstance(max_words, str):
            self.max_words = int(max_words)
    @property
    def is_in_tokens(self):
        """Function to check whether "word" is in the text file or not"""
        if self.word not in self.tokens:
            raise ValueError("This word is not in the text. Please enter a different word!")
        else:
            return True
    @property
    def gen_text(self):
        if self.is_in_tokens:
            curr_word = self.word
            msg = curr_word
            counter = 0
            next_word_counter = {} # Acts a a counter-cache, to avoid multiple word-frequency calculations.
            try:
                while(counter<self.max_words):
                    ## Frequency for all the next words after 'curr_word'
                    if curr_word not in next_word_counter.keys():
                        count_next_word = Counter([self.tokens[i+1] for i,word in enumerate(self.tokens) if word ==curr_word]) 
                        count_next_word = OrderedDict(count_next_word.most_common()) # To preserve order
                        next_word_counter[curr_word] = count_next_word
                        next_pred, *_ = choices(population=[*count_next_word.keys()], weights=count_next_word.values(), k=1) # generate randomly only 1 word
                        curr_word = next_pred # Update curr_word
                        msg = " ".join([msg, curr_word])
                        counter +=1 
                    else:
                        count_next_word = next_word_counter[curr_word]
                        next_pred, *_ = choices(population=[*count_next_word.keys()], weights=count_next_word.values(), k=1) # generate randomly only 1 word
                        curr_word = next_pred # Update curr_word
                        msg = " ".join([msg, curr_word])
                        counter +=1 
                return msg
            except IndexError:
                print(f"No next word for the word :{self.word}")

    

if __name__ == '__main__':
    input = get_user_input()
    file_name, word, max_words = input
    TEXT= get_file(file_name=file_name) # Save the searched Text file
    
    text_obj = GenerateText(text=TEXT, word= word, max_words= max_words)

    print(text_obj.gen_text) 


