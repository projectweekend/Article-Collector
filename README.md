Article-Collector takes a source URL for a news site, extracts all the individual article URLs it can find, and sends each one as a message to RabbitMQ for later processing.


## Config

Article-Collector uses a config file, written in YAML, that contains two properties:
* `source` - the URL for a news site
* `rabbit_url` - the connection URL for a RabbitMQ server

### Example
```yaml
source: http://cnn.com/
rabbit_url: https://user:password@somerabbitserver.com/whatever
```
