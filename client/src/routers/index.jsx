import App from "App";
import ErrorPage from "components/login/ErrorPage";
import RegistPage from "components/login/RegistPage";
import { createBrowserRouter } from "react-router-dom";

const router = createBrowserRouter([
    {
        path: "/",
        element: <App />,
        errorElement: <ErrorPage />,
    },
    {
        path: "/regist",
        element: <RegistPage />,
        errorElement: <ErrorPage />,
    },
]);
export default router;
