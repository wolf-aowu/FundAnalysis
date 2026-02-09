import { Outlet } from "react-router-dom";
import styles from "./App.module.css";

function App() {
    return (
        <div id={styles.backgroundBox}>
            {/* 背景图片 */}
            <div className={styles.backgroundContainer}></div>
            <Outlet />
        </div>
    );
}

export default App;
