# Weather app project

> Weather application for collect information from different weather sites and display the received data in a convenient format. 

This is a console application (Python interpreter) that accepts certain commands and parameters and outputs the result in a format that is convenient to us. 

## weatherapp.core 
> Application core where the main functional is implemented.

## weatherapp.accu 

> AccuWeather provider for getting data from AccuWeather site.

## weatherapp.rp5

> Rp5 provider for getting data from rp5.ua site. 

Adding a new provider does not change the implementation of the main functionality, but only connects the new module as a plugin.

### Install packages with the ability to edit packages after installation: 

```bash
pip install --editable weatherapp.core
```

```bash
pip install --editable weatherapp.accu
```

```bash
pip install --editable weatherapp.rp5
```

### Commands weather application:

Get the weather data from all providers:

```bash
wfapp
```

Get the weather data from a specific provider:

```bash
wfapp [provider id]
```

Get a list of all providers:

```bash
wfapp providers
```

Choice location for getting weather information from a specific provider:

```bash
wfapp configurate [provider id]
```

Update cache for all providers:

```bash
wfapp --refresh
```

Update cache for specific provider:

```bash
wfapp [provider id] --refresh
```

Optional argument for show traceback on errors:
`--debug`

Optional argument for logging messages starting from INFO level:
`-v`

Optional argument for logging messages starting from DEBUG level:
`-vv`

Optional argument for output format (default to table):
`-f` or `-- formatter`