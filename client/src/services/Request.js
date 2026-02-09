import axios from "axios";

import { BASE_URL, TIMEOUT } from "@/config/ServiceConfig";

// axios 参考网址：https://www.axios-http.cn/docs/intro

// 这样以后万一 axios 不能用了只需要改这个文件就可以了
// create 创建实例的作用：项目有多个服务器地址时，可以创建多个实例，分别配置不同的 baseURL
// 如果有多个服务器可以只配置一个实例，使用 nginx，都发个 nginx，由 nginx 转发到不同的服务器

const clientInstance = axios.create({
    baseURL: BASE_URL,
    timeout: TIMEOUT,
});

// 可以通过 axios.interceptors.request.use 或 axios.interceptors.response.use
// 添加拦截器的作用：
// 1. 请求拦截器可以在请求发送之前对请求进行处理，
// 比如添加 token、修改请求头、param/data 序列化等操作。
// 2. 发送网络请求时，可以显示加载动画，等请求完成后再关闭加载动画。
// 3. 响应拦截器可以在响应数据返回之前对响应数据进行处理，比如统一处理错误码、格式化数据等操作。

clientInstance.interceptors.request.use(
    (request) => {
        // 请求时请求头都添加 token
        const token = sessionStorage.getItem("token");
        if (token) {
            request.headers.Authorization = `Bearer %{token}`;
        }
        return request;
    },
    (error) => {
        return Promise.reject(error);
    },
);

clientInstance.interceptors.response.use(
    (response) => {
        // 对响应数据进行处理
        return response.data;
    },
    (error) => {
        // 对响应错误进行处理
        console.error("请求错误:", error);
        switch (error.response?.status) {
            case 400:
                console.error("请求错误(400)：请求参数错误");
                break;
            case 401:
                console.error("未授权(401)：请重新登录");
                break;
            case 403:
                console.error("禁止访问(403)：拒绝访问");
                break;
            case 404:
                console.error("未找到(404)：请求资源未找到");
                break;
            case 500:
                console.error("服务器错误(500)：请稍后重试");
                break;
            default:
                console.error(`连接错误(${error.response?.status})！`);
        }
        return Promise.reject(error);
    },
);

export async function get(url, params) {
    try {
        const data = await clientInstance.get(url, params);
        return data;
    } catch (error) {
        console.error("请求错误:", error);
    }
}

export async function post(url, params) {
    try {
        const data = await clientInstance.post(url, params);
        return data;
    } catch (error) {
        console.error("请求错误:", error);
    }
}

export async function put(url, params) {
    try {
        const data = await clientInstance.put(url, params);
        return data;
    } catch (error) {
        console.error("请求错误:", error);
    }
}

export async function del(url) {
    try {
        const data = await clientInstance.delete(url);
        return data;
    } catch (error) {
        console.error("请求错误:", error);
    }
}
