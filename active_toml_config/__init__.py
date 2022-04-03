import logging
import os
from collections import namedtuple

import pytoml as toml

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

inclusive_matrix = {
    "dev": ["dev"],
    "test": ["dev", "test"],
    "acc": ["dev", "test", "acc"],
    "prod": ["dev", "test", "acc", "prod"],
}


def get_config_from_toml_file(file_path: str) -> dict:
    """
    Parses a toml file and returns a dictionary of the parsed config.
    :param file_path:
    :return:
    """
    try:
        with open(file_path, "rb") as toml_file:
            return toml.load(toml_file)
    except FileNotFoundError:
        logging.error(f"Config toml: {file_path} not found.")


def parse_environment_vars_into_app_config(config: dict) -> dict:
    """
    Parses the current set environment variables into the app config provided,
    based on the active "ENV" variable.
    :param config: app config as dict loaded from toml file
    :return: dict of the active environment config.
    """
    current_env = os.getenv("ENV", "dev")

    if not current_env:
        raise ValueError("No ENV name has been set in your toml config file.")
    for env_name, env_dict in config.items():
        for key, val in env_dict.items():
            if isinstance(val, str):
                if val == "":
                    config[env_name][key] = None
                else:
                    config[env_name][key] = parse_env_to_string(val)

    new_config = config[inclusive_matrix[current_env][0]]

    for env_name, envs_to_update in inclusive_matrix.items():
        for env_to_update in envs_to_update:
            if env_to_update in inclusive_matrix[current_env]:
                new_config.update(config[env_to_update])

    return new_config


def parse_env_to_string(config_str: str) -> str:
    """
    Parses a string that contains environment variable templates and
    returns a string with the environment variables replaced.
    :param config_str: string from a config value to be parsed
    :return: string with environment variables replaced
    """
    start = config_str.find("${")
    end = config_str.find("}")
    if start != -1 and end != -1:
        env_to_replace = config_str[start + 2: end].split(":")
        if len(env_to_replace) == 1:
            config_str = config_str.replace(
                f"${{{env_to_replace[0]}}}", os.getenv(env_to_replace[0], "")
            )
        else:
            config_str = config_str.replace(
                f"${{{env_to_replace[0]}:{env_to_replace[1]}}}",
                os.getenv(env_to_replace[0], env_to_replace[1]),
            )

        return parse_env_to_string(config_str)
    else:
        return config_str


def convert_to_named_tuple(config) -> namedtuple:
    """
    Converts a dictionary to a named tuple.
    :param config:
    :return: namedtuple
    """
    Env = namedtuple("env", config.keys())
    return Env(**config)


def get_active_toml_config(file_path: str) -> namedtuple:
    """
    Gets the active toml config from the file path provided.
    :param file_path:
    :return: namedtuple
    """
    config = get_config_from_toml_file(file_path)
    if config:
        config = parse_environment_vars_into_app_config(config)
        return convert_to_named_tuple(config)

    log.warning("No config found.")


env = get_active_toml_config(
    os.getenv("ACTIVE_TOML_CONFIG_PATH", "./config.toml")
)
