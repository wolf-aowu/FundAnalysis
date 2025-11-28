# 放配置文件相关方法
import os

from app.configs import config


def get_config() -> config.Config:
    env_key = config.Config.ENV_KEY
    env = os.getenv(env_key) or "Development"
    config_classname = f"{env}Config"
    config_obj = getattr(config, config_classname, config.DevelopmentConfig)
    return config_obj
