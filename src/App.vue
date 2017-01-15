<template>
    <div>
        <md-layout :md-gutter="24">
            <app-header></app-header>
        </md-layout>
        <md-layout :md-gutter="24">
            <router-view></router-view>
        </md-layout>
    </div>
</template>

<style>
</style>

<script type="text/babel">
    import Header from './components/Header.vue'

    export default {
        name: 'app',
        components: {
            'app-header': Header,
        },
        watch: {
            $route(to, from){
                let board = this.$store.getters.findBoardById
                this.$store.commit('setCurrentBoard', board)
            }
        }
    }
</script>
