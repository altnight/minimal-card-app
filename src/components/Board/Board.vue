<template>
    <div v-if="getCurrentBoard" style="width: 100%;">
        <router-view></router-view>

        <md-layout v-if="getCurrentBoard">

            <div class="list"
                 v-for="list in lists"
                 :key="list.id"
                 draggable="true"
                 @dragstart="onDragStart(list)"
                 @dragenter="onDragEnter(list)"
                 @dragend="onDragEnd">
                <list :list="list"></list>
            </div>
            <md-card v-if="getCurrentBoard.lists.length < maxListNum" style="width: 20%; height: 114px">
                <editable-content
                        class="box-adding"
                        :text="form.name"
                        :obj="form"
                        :reset="true"
                        @save="onAddList"
                        display="inline"
                        addingText="Add a list ...">
                </editable-content>
            </md-card>
        </md-layout>

    </div>
</template>

<style>
    .list {
        flex-overflow: nowrap;
        width: 20%;
    }
    .box-adding {
        margin: 16px;
    }
</style>

<script type="text/babel">
    import {mapGetters} from 'vuex'

    import EditableContent from '../EditableContent.vue'
    import List from './List.vue'
    import CardModal from './CardModal/CardModal.vue'

    export default {
        name: 'board',
        data() {
            return {
                form: {
                    name: ''
                },
                maxListNum: 5
            }
        },
        computed: {
            ...mapGetters([
                'sequence',
                'getCurrentBoard', 'getCurrentCard',
                'getDraggingList', 'getDraggingCard']),
            lists() {
                return this.getCurrentBoard.lists.sort((a, b) => {
                    return a.index - b.index
                })
            }
        },
        created() {
            this.switchBoard()
        },
        components: {
            EditableContent,
            List, CardModal,
        },
        methods: {
            switchBoard() {
                if (!this.getCurrentBoard) {
                    this.$store.commit('setCurrentBoard', this.$store.getters.findBoardById)
                }
            },
            onDragStart(list) {
                if (this.getDraggingCard) return
                this.$store.commit('setDraggingList', list)
            },
            onDragEnter(list) {
                if (this.getDraggingCard) return
                this._swapIndex(list)
            },
            _swapIndex(list) {
                let tmpIndex = list.index
                list.index = this.getDraggingList.index
                this.getDraggingList.index = tmpIndex
            },
            onDragEnd() {
                this.$store.commit('setDraggingList', null)
            },
            onAddList(obj, value) {
                this.$store.commit('incrementSequence', 'list')
                this.getCurrentBoard.lists.push({
                    id: this.sequence.list,
                    index: this.getCurrentBoard.lists.length,
                    name: value,
                    cards: [],
                })
                this.form.body = ''
            },
        },
        watch: {
            $route(to, from) {
                this.switchBoard()
            }
        },
    }
</script>