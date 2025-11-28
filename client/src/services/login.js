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
