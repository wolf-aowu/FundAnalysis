# 基金分析

## 介绍

功能：

1. 计算基金每日涨跌幅
2. 管理买入卖出份数

## 使用的库

### 前端

``` shell
react-router-dom@7.12.0
vite@7.3.1
antd@6.1.4
axios@1.13.2
```

所有依赖包：

``` json
├── @eslint/js@9.39.2
├── @types/react-dom@19.2.3
├── @types/react@19.2.8
├── @vitejs/plugin-react@5.1.2
├── antd@6.1.4
├── axios@1.13.2
├── eslint-plugin-react-hooks@7.0.1
├── eslint-plugin-react-refresh@0.4.26
├── eslint@9.39.2
├── globals@16.5.0
├── react-dom@19.2.3
├── react-router-dom@7.12.0
├── react@19.2.3
└── vite@7.3.1
```

### 后端

```shell
fastapi           0.121.2
fastapi-cli       0.0.16
fastapi-cloud-cli 0.3.1
pydantic          2.12.4
python-multipart  0.0.20
uvicorn           0.38.0
SQLAlchemy-Utils  0.42.0
PyMySQL           1.1.2
aiomysql          0.3.2
cryptography      46.0.3
alembic           1.17.2
click             8.3.0
```

## 安装

### 前端

大部分文件都在 client 目录下

1. 安装 node.js（网上自行搜索安装教程）

    ```shell
    # 验证安装成功，有版本号
    npm -v
    ```

2. 使用 vite 创建项目，在项目目录下终端中执行 `npm create vite`, Project name 为 fund-analysis。选择 React -> JavaScript ->（Use rolldown-vite (Experimental)?）No ->（Install with npm and start now?）Yes。将新生成的 fund-analysis 文件夹重命名为 client。将 `client/package.json` 文件中 `scripts` 下 `"dev": "vite"` 改为 `"start": "vite"`，这样启动项目命令依然为 `npm run start`，否则命令为 `npm run dev`。

    eslint 能够帮助开发代码时更规范，bug 提示更精确。vite5 之上安装后自动安装 eslint，无需多余配置。当前为 vite7。

3. 进入 client 目录下执行 `npm install` 安装需要的库。

4. 进入 client 目录下执行 `npm run start` 即可运行前端代码。

### 后端

大部分文件都在 app 目录下

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
    
    from app.models.orm.base import Base
    import app.models.orm
    
    # 本项目中数据库的所有模型类都会放在 app/models/orm 文件夹下（暂定），导入所有数据库模型类
    # 想要能够动态更新表结构就必须把需要更新表结构的所有模型类都导入，只有导入的模型类才会与数据库表比对后更新
    for loader, module_name, ispkg in pkgutil.iter_modules(app.models.orm.__path__):
        if not ispkg and module_name != "base":
            print(f"{module_name=}")
            full_module_name = f'app.models.orm.{module_name}'
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
    
    **如果有一天改变了数据库模型的目录**，也就是 `models/orm` 下的文件改变位置了，需要改变（例如 `models` -> `models/orm`）：
    
    原代码：
    
    ``` python
    import app.models
    from app.models.base import Base
    
    for loader, module_name, ispkg in pkgutil.iter_modules(app.models.__path__):
        if not ispkg and module_name != "base":
            print(f"{module_name=}")
            full_module_name = f'app.models.{module_name}'
            module = importlib.import_module(full_module_name)
    target_metadata = Base.metadata
    ```
    
    改后：
    
    ``` python
    import app.models.orm
    from app.models.orm.base import Base
    
    for loader, module_name, ispkg in pkgutil.iter_modules(app.models.orm.__path__):
        if not ispkg and module_name != "base":
            print(f"{module_name=}")
            full_module_name = f'app.models.orm.{module_name}'
            module = importlib.import_module(full_module_name)
    target_metadata = Base.metadata
    ```
    
    `before_start.py` 文件也需要这样改。

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

这里使用 `axios` 库发送请求，`umi-request` 库请移步至 `历史笔记\umi-request`

``` javascript
import axios from "axios";

const BASE_URL = "http://localhost:8000";
const TIMEOUT = 5000;
const clientInstance = axios.create({
    baseURL: BASE_URL,
    timeout: TIMEOUT,
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

### 密码加密

加盐处理 + SHA3-256 哈希算法

步骤：

1. 生成随机盐值
2. 密码 + 盐值
3. 计算哈希
4. 将盐值和哈希值一起存入数据库中

**为什么不用 PBKDF2 算法（来自 AI 说的）：**

PBKDF2 算法依赖迭代次数，计算效率较慢，输出长度可变。

SHA3-256 算法为理论 $2^{256}$ 复杂度，计算较快，适合大量数据，输出长度固定 256 位。

### 循环 import 问题

``` shell
  File "D:\Git 仓库\FundAnalysis\main.py", line 7, in <module>
    from app.routers.root import root_router
  File "D:\Git 仓库\FundAnalysis\app\routers\root.py", line 2, in <module>
    from app.queries.user import get_user_by_username
  File "D:\Git 仓库\FundAnalysis\app\queries\user.py", line 1, in <module>
    from app.queries.base import get_session
  File "D:\Git 仓库\FundAnalysis\app\queries\base.py", line 1, in <module>
    from main import AsyncSession
  File "D:\Git 仓库\FundAnalysis\main.py", line 7, in <module>
    from app.routers.root import root_router
```

报错原因：

`main.py` 文件需要添加路由，则需要从 `root.py` 文件中导入 `root_touter`。在 `main.py` 文件中创建了数据库会话类 `AsyncSession`。在 `root.py` 文件中因为需要处理请求，所以需要执行一些数据库操作，数据库操作在 `user.py` 文件中，此时需要实例出来一个会话对象，实例会话对象这个功能我规划在了 `base.py` 文件中，要实现这个功能就需要从 `main.py` 文件导入数据库会话类 `AsyncSession`。这就构成了循环导入。

说明：

1. 知道 FastAPI 支持注入依赖，但我觉得那样写有点丑（没试过能不能解决循环导入的问题，GPT 回答可以），理由：
   1. 在写接受请求时还要关心这个方法要不要查询数据库
   2. 我希望数据库操作方法能够写在一个文件中与接收请求响应的方法分开写，这样更便于管理和代码重复利用
   3. 每个请求需要一个 session 入参，数据库操作也需要一个 session 入参，写两遍难受

方案：

我将 `base.py` 文件中导入 `AsyncSession` 放进了 `with_session`（功能等同于报错中的 `get_session`） 方法中，而不是在文件的开头就导入。也就是错开了导入时间。同时为了能够只写一遍实例 `AsyncSeesion` 我使用了装饰器来减少敲的代码量。

queries/base.py

``` python
from functools import wraps

def with_session(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        from main import AsyncSession
        async with AsyncSession() as session:
            return await func(session, *args, **kwargs)
    return wrapper
```

queries/user.py

``` python
from app.queries.base import with_session
@with_session
async def get_user_by_username(session, username: str) -> User:
    result = await session.execute(select(UserORM).where(UserORM.username == username))
    user_orm_obj = result.scalars().first()
    user_obj = to_entity(User, user_orm_obj)
    return user_obj
```

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

## 前端组件库

Taro UI for React - 京东出品，多端合一，所向披靡

https://github.com/jd-opensource/taro-ui

https://taro-ui.jd.com/#/docs/introductionAnt 

Design Mobile of React - 阿里前端 UI 库，面向企业级中后台

https://github.com/ant-design/ant-design-mobile

https://mobile.ant.design/zh/guide/quick-start/

TDesign React Mobile - 腾讯 UI 组件库，配套工具完满，设计工整，文档清晰

https://github.com/Tencent/tdesign-react

https://tdesign.tencent.com/react/overview

NutUI for React - 京东出品，移动端友好，面向电商业务场景

https://github.com/jdf2e/nutui-react

https://nutui.jd.com/h5/react/2x/#/zh-CN/guide/intro-react

Material-UI - 全球顶级 React 组件库 Google Material 设计标准 android 首先

https://mui.com/material-ui/getting-started/installation/

https://github.com/mui/material-ui

React WeUI - 微信出品，面向微信移动端，完整的微信生态 UI 组件库

https://weui.github.io/react-weui/docs/#/react-weui/docs/page/2/articles/0

https://github.com/weui/react-weui

Zarm Design React - 宝藏 React 移动端 UI 组件库

https://zarm.design/#/

https://github.com/ZhongAnTech/zarm

## 历史笔记

### create-react-app

react 中项目创建有很多种，create-react-app 是其中的一种，一般用于快速、小型的项目启动和开发。

在项目根目录执行 `npx create-react-app 项目名称`。会在项目根目录生成一个以项目名称命名的文件夹。 `node_modules` 文件夹、`package.json`、`package-lock.json`、`README.md`、`public\index.html`、`src\index.js`、`src\App.js` 保留，其他文件都可删除。

`public\index.html` 文件中可以把涉及到之前删除的文件的代码都删掉。

`src\index.js` 文件同理，同时把最后一行代码及其导入 `reportWebVitals()` 都删除。`reportWebVitals` 是 Google 推出的用于衡量网页性能的核心指标工具，旨在帮助开发者优化用户体验，会将指标数据上报。

`src\App.js` 文件同理，同时 `App` 方法中的 `return` 的内容也可以删除，在 `return` 中开始写自己的 `react` 代码。

现在 `create-react-app` 已经自带 eslint 了。

#### 设置导入的默认起始目录

将 src 设置为导入的默认起始目录。

创建 `jsconfig.json` 文件，

``` json
{
    "compilerOptions": {
        "baseUrl": "src"
    },
    // 排除编译时要处理的目录
    "exclude": ["node_modules"]
}
```

### vite

不喜欢，下次起项目不用这个了，这次是 umi-request 过时了总是会有警告，一开始以为是 create-react-app 太老了，正好学到 vite 就换了，换完才发现是 umi-request 的锅😑。

优点：

1. css 类名、id名 不用担心不同组件中间名称重复问题

缺点：

1. jsx 文件中 `className=`、`id=` 后面不再是字符串，而是 js，所以不适合用“-”分割单词，需要时使用驼峰命名法
2. 可能需要多加一个 `div`，也就是 `index.html` 中自带的 `id=root` 不能使用了，除非添加全局样式，所以一般需要多加一个 `div` 来处理全屏。
3. 浏览器中的类名为了处理不重复问题会在类名中添加一串随机字符串，很难看

#### 设置导入的默认起始目录别名

将 src 设置为导入的默认起始目录别名。

`vite.config.js` 文件 `defineConfig` 中

``` json
{
    resolve: {
        alias: {
            "@": "/src",
        },
    },
}
```

#### 设置运行端口

`vite.config.js` 文件 `defineConfig` 中

``` js
{
    server: {
        port: 3000,
        host: "127.0.0.1",
    },
}
```

### umi-request

实现请求原本计划使用这个库的，在它的 github 上有与 fetch、axios 的对比很诱人，但是后来发现它已经停止更新了。所以改用 axios 库了。
参考网址：https://github.com/umijs/umi-request/blob/master/README_zh-CN.md（创建实例）

在 `utils/request.js` 中重新封装 `request`。

``` javascript
import { extend } from "umi-request";

export const request = extend({
    prefix: "http://localhost:8000",
});
```

在 `services/login.js` 中使用 `request`

``` javascript
import { request } from "utils/request";

export async function login(params) {
    return request.post("/login", {
        data: params,
    });
}

export async function regist(params) {
    return request.post("/regist", {
        data: params,
    });
}
```

在 `components/login/LoginPage.jsx` 的 `LoginBox` 组件中调用 `login`

``` javascript
function LoginBox() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    async function handleSubmit(event) {
        event.preventDefault();

        await login({ username, password })
            .then((response) => {
                if (response.success) {
                    navigate("/home");
                } else {
                    alert("注册失败：" + response.message);
                }
            })
            .catch((error) => {
                console.error("注册请求失败：", error);
            });
    }

    return (
        <div className="login-container">
            <h2 className="login-title">登录</h2>
            <form className="login-form" onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="用户名"
                    required
                    pattern="[a-zA-Z0-9_]+"
                    title="只能包含字母、数字和下划线"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />
                <input
                    type="password"
                    placeholder="密码"
                    required
                    pattern="[a-zA-Z0-9_]+"
                    title="只能包含字母、数字和下划线"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <button type="submit" className="login-btn">
                    登录
                </button>
            </form>
            <div className="forget-and-regist">
                <a href="#" className="forget-link">
                    忘记用户名或密码
                </a>
                <Link to={"/regist"} className="regist-link">
                    注册账号
                </Link>
            </div>
        </div>
    );
}
```

