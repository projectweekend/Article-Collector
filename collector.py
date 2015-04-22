import yaml
import newspaper
from newspaper import news_pool


def get_config():
    with open('/options/config.yml') as file:
        config = yaml.safe_load(file)
    keys = config.keys()
    if not 'threads' in keys:
        config['threads'] = 2
    if not 'source' in keys:
        raise Exception('"source" not defined in config.yml')
    if not 'words' in keys:
        raise Exception('"words" not defined in config.yml')
    return config


def main():
    config = get_config()
    target_words_set = set([i.lower() for i in config['words']])
    paper = newspaper.build(config['source'])
    news_pool.set([paper], threads_per_source=config['threads'])
    news_pool.join()

    for a in paper.articles:
        a.parse()
        a.nlp()
        if target_words_set < set(a.keywords):
            print(a.title)
            print(a.keywords)
            # TODO: hand article to queue for processing


if __name__ == '__main__':
    main()
