# active-toml-config
A small library for parsing active environment variables into TOML config.

it can provide you with namedtuples, which are a way to represent a toml config
structure in a more convenient way when using it in your apps. 

It can also be used to parse environment variables at import time,
which is useful for configuring your app at startup and provides a
 

## Installation

To install this library, you can use any pip compatible package manager:

In your terminal, run:

```bash
pip install active-toml-config
```

## Setup
In the application you are going use this library, you need to create 
a `config.toml` file in the root directory of your project.

Alternatively you can provide an alternative path to the config.toml 
file by setting the `ACTIVE_TOML_CONFIG_PATH` environment variable
when running your application.

A typical config.toml file might look like this:

```toml
[dev]
port = "8080"
host = "localhost"
mysql_host = "localhost"
mysql_port = "3306"
mysql_user = "root"
mysql_password = "root"
mysql_database = "my_database"
enable_logging = "${ACTIVE_ENV_LOGGING:false}"

[test]
mysql_database = "my_test_database"

[acc]
mysql_host = "https://exampledbhost.com"
mysql_user = "app_user"
mysql_password = "${MYSQL_PASSWORD}"
mysql_database = "acc_database"

[prod]
mysql_host = "https://exampledbhost-prod.com"
mysql_user = "app_user_prod"
mysql_database = "prod_database"
```

The library currently looks for the following headings in the toml file:
```dev,test,acc and prod```
and will use the config values based on `ENV` environment variable.
only the dev environment will be used if `ENV` is not set and is 
also required to be in the config.toml file. All other environments
are optional.

In that exact order, environment based config sections 
will be merged downwards in the order chain 
when building the config object.

## Usage

The library allows you to simply import the `active_toml_config` module and
use the `env` global to access the parsed configuration.

At first import, the library will parse the config file and build a config.
the resulting config is a named tuple containing all the fields in the config file.

```python
from active_toml_config import env

def main():
    print(env.my_var)
```