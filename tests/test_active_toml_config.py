import os
from imp import reload


project_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
test_config_file = os.path.join(project_root_dir, "tests/resources/test_config.toml")


def get_and_reload_env_tuple():
    import active_toml_config as atc
    reload(atc)
    return atc.env


def test_dev_config_load_with_default_replacement():
    """
    Test that the environment variable is imported
    """
    os.environ["ACTIVE_TOML_CONFIG_PATH"] = test_config_file
    env = get_and_reload_env_tuple()
    assert env.test_var == "test_value"
    assert env.test_var_replace == "default_value"


def test_dev_config_load_with_environment_replacement():
    """
    Test that the environment variable is imported
    """
    expected_value = "test_replace_value"
    os.environ["ACTIVE_TOML_CONFIG_PATH"] = test_config_file
    os.environ["REPLACE_VAR"] = expected_value
    env = get_and_reload_env_tuple()
    assert env.test_var_replace == expected_value


def test_test_config_with_dev_included():
    expected_dev_value = "test_value"
    expected_additional_value = "additional_value"
    os.environ["ENV"] = "test"
    os.environ["ACTIVE_TOML_CONFIG_PATH"] = test_config_file
    env = get_and_reload_env_tuple()
    assert env.test_var == expected_dev_value
    assert env.additional_var == expected_additional_value


def test_acc_config_with_overwriting_value():
    expected_acc_value = "test_value_overwritten"
    os.environ["ENV"] = "acc"
    os.environ["ACTIVE_TOML_CONFIG_PATH"] = test_config_file
    env = get_and_reload_env_tuple()
    assert env.test_var == expected_acc_value


def test_prod_config_with_overwriting_values():
    expected_prod_value = "test_value_overwritten_by_prod"
    expected_additional_value = "additional_value_overwritten_by_prod"
    os.environ["ENV"] = "prod"
    os.environ["ACTIVE_TOML_CONFIG_PATH"] = test_config_file
    env = get_and_reload_env_tuple()
    assert env.test_var == expected_prod_value
    assert env.additional_var == expected_additional_value
