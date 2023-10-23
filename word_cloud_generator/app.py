import os
from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

def main():
    
    # gets the working directory of your project
    file_path = os.path.dirname(os.path.abspath(__file__))

    # defines file path for corpus and background mask from working directory
    corpus_path = os.path.join(file_path, 'corpus.txt')
    background_mask = os.path.join(file_path, 'background_mask.png')

    # reads the corpus file as a text_file
    with open(corpus_path, 'r') as text_file:
        text = text_file.read()

    # loads background mask image as a numpy array
    background_mask = np.array(Image.open(background_mask))

    # removes pre-defined stop words from corpus to final word cloud
    stopwords = set(STOPWORDS)
    #stopwords.update(["example_word1", "example_word2", "another_word", "more_stopwords"])

    # defines the word cloud parameters
    word_cloud = WordCloud(background_color="white", max_words=2000, mask=background_mask,
                stopwords=stopwords, contour_width=3, contour_color='steelblue')

    # generate word cloud and save file in the working directory
    word_cloud.generate(text)
    working_directory = os.path.join(file_path, "word_cloud.png")
    word_cloud.to_file(working_directory)

    # displays the generated word cloud image
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis("off")

if __name__ == "__main__":
    main()