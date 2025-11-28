# 基金分析

## 介绍

功能：

1. 计算基金每日涨跌幅
2. 管理买入卖出份数

## 使用的库

### 前端

``` shell
"umi-request": "^1.4.0",
"react-router-dom": "^7.9.6",
```

### 后端

```shell
fastapi           0.121.2
fastapi-cli       0.0.16
fastapi-cloud-cli 0.3.1
pydantic          2.12.4
python-multipart  0.0.20
uvicorn           0.38.0
sqlmodel          0.0.27
SQLAlchemy-Utils  0.42.0
click             8.3.0
PyMySQL           1.1.2
alembic           1.17.2
```

## 安装

### 前端

1. 安装 node.js（网上自行搜索安装教程）

    ```shell
    # 验证安装成功，有版本号
    npm -v
    ```

2. 在项目目录下终端中执行 `npx create-react-app fund-analysis` 命令。创建成功后项目目录中会多出一个 `fund-analysis` 的文件夹，将文件夹下的 `node_modules` 文件夹复制至 `client` 目录下。删除 `fund-analysis`。

3. 进入 client 目录下执行 `npm install` 安装需要的库。

4. 进入 client 目录下执行 `npm run start` 即可运行前端代码。

### 后端

1. 需要安装 python、MySQL（网上自行搜索安装教程）

2. 安装虚拟环境（该步骤可跳过，推荐安装，自行搜索安装教程）

    参考网址：https://github.com/wolf-aowu/StudyNotes/blob/main/Notes-VS%20Code/Python/%E8%99%9A%E6%8B%9F%E7%8E%AF%E5%A2%83/%E8%99%9A%E6%8B%9F%E7%8E%AF%E5%A2%83.md

3. `pip install -r requirements.txt` 安装需要用到的 python 库。

4. 在 `config/config.py` 文件中配上正确的 MySQL 账号密码等。

5. `python before_start.py create-app-database` 创建 `fund_analysis` 数据库

    记下 `db_url` 的输出，后面会用到，本步骤可重复执行。

6. 如果不对代码进行开发可跳过此步骤，使表结构可更新。

    `alembic init migrations` 会生成 `migrations` 目录和 `alembic.ini` 文件

    打开 `alembic.ini` 文件找到 `sqlalchemy.url = driver://user:pass@localhost/dbname` 等号后面替换为 `db_url` 的值，例 `mysql+pymysql://root:1234@localhost:3306/fund_analysis`，注意单引号不需要。

    打开 `migrations/env.py` 文件，添加

    ```python
    import pkgutil
    import importlib
    # 添加项目的根目录作为模块导入，这样项目的绝对路径就能生效
    import os
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    
    from app.models.base import Base
    import app.models
    
    # 本项目中数据库的所有模型类都会放在 app/models 文件夹下（暂定），导入所有数据库模型类
    # 想要能够动态更新表结构就必须把需要更新表结构的所有模型类都导入，只有导入的模型类才会与数据库表比对后更新
    for loader, module_name, ispkg in pkgutil.iter_modules(app.models.__path__):
        if not ispkg and module_name != "base":
            print(f"{module_name=}")
            full_module_name = f'app.models.{module_name}'
            module = importlib.import_module(full_module_name)
    ```

    将 `target_metadata = None` 改为 `target_metadata = Base.metadata`

    如果使用异步数据库，需要添加以下行，代码里有找到位置，加上注释的那几行（我用的是同步没试过，网上抄的）。

    ```python
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata,
            # # 如果你使用异步数据库，需要添加以下行
            # transaction_per_migration=True,  # 确保每个迁移都在一个事务中
            # compare_type=True,  # 启用类型比较，以便自动检测类型变更
        )
    ```

    执行 `alembic revision --autogenerate -m "create initial tables"` 其中 `-m` 参数后面的内容可自定义，是给本次更新记的 `message` （注释）。执行完会在 `migrations/versions` 文件夹下生成 `version_id_create_initial_tables.py` 迁移脚本，并在数据库中创建 `alembic_version` 表。如果有问题 `migrations/versions` 下的文件和数据库中的 `alembic_version` 表都是可以删除的。

    执行 `alembic upgrade head` 会执行迁移脚本创建表。

SQLAlchemy 基础参考网址：

https://www.bilibili.com/video/BV1RB4y1P7jz/?p=54&share_source=copy_web&vd_source=19ded2cbbeabb5205eb9a82e27ee28db

动态更新表结构（数据库迁移技术）参考网址：
https://blog.csdn.net/weixin_50882748/article/details/149811042?fromshare=blogdetail&sharetype=blogdetail&sharerId=149811042&sharerefer=PC&sharesource=lang_wolf&sharefrom=from_link
https://www.cnblogs.com/jackadam/p/8684633.html

python 导入规则参考网址：https://www.bilibili.com/video/BV1K24y1k7XA/?share_source=copy_web&vd_source=19ded2cbbeabb5205eb9a82e27ee28db

alembic 常用命令

```shell
# 生成迁移脚本
alembic revision --autogenerate -m "message"
# 更新数据库，如果这一步报错，需要删除迁移文件
alembic upgrade head
# 查看迁移历史
alembic history
# 回退到上一个版本
alembic downgrade -1
# 数据库回退到初始状态
alembic downgrade base
```

## 项目技术

### 双端通信

前后端都需要配置一下

#### 前端

参考网址：https://github.com/umijs/umi-request/blob/master/README_zh-CN.md（创建实例）

在 `utils/request.js` 中重新封装 `request`。

``` javascript
import { extend } from "umi-request";

export const request = extend({
    prefix: "http://localhost:8000",
});
```

#### 后端

使用 CORS（跨域资源共享）技术

参考网址：https://fastapi.tiangolo.com/zh/tutorial/cors/

``` python
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 代理（绕过同源策略）

不需要配置上面提到的前后端，只需按下面配置就能实现双端通信。

这个方法用于开发环境，如果想用于生产环境就需要配置反向代理等（需要自己网上查）。

**单一后端**

前端在根目录下的 package.json 文件中添加（配置代理）：

`"http://localhost:8000"` 是后端的 url

``` json
"proxy": "http://localhost:8000"
```

**多个后端（没试过）**

在 src 目录下创建 setupProxy.js 文件

``` javascript
const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/api',
    createProxyMiddleware({
      target: 'http://localhost:8000',
      changeOrigin: true,
      pathRewrite: {
        '^/api': '/api'
      }
    })
  );
  
  app.use(
    '/v2',
    createProxyMiddleware({
      target: 'http://localhost:8001',
      changeOrigin: true,
    })
  );
}
```

### 登陆页面背景图

登陆页面背景图采用 Picsum Photos `green`、`nature` 主题随机生成。这是个 MIT 许可证的资源项目 😘😍。

`https://picsum.photos/1920/1080?green,nature`

`1920` 和 `1080` 代表图片大小 `1920 * 1080`。

用法教学网址：https://picsum.photos/

GitHub：https://github.com/DMarby/picsum-photos

## 支持我

![](https://raw.githubusercontent.com/wolf-aowu/FundAnalysis/refs/heads/main/%E5%9B%BE%E7%89%87/%E6%94%B6%E6%AC%BE%E7%A0%81.png)

![](https://raw.githubusercontent.com/wolf-aowu/FundAnalysis/refs/heads/main/%E5%9B%BE%E7%89%87/%E6%94%AF%E6%8C%81%E4%B8%80%E4%B8%8B.png)

![](https://raw.githubusercontent.com/wolf-aowu/FundAnalysis/refs/heads/main/%E5%9B%BE%E7%89%87/%E4%B8%80%E6%9D%AF%E5%A5%B6%E8%8C%B6.png)

![](https://raw.githubusercontent.com/wolf-aowu/FundAnalysis/refs/heads/main/%E5%9B%BE%E7%89%87/%E6%9C%89%E7%94%A8%E8%B5%8F.png)

## 功能（写给我自己看的，非要看我不拦你 😑）

![](图片\模型设置.png)

### 注册

#### 前端

1. 账号名重复需要有提示
2. 注册后直接进入个人主页
3. 密码确认
4. 密码可见

#### 后端

1. 账号名，不能重复
2. 密码

#### 待做

1. 密码强度
2. 绑定手机号

### 登录

#### 前端

1. 跳转注册
2. 登录后进入个人主页

#### 后端

1. 检测账号名是否存在
2. 检测密码与账号名是否匹配
3. 账号名不存在或密码与账号名不匹配提示“账号名或密码有误！”

### 个人主页

#### 前端

1. 显示账号名
2. 修改密码按钮
3. 导航栏：基金管理、当日基金

#### 后端

#### 待做

1. 绑定手机号

### 基金管理

#### 前端

1. 添加基金，可以只添加基金
2. 添加买入卖出记录，时间、份数、买入 or 卖出
3. 选择持仓基金或全部，展示买入卖出记录，默认剔除被过滤的数据，可以选择展示全部

#### 后端

1. 添加的基金是否存在，不存在提示“基金不存在”
2. 添加买入卖出记录，基金净值
3. 更新买入卖出记录确定哪些是已完成买入和卖出的可以被过滤（份数一致、累加份数一致，设定差为 3%以上）
4. 需要有张表是关于基金的记录

#### 待做

1. 可以看百分比的图（照着支付宝的来）开始时间为 0.00% 精确到 2 位小数
2. 百分比图支持 近 1 个月、近 3 个月、买入以来、近 6 个月、今年、近 3 年、近 5 年、成立。

### 当日基金

#### 前端

1. 区分持仓基金和自选基金，前一日净值、当日涨跌幅、前 10 股票持仓百分比
2. 可以添加自选基金
3. 每行基金后面有个按钮“查看可卖”，跳转至可买基金页面

#### 后端

1. 有个自选基金表格
1. 查一次爬一次当天基金涨跌幅
1. 计算基金当天涨跌幅

#### 待做

1. 每行基金后面有个“查看详情”按钮，跳转后可以看到基金的前 10 重仓的股票的涨跌幅和持仓百分比，有一个更新按钮可以刷新
1. 基金可能存在代码和名称改变的情况需要考虑一下这种情况怎么处理，暂定当前如果遇到自己改数据库的基金代码

### 可买基金

#### 前端

1. 有一个输入涨跌幅百分比的地方，意味着列出大于这个百分比的买入
2. 有一个可以勾选被过滤的勾选框

#### 后端
