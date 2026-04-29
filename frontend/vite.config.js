import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/students": "http://127.0.0.1:8000",
      "/risk": "http://127.0.0.1:8000",
      "/promotion": "http://127.0.0.1:8000",
      "/enrollments": "http://127.0.0.1:8000",
      "/quarters": "http://127.0.0.1:8000",
      "/quarter-weights": "http://127.0.0.1:8000",
      "/academic-records": "http://127.0.0.1:8000",
      "/academic-record-signatures": "http://127.0.0.1:8000",
      "/exports": "http://127.0.0.1:8000",
    },
  },
});