import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { regist } from "services/login";
import "common.css";
import "index.css";

function RegistPage() {
    // jsx 只能返回一个父元素，所以不可以同时返回 <p></p><p></p>
    return (
        <>
            {/* 背景图片 */}
            <div className="background-container"></div>
            <RegistBox />
        </>
    );
}

function RegistBox() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    async function handleSubmit(event) {
        event.preventDefault();

        await regist({ username, password })
            .then((response) => {
                if (response.success) {
                    navigate("/");
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
            <h2 className="login-title">注册</h2>
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
                    注册
                </button>
            </form>
            <div className="forget-and-regist">
                <a href="#" className="forget-link">
                    忘记用户名或密码
                </a>
                <Link to="/" className="regist-link">
                    登录
                </Link>
            </div>
        </div>
    );
}

export default RegistPage;
