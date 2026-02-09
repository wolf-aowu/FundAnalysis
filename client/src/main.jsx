import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { RouterProvider } from "react-router-dom";

import router from "@/routers/index";
import "./common.css";

createRoot(document.getElementById("root")).render(
    // StrictMode 可以发现过时 API、异步边界，但是会影响性能
    // 在应用跟组件中包裹 StrictMode，不需要额外配置，开发环境自动启用检查，生产环境自动禁用
    // 开发环境下 StrictMode 会导致组件渲染两次，如 constructor、useEffect 双调用等
    // <StrictMode>
    <RouterProvider router={router} />,
    // {/* </StrictMode>, */}
);
