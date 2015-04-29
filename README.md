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

## Run with Docker
The Article-Collector is easy to run using [Docker](https://www.docker.com/), first you need to build an image using the provided `Dockerfile`. From inside the project directory:

```
docker build -t give_it_a_name .
```

After the build process completes, you can launch a container to run the process. When launching the container, you will need to mount a volume containing the config file you wish to use:

### Run in Interactive Mode

```
docker run -it -v /path/to/config.yml:/src/config.yml give_it_a_name
```

### Run in Detached Mode

```
docker run -d -v /path/to/config.yml:/src/config.yml give_it_a_name
```
