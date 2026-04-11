import './assets/css/basic.css'//ye css poori app me apply karo 


import { createApp } from 'vue'//ye vue ka engine import kr rha hai..aur bhai ye main.js hi entry point hota hai appm ka 
import App from './App.vue'//ye app.vue ko import kr rha hai..ye app.vue hi root component hota hai appm ka 
import router from './router'

const app = createApp(App)//

app.use(router)

app.mount('#app')
