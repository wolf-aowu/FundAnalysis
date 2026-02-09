const baseURL = "http://localhost:8000";
const developmentBaseURL = "http://localhost:8000";
const testingBaseURL = "http://localhost:8000";
const productionBaseURL = "http://localhost:8000";

// process.env 是 Next.js 中用的
// import.meta.env.MODE 获取运行环境
// vite 项目中自定义环境变量必须以 VITE_ 开头
export const ENV_MODE = import.meta.env.MODE;
// import.meta.env.DEV 等同于 import.meta.env.MODE == "development"
// import.meta.env.PROD 等同于 import.meta.env.MODE == "production"
export const BASE_URL = import.meta.env.DEV
    ? developmentBaseURL
    : ENV_MODE === "testing"
      ? testingBaseURL
      : import.meta.env.PROD
        ? productionBaseURL
        : baseURL;

export const TIMEOUT = 5000;
