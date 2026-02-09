import { post } from "@/services/Request.js";

export async function login(params) {
    return await post("/login", params);
}

export async function regist(params) {
    return await post("/regist", params);
}
