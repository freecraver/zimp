import re
import zimp.pos.nltkmodules as nm
nm.init()  # load packages

from spacy.lang.de import German
from spacy.lang.en import English

from abc import abstractmethod, ABC

from nltk import TweetTokenizer
from nltk.tokenize import word_tokenize
from nltk.tokenize.nist import NISTTokenizer

from textblob import TextBlob
from gensim.utils import tokenize

class Tokenizer(ABC):

    @abstractmethod
    def tokenize_text(self, text: str) -> list[str]:
        pass


class RegexTokenizer(Tokenizer):
    def __init__(self, pattern=r"(?u)\b\w\w*\b"):
        """
        :param pattern: regex pattern for splitting tokens
        """
        self._f_regex = re.compile(pattern)

    def tokenize_text(self, text: str) -> list[str]:
        return self._f_regex.findall(text)


class PythonTokenizer(Tokenizer):
    def tokenize_text(self, text: str) -> list[str]:
        return text.split()


class NltkTokenizer(Tokenizer):
    def __init__(self, lang='english') -> None:
        super().__init__()
        self.lang = lang

    def tokenize_text(self, text: str) -> list[str]:
        return word_tokenize(text, self.lang)


class NltkTweetTokenizer(Tokenizer):
    def __init__(self) -> None:
        super().__init__()
        self._base_tokenizer = TweetTokenizer()

    def tokenize_text(self, text: str) -> list[str]:
        return self._base_tokenizer.tokenize(text)


class NltkNistTokenizer(Tokenizer):
    def __init__(self) -> None:
        super().__init__()
        self._base_tokenizer = NISTTokenizer()

    def tokenize_text(self, text: str) -> list[str]:
        return self._base_tokenizer.tokenize(text)


class SpacyTokenizer(Tokenizer):
    def __init__(self, lang='english') -> None:
        super().__init__()
        if lang == 'english':
            self._base_model = English()
        elif lang == 'german':
            self._base_model = German()
        else:
            raise AttributeError(f'Language {lang} not supported')

    def tokenize_text(self, text: str) -> list[str]:
        return [token.text for token in self._base_model(text)]


class TextBlobTokenizer(Tokenizer):
    def tokenize_text(self, text: str) -> list[str]:
        return TextBlob(text).words


class GensimTokenizer(Tokenizer):
    def tokenize_text(self, text: str) -> list[str]:
        return list(tokenize(text))