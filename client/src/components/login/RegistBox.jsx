import { Link } from "react-router-dom";
import styles from "./RegistBox.module.css";

function RegistBox({
    username,
    password,
    setUsername,
    setPassword,
    handleSubmit,
}) {
    return (
        <div className={styles.registContainer}>
            <h2 className={styles.registTitle}>注册</h2>
            <form className={styles.registForm} onSubmit={handleSubmit}>
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
                <button type="submit" className={styles.registBtn}>
                    注册并登录
                </button>
            </form>
            <div className={styles.forgetAndLogin}>
                <a href="#" className={styles.forgetLink}>
                    忘记用户名或密码
                </a>
                <Link to={"/login"} className={styles.loginLink}>
                    登录账号
                </Link>
            </div>
        </div>
    );
}

export default RegistBox;
