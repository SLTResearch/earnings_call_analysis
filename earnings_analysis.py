import re
from wordcloud import WordCloud, STOPWORDS
import numpy as np
from PIL import Image
from mtbpy import mtbpy
import json
from wordcloud import WordCloud, STOPWORDS
import numpy as np
from PIL import Image
from mtbpy import mtbpy

# Loughran and McDonald Sentiment Word Lists (https://sraf.nd.edu/textual-analysis/resources/)
with open(
    r"Loughran and McDonald Sentiment Word Lists.txt",
    "r",
) as f:
    lmdict = eval(f.read())

# negation check as suggested by Loughran and McDonald
# That is, any occurrence of negate words (e.g., isn’t, not, never) within three words preceding a positive word will flip that positive word into a negative one.
# Negation check only applies to positive words because Loughran and McDonald suggest that double negation (i.e., a negate word precedes a negative word) is not common.
with open(
    r"negate.txt",
    "r",
) as f:
    negate = eval(f.read())


def negated(word):
    """
    Determine if preceding word is a negation word

    """
    if word.lower() in negate:
        return True
    else:
        return False


def tone_count_with_negation_check(dict, article):
    """
    Count positive and negative words with negation check. Account for simple negation only for positive words.
    Simple negation is taken to be observations of one of negate words occurring within three words
    preceding a positive words.
    """
    pos_count = 0
    neg_count = 0

    pos_words = []
    neg_words = []

    input_words = re.findall(
        r"\b([a-zA-Z]+n\'t|[a-zA-Z]+\'s|[a-zA-Z]+)\b", article.lower()
    )

    word_count = len(input_words)

    for i in range(0, word_count):
        if input_words[i] in dict["Negative"]:
            neg_count += 1
            neg_words.append(input_words[i])
        if input_words[i] in dict["Positive"]:
            if i >= 3:
                if (
                    negated(input_words[i - 1])
                    or negated(input_words[i - 2])
                    or negated(input_words[i - 3])
                ):
                    neg_count += 1
                    neg_words.append(input_words[i] + " (with negation)")
                else:
                    pos_count += 1
                    pos_words.append(input_words[i])
            elif i == 2:
                if negated(input_words[i - 1]) or negated(input_words[i - 2]):
                    neg_count += 1
                    neg_words.append(input_words[i] + " (with negation)")
                else:
                    pos_count += 1
                    pos_words.append(input_words[i])
            elif i == 1:
                if negated(input_words[i - 1]):
                    neg_count += 1
                    neg_words.append(input_words[i] + " (with negation)")
                else:
                    pos_count += 1
                    pos_words.append(input_words[i])
            elif i == 0:
                pos_count += 1
                pos_words.append(input_words[i])

    print("The results with negation check:", end="\n")
    print("The # of positive words:", pos_count)
    print("The # of negative words:", neg_count)
    print("The ratio of positive over negative words:", pos_count / neg_count)
    print("The list of found positive words:", pos_words)
    print("The list of found negative words:", neg_words)
    print("\n", end="")

    results = [word_count, pos_count, neg_count, pos_words, neg_words]

    return results


# A sample output
article = open(
    r"Alphabet Inc.txt",
    "r",
    encoding="utf8",
).read()

results = tone_count_with_negation_check(lmdict, article)
print(results)

nWords = 100

# Open and read the mask image into a numpy array.
maskArray = np.array(Image.open(r"cloud.png"))

# Specify the properties of the word cloud.
cloud = WordCloud(
    background_color="white", max_words=nWords, mask=maskArray, stopwords=set(STOPWORDS)
)

# Generate the positive and negative word clouds.
cloud.generate(" ".join(results[3]))
# Save the word cloud to a png file.
cloud.to_file(r"word_cloud_pos.png")

cloud.generate(" ".join(results[4]))
# Save the word cloud to a png file.
cloud.to_file(r"word_cloud_neg.png")
