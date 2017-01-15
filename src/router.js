import Vue from 'vue'
import VueRouter from 'vue-router'

import Top from './components/Top/Top.vue'
import Board from './components/Board/Board.vue'
import CardModal from './components/Board/CardModal/CardModal.vue'

Vue.use(VueRouter)

export default new VueRouter({
    mode: 'history',
    base: '/minimal-card-app/',
    routes: [
        {path: '/', name: 'top', component: Top},
        {path: '/b/:board_id', name: 'board', component: Board, children: [
            {path: 'c/:card_id', name: 'card', component: CardModal}]
        }
    ]
})
