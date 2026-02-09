import { Link } from "react-router-dom";
import styles from "./LoginBox.module.css";

function LoginBox({
    username,
    password,
    setUsername,
    setPassword,
    handleSubmit,
}) {
    return (
        <div className={styles.loginContainer}>
            <h2 className={styles.loginTitle}>登录</h2>
            <form className={styles.loginForm} onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="用户名"
                    required
                    pattern="[a-zA-Z0-9_]+"
                    title="只能包含字母、数字和下划线"
                    name="username"
                    value={username}
                    autoComplete="off"
                    onChange={(e) => setUsername(e.target.value)}
                />
                <input
                    type="password"
                    placeholder="密码"
                    required
                    pattern="[a-zA-Z0-9_]+"
                    title="只能包含字母、数字和下划线"
                    name="password"
                    value={password}
                    autoComplete="off"
                    onChange={(e) => setPassword(e.target.value)}
                />
                <button type="submit" className={styles.loginBtn}>
                    登录
                </button>
            </form>
            <div className={styles.forgetAndRegist}>
                <a href="#" className={styles.forgetLink}>
                    忘记用户名或密码
                </a>
                <Link to={"/regist"} className={styles.registLink}>
                    注册账号
                </Link>
            </div>
        </div>
    );
}

export default LoginBox;
