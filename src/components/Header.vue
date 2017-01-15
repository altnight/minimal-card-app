<template>
    <md-toolbar style="flex: 1;">
        <router-link :to="{name: 'top'}">
            <md-button class="md-icon-button">
                <md-icon>home</md-icon>
            </md-button>
        </router-link>
        <div @click="clearCache()">
            <md-button class="md-icon-button">
                <md-icon>cached</md-icon>
            </md-button>
        </div>
        <h2 class="md-title">
            <span class="header-link">
                <router-link :to="{name: 'top' }">Minimal-Card-App</router-link>
            </span>
            <span class="header-link"
                  v-if="getCurrentBoard">
                / <router-link :to="{name: 'board', params: {board_id: getCurrentBoard.id }}">{{ getCurrentBoard.name }}</router-link>
            </span>
        </h2>
    </md-toolbar>
</template>

<style>
    .header-link a {
        color: rgba(255, 255, 255, .87) !important;
    }
    .md-button.md-fab .md-icon, .md-button.md-icon-button .md-icon {
        color: rgba(255, 255, 255, .87);
    }
</style>

<script type="text/babel">
    import {mapGetters} from 'vuex'

    export default {
        name: 'v-header',
        computed: {
            ...mapGetters(['getCurrentBoard', 'getCurrentCard'])
        },
        methods: {
            clearCache() {
                localStorage.vuex = null
                alert('cache cleared')
            }
        }
    }
</script>
