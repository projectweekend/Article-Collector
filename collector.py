import os
import newspaper
from newspaper import news_pool


SOURCE_URL = os.getenv('SOURCE_URL', None)
assert SOURCE_URL
TARGET_WORDS = os.getenv('TARGET_WORDS', None)
assert TARGET_WORDS
THREADS = os.getenv('THREADS', '2')


def main():
    target_words_set = set([i.strip() for i in TARGET_WORDS.split(',')])
    num_of_threads = int(THREADS)

    paper = newspaper.build(SOURCE_URL)
    news_pool.set([paper], threads_per_source=num_of_threads)
    news_pool.join()

    for a in paper.articles:
        a.parse()
        a.nlp()
        if set(a.keywords) < target_words_set:
            print(a.title)
            # TODO: hand article to queue for processing


if __name__ == '__main__':
    main()
