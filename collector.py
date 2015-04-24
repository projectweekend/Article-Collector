import yaml
import newspaper
from rabbit.publisher import Publisher


def main():
    with open('/options/config.yml') as file:
        config = yaml.safe_load(file)
    paper = newspaper.build(config['source'])
    publisher = Publisher(
        rabbit_url=config['rabbit_url'],
        publish_interval=1,
        article_urls=paper.articles)
    publisher.run()


if __name__ == '__main__':
    main()
