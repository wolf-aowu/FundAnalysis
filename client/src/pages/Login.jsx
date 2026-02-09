import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { login } from "@/services/login";
import LoginBox from "@/components/login/LoginBox";

import { message } from "antd";

function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    const [messageApi, contextHolder] = message.useMessage();

    async function handleSubmit(event) {
        event.preventDefault();

        const response_data = await login({ username, password });
        if (response_data.success) {
            const data = response_data.data;
            const token = data.token;
            sessionStorage.setItem("token", token);
            messageApi.open({
                type: "success",
                content: "登录成功",
            });
            // navigate("/home");
        } else {
            messageApi.open({
                type: "error",
                content: "登录失败：" + response_data.message,
            });
        }
    }

    return (
        <>
            {contextHolder}
            <LoginBox
                username={username}
                password={password}
                setUsername={setUsername}
                setPassword={setPassword}
                handleSubmit={handleSubmit}
            />
        </>
    );
}

export default Login;
