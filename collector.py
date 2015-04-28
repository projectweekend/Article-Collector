import sys
import yaml
import newspaper
from rabbit import Publisher


def parse_config():
    try:
        with open('./config.yml') as file:
            config = yaml.safe_load(file)
    except IOError:
        print("No volume mounted with file 'config.yml'")
        sys.exit(1)
    try:
        source_url = config['source']
    except KeyError:
        print("'source' property is missing in 'config.yml'")
        sys.exit(1)
    try:
        rabbit_url = config['rabbit_url']
    except KeyError:
        print("'rabbit_url' property is missing in 'config.yml'")
        sys.exit(1)

    return (source_url, rabbit_url, )


def main():
    source_url, rabbit_url = parse_config()
    paper = newspaper.build(source_url)
    publisher = Publisher(
        rabbit_url=rabbit_url,
        publish_interval=0.25,
        article_urls=paper.article_urls())
    publisher.run()


if __name__ == '__main__':
    main()
