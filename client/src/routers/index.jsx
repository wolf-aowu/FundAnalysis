import App from "@/pages/App";
import { createBrowserRouter, Navigate } from "react-router-dom";
import Login from "@/pages/Login";
import Regist from "@/pages/Regist";
import Error from "@/pages/Error";

const router = createBrowserRouter([
    {
        path: "/",
        element: <App />,
        errorElement: <Error />,
        children: [
            // 访问 / 时自动重定向到 /login
            {
                index: true,
                element: <Navigate to="/login" replace />,
            },
            {
                path: "login",
                element: <Login />,
                errorElement: <Error />,
            },
            {
                path: "regist",
                element: <Regist />,
                errorElement: <Error />,
            },
        ],
    },

    // {
    //     path: "/home",
    //     element: <HomePage />,
    //     errorElement: <ErrorPage />,
    // },
]);
export default router;
