<template>
    <md-layout>
        <md-card class="list-container">
            <md-card-header>
                <div>
                    <editable-content
                            :text="list.name"
                            :obj="list"
                            @save="onUpdateListName"
                            display="inline">
                    </editable-content>
                </div>
            </md-card-header>
            <md-card-content>
                <div v-show="cards.length"
                     v-for="card in cards"
                     :key="card.id"
                     draggable="true"
                     @dragstart="onDragStart(card)"
                     @dragenter="onDragEnter(card)"
                     @dragend="onDragEnd">
                    <card :card="card"></card>
                </div>
                <div @dragenter="onDragEnter_list(list)"
                     @dragend="onDragEnd">
                    <editable-content
                            class="box-adding"
                            :text="form.name"
                            :obj="form"
                            :reset="true"
                            @save="onAddCard"
                            display="inline"
                            addingText="Add a card ...">
                    </editable-content>
                </div>
            </md-card-content>
        </md-card>
    </md-layout>
</template>

<style>
    .list-container {
        width: 100%;
    }
    .box-adding {
        margin-top: 16px;
        margin-bottom: 0;
    }
</style>

<script type="text/babel">
    import {mapGetters} from 'vuex'

    import EditableContent from '../EditableContent.vue'
    import Card from './Card.vue'

    export default {
        name: 'list',
        props: {
            list: {
                type: Object,
                required: true,
            }
        },
        data() {
            return {
                form: {
                    name: ''
                }
            }
        },
        components: {
            EditableContent,
            Card
        },
        computed: {
            cards() {
                return this.list.cards.sort((a, b) => {
                    return a.index - b.index
                })
            },
            ...mapGetters([
                'sequence',
                'getCurrentBoard', 'getDraggingCard', 'getDraggingList'])
        },
        methods: {
            onDragStart(card) {
                if (this.getDraggingList) return

                this.$store.commit('setDraggingCard', card)
            },
            onDragEnter_list(targetList) {
                let currentList = this.findListByCardId(this.getDraggingCard.id)
                targetList.cards.push(this.getDraggingCard)
                currentList.cards.splice(this.getDraggingCard.index, 1)
                this.$store.commit('regenerateCardIndex', targetList)
                this.$store.commit('regenerateCardIndex', currentList)
            },
            onDragEnter(card) {
                if (this.getDraggingList) return

                let currentList = this.findListByCardId(this.getDraggingCard.id)
                let targetList = this.findListByCardId(card.id)
                const isSameList = currentList == targetList
                if (isSameList) {
                    this.swapIndex(card)
                } else {
                    targetList.cards.push(this.getDraggingCard)
                    currentList.cards.splice(this.getDraggingCard.index, 1)
                    this.$store.commit('regenerateCardIndex', targetList)
                    this.$store.commit('regenerateCardIndex', currentList)
                }
            },
            swapIndex(card) {
                let tmpIndex = card.index
                card.index = this.getDraggingCard.index
                this.$store.commit('updateDraggingCardIndex', tmpIndex)
            },
            onDragEnd() {
                this.$store.commit('setDraggingCard', null)
            },
            findListByCardId(cardId) {
                let cards = []
                this.getCurrentBoard.lists.forEach(list => {
                    list.cards.forEach(card => {
                        cards.push({
                            card: card,
                            list: list
                        })
                    })
                })
                const ob = cards.find(ob => {
                    if (ob.card.id == cardId) return ob.list
                })
                return ob.list
            },
            onUpdateListName(list, value) {
                this.$store.commit({
                    type: 'updateList',
                    target: list,
                    params: {name: value},
                })
            },
            onAddCard(obj, value) {
                this.$store.commit('incrementSequence', 'card')
                this.list.cards.push({
                    id: this.sequence.card,
                    index: 1000,
                    name: value,
                    description: '',
                    comments: [],
                    checklists: [],
                })
                this.$store.commit('regenerateCardIndex', this.list)
                this.form.body = ''
            },
        },
    }
</script>