import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { regist } from "@/services/login";
import RegistBox from "@/components/login/RegistBox";

import { message } from "antd";

function Regist() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    const [messageApi, contextHolder] = message.useMessage();

    async function handleSubmit(event) {
        event.preventDefault();

        const response_data = await regist({ username, password });

        if (response_data.success) {
            const data = response_data.data;
            const token = data.token;
            sessionStorage.setItem("token", token);
            messageApi.open({
                type: "success",
                content: "注册成功",
            });
            // navigate("/home");
        } else {
            messageApi.open({
                type: "error",
                content: "注册失败：" + response_data.message,
            });
        }
    }

    // jsx 只能返回一个父元素，所以不可以同时返回 <p></p><p></p>
    return (
        <>
            {contextHolder}
            <RegistBox
                username={username}
                password={password}
                setUsername={setUsername}
                setPassword={setPassword}
                handleSubmit={handleSubmit}
            />
        </>
    );
}

export default Regist;
