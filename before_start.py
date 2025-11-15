import click
import pkgutil
import importlib
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database

from app.utils.config import get_config
from app.utils.database import get_database_url


@click.group()
def cli():
    pass


@cli.command()
def create_app_database():
    config_obj = get_config()
    db_url = get_database_url(config_obj)
    print(f"{db_url=}")
    try:
        exists = database_exists(db_url)
        if exists:
            # 目前 APP 只计划用一个数据库
            print(f"数据库 {config_obj.APP_NAME} 已存在！")
        else:
            print(f"数据库 {config_obj.APP_NAME} 不存在，开始创建数据库！")
            create_database(f"{db_url}")
    except Exception as e:
        print(f"检查或创建数据库时出现错误：{e}")


@cli.command()
def create_all_table():
    config_obj = get_config()
    db_url = get_database_url(config_obj)
    print(f"{db_url=}")
    # 如果觉得控制台打印日志太多，可以设置成 echo=False
    engine = create_engine(f"{db_url}?charset={config_obj.MYSQL_CHARSET}", echo=True)
    with Session(engine) as session:

        # 导入 models 文件夹下所有的 module，不包括 base.py 因为上面导入过了，再导一遍也不会再执行一遍
        from app.models.base import Base
        import app.models
        for loader, module_name, ispkg in pkgutil.iter_modules(app.models.__path__):
            if not ispkg and module_name != "base":
                print(f"{module_name=}")
                full_module_name = f'app.models.{module_name}'
                module = importlib.import_module(full_module_name)

        try:
            Base.metadata.create_all(engine)
        except Exception as e:
            print(f"创建数据库表时出现错误：{e}")
        finally:
            session.close()
            engine.dispose()


if __name__ == "__main__":
    cli()
