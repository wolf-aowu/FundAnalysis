import { extend } from "umi-request";

export const request = extend({
    prefix: "http://localhost:8000",
});
