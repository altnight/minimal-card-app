import Vue from 'vue'
import App from './App.vue'

import store from './store'

import router from './router'
import { sync } from 'vuex-router-sync'

sync(store, router)


import VueMaterial from 'vue-material'
Vue.use(VueMaterial)

new Vue({
    el: '#app',
    render: h => h(App),
    store,
    router,
})
