import { createApp } from "vue"
import App from "./App.vue"
import router from "./router/index.js"
import "@fontsource/vt323"
import "./assets/minecraft.css"

const app = createApp(App)

app.use(router)

app.mount("#app")
