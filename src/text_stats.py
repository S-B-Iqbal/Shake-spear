
import  sys
import  re
from    collections import Counter
from    pathlib     import Path
from    time        import sleep

def get_user_input():
    """Function to get command-line argument from user in terminal
    Example:
    -------
    >>> python3 ./text_stats.py shakespeare.txt hamlet 2000

    Raises:
        ValueError: If no input is provided in the terminal.
    """
    # If only '.py' file exists without the arguments
    if len(sys.argv) == 1:
        raise ValueError("filename cannot be empty! Please provide a valid filename")
    if len(sys.argv)==2:
        file_name = sys.argv[1] # Saves the final passed argument to the terminal
        return [Path(str(file_name))]# returns a Path wrapper to resolve OS based PATH conflicts.
    if len(sys.argv)>=3:
        return sys.argv[1:]

def get_file(file_name, *args, **kwargs):
    """Function to get the contents of the file from the user.
    - The Function performs a search in the 'current working directory' and its sub-directories.
    - The Function reads the content of the file.
    - The Function returns the content of the file
    Params:
    ------
    file_name: str, <filename> to be searched in the current directory and its subdirectories.

    Returns:
    -------
    TEXT: str, all the contents of the file.
    
    Example:
    -------
    >>> text_file = get_file('shakespeare.txt', encoding = 'utf8')

    Raises:
        FileNotFoundError: If the <filename> does not exist in the directory and its sub-directories.
    """
    file_to_find = file_name
    search_result = sorted(Path('.').glob(f"**/*{file_name}"))
    if search_result:
        full_path =  Path.cwd() / Path(search_result[-1]) ## OS agnostic path
        ## Read file with 'UTF-8' encoding
        with open(full_path, mode='r', encoding='utf8') as f:
            TEXT = f.read()
        return(TEXT)

    else:
        raise FileNotFoundError("The file does not exist!")

def write_to_file(file_name, writeable_data):
    """Function to write output in the file provided in the PATH = <file_name>
    Params:
    ------
    file_name: str, file to be searched in rcurrent-working and its sub-directories.
    writeable_data: str, data to be written in the given file, provided the file exists
    """
    file_to_find = file_name
    search_result = sorted(Path('.').glob(f"**/*{file_name}"))
    if search_result:
        full_path =  Path.cwd() / Path(search_result[-1]) ## OS agnostic path
        sleep(3)
        print("Writing....")
        with open(full_path, mode='w') as f:
            f.writelines('\n')
            for data in writeable_data:
                
                f.writelines(f"\n{data}") # Data Object written in the file.
                f.writelines("\n********************************************\n")

class TextStats(object):
    def __init__(self, text):
        self.text           = text
        self._tokens        = [] # List of unique words in 'text'
        self._word_counter   = {} # Dict of Word Frequecy
        self.letter_freq    = "" # Saved as string for aesthetical representation
        self.freq_table     = "" # Saved as string for aesthetical representation
        self._total_words   = None # Count of total no of words in the provided text
        self._unique_words  = None # Count of total unique words in the provided text
        self._top_five      = None # List of Top-5 words and their frequency
        self._top_five_next = None # Dictionary of next-word and their frequency of top-5 words
        
    @property
    def tokens(self):
        """Function to get the list of all the words in the Text. 
        - The Text is normalized to lowercase.
        - The Text ignored numbers,punctuations, etc.
        Params:
        ------
        text: str
        Returns:
        -------
        List[str]: List of tokenized words.
        """
        if not self._tokens:
            self._tokens = re.findall("[a-z’]+", self.text.lower())
        return self._tokens
    @property
    def word_counter(self):
        """Returns a counter for tokenized words"""
        if not self._word_counter:
            self._word_counter = Counter(self.tokens)
        return self._word_counter
    
    @property
    def get_letters_freq(self):
        """Function to get the frequency table of most common 'letters' ordered from most common to the least.
    
        Example:
        ------
        >>> print(TextStats.get_letters_freq("Aa BBb"))
        [Out]:  |--------- Frequency Table for Letters ---------|
                |  b    | 3
                |  a    | 2
                |-----------------------------------------------|
        """
        new_text = "".join(self.tokens).translate({ord('’'): None}) # We do not count <backspace> and ’ character
        letters_counter = Counter(new_text) # Counter dictionary on letters
        begin   = "|--- Frequency Table for Letters ---|"
        end     = " |-----------------------------------|"
        letter_counts    = '\n'.join(f" |  {k}{' '*5}| {v}" for (k,v) in letters_counter.most_common())
        if  not self.letter_freq:
            self.letter_freq += '\n'.join((begin,letter_counts,end))
        return self.letter_freq
    
    @property
    def get_total_words(self):
        """Function to get total number of words based on tokens()"""
        if self._total_words  is None:
            self._total_words = len(self.tokens)
        return f"The total words in the file are {self._total_words}"

    @property
    def get_unique_words(self):
        """Function to get total unique words in the provided text based on tokens()"""
        if self._unique_words is None:
            self._unique_words =  {word for word in self.tokens} # Create a set of unique words
        return f"The total unique words in the file are {len(self._unique_words)}"
        
    @property
    def get_word_freq(self):
        """Function to get the frequency of top-5 words in text. 
        Params:
        ------
        n: int[Default=5]; No. of words whose frequency needs to be calculated.
        Returns:
        -------
        self._top_five_next: tuple, Counter of next-words and their frequency as next words
        self._top_five : List[(word, frequency)], List of top-5 words and their frequency
        """
        words =  self.word_counter # Token frequency
        top_five = words.most_common(5) # Frequency of top-5 words
        top_five_words = [w[0] for w in words.most_common(5)] # List of top-5 words
        # Condition to count next word of most frequent word
        next_word = lambda x: Counter((self.tokens[i+1] for i,w in enumerate(self.tokens) if w == x)) 
        top_five_next = tuple(map(next_word,top_five_words)) # Tuple of most common next word of 'top_five_words'
        top_five_next = tuple(map(Counter.most_common, top_five_next)) # Sorted tuple of 'top_five_next'
        top_five_next = {k:v for k,v in zip(top_five_words, top_five_next)}
        self._top_five = top_five
        self._top_five_next = top_five_next
        return self._top_five_next, self._top_five

    @property
    def print_word_freq(self):
        """Function to print the results of get_word_freq()"""
        followed_word_freq,top_words = self.get_word_freq
        for word in top_words:
            # print(f"{word[0]} ({word[1]} occurences)")
            self.freq_table  += f"{word[0]} ({word[1]} occurences)\n"
            # Print top-3 next word and frequency
            for i,counts in enumerate(followed_word_freq):
                if i<=3:
                    # returns "--- <word>, <word-frequency>"
                    self.freq_table  += f"--- {followed_word_freq[word[0]][i][0]}, {followed_word_freq[word[0]][i][1]}\n"
                else:
                    pass
        return(self.freq_table)

if __name__ == '__main__':
    input= get_user_input() # Save user input
    # print(input)
    TEXT= get_file(file_name=input[0]) # Save the searched Text file
    # del(text_obj)
    txt = TextStats(text=TEXT)
    ##### Print the required metrics #####
    print('\n',txt.get_letters_freq) # Letter Frequency Table
    print('\n',txt.get_total_words) # Total No of words
    print('\n',txt.get_unique_words) # Total unique words
    print('\n',txt.print_word_freq) # Word frequency

    # Edit the file
    write_to_file(input[0], writeable_data=[txt.get_letters_freq,txt.get_total_words,txt.get_unique_words, txt.print_word_freq])
    


