<template>
    <md-layout md-flex="100">

        <md-card v-for="board in getBoards" :key="board.id">
            <md-card-header>
                <router-link @click="$store.commit('setCurrentBoard', board)"
                             :to="{name: 'board', params: {board_id: board.id}}">
                    <div class="md-title">{{ board.name }}</div>
                </router-link>
            </md-card-header>
        </md-card>

        <md-card>
            <md-card-header>
                <div class="md-title">Add Board</div>
            </md-card-header>
            <md-card-content>
                <md-input-container>
                    <md-input v-model="form.name" @keyup.enter="addBoard"></md-input>
                </md-input-container>
            </md-card-content>
            <md-card-actions>
                <md-button @click.prevent="addBoard">Add</md-button>
            </md-card-actions>
        </md-card>

    </md-layout>
</template>

<style scoped>
    .md-card {
        width: 33%;
    }
</style>

<script type="text/babel">
    import {mapGetters} from 'vuex'

    export default {
        name: 'top',
        computed: {
            ...mapGetters(['getBoards', 'sequence'])
        },
        data() {
            return {
                form: {
                    name: '',
                }
            }
        },
        methods: {
            addBoard() {
                if (!this.form.name) return

                this.$store.commit('incrementSequence', 'board')
                this.getBoards.push({
                    id: this.sequence.board,
                    index: this.getBoards.length,
                    name: this.form.name,
                    lists: [],
                })
                this.form.name = ''
            },
        },
    }
</script>