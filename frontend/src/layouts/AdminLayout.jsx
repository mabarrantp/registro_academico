import { Outlet } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import "./AdminLayout.css";

export default function AdminLayout() {
    return (
        <div className="hca-layout">
            <Sidebar />

            <section className="hca-main">
                <Header title="Panel Administrativo" />

                <div className="hca-content">
                    <Outlet />
                </div>
            </section>
        </div>
    );
}