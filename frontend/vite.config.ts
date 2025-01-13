import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import autoprefixer from 'autoprefixer'
import tailwind from 'tailwindcss'
import { fileURLToPath, URL } from 'node:url'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => ({
    base:
        mode == "development"
            ? "http://localhost:5173/"
            : "/static/api/spa/",
    build: {
        emptyOutDir: true,
        outDir: "../api/static/api/spa",
    },
    css: {
        postcss: {
            plugins: [tailwind(), autoprefixer()],
        },
    },
    plugins: [vue()],
    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url))
        },
    },
}));
