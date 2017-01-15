<template>
    <div v-if="getCurrentCard" class="card-modal-outer">
        <md-card class="card-modal">

            <md-card-header>
                <div class="container">
                    <div class="container-row">
                        <editable-content
                                :text="String(getCurrentCard.name)"
                                :obj="getCurrentCard"
                                @save="onUpdateCardName"
                                display="inline">
                        </editable-content>
                    </div>
                    <div class="container-row-right">
                        <router-link :to="{name: 'board', params: {board_id: getCurrentBoard.id}}"
                                     @click="$store.commit('setCurrentCard')">
                            <md-button class="md-icon-button">
                                <md-icon>clear</md-icon>
                            </md-button>
                        </router-link>
                    </div>
                </div>
            </md-card-header>

            <div style="display: flex">

                <div class="main">
                    <md-card-content>
                        <span>description</span>
                        <div class="card-description">
                            <editable-content :text="getCurrentCard.description"
                                              :marked=true
                                              :obj="getCurrentCard"
                                              @save="onUpdateCardDescription"
                                              display="block">
                            </editable-content>
                        </div>

                        <div v-if="checklists"
                             v-for="checklist in checklists"
                             :key="checklist.id"
                             draggable="true"
                             @dragstart.self="onDragStart(checklist)"
                             @dragend="onDragEnd"
                             @dragenter="onDragEnter(checklist)">

                            <checklist :checklist="checklist"></checklist>
                        </div>

                        <div @keyup.enter.ctrl="saveComment">
                            <md-input-container>
                                <label>comment</label>
                                <md-textarea v-model="commentForm.body"
                                             placeholder="ctrl enter to add comment"
                                ></md-textarea>
                            </md-input-container>
                        </div>

                        <comment v-for="comment in comments"
                                 :key="comment.id"
                                 :comment="comment">
                        </comment>
                    </md-card-content>
                </div>

                <div class="side">
                    <md-card>
                        <md-input-container>
                            <label>checklist name</label>
                            <md-input v-model="checklistForm.name" @keyup.enter="addBoard"></md-input>
                        </md-input-container>
                        <md-button @click.prevent="addChecklist">Add checklist</md-button>
                    </md-card>
                </div>
            </div>

        </md-card>
    </div>
</template>

<style scoped>
    .container {
        display: flex;
    }
    .container-row {
        width: 100%;
        margin: 16px 0;
    }
    .container-row-right {
        margin: 0 0 0 auto;
    }

    .main {
        width: 75%;
    }
    .side {
        width: 25%;
        padding: 0 8px 0 0px;
        margin: 38px 0 16px 0;
    }

    .card-modal {
        display: flex;
        width: 70%;
        height: 70%;
        overflow-y: auto;
        left: 15%;
        top: 15%;
        border: 1px solid black;
        position: fixed;
        z-index: 10;
    }
    .card-modal-outer {
        width: 100%;
        height: 100%;
        position: fixed;
        z-index: 50;
        background-color: #010101;
    }
    .card-modal > a > span {
        color: black;
        font-size: 20px
    }
    .card-description {
        box-shadow: 0 1px 5px rgba(0,0,0,.2),
                    0 2px 2px rgba(0,0,0,.14),
                    0 3px 1px -2px rgba(0,0,0,.12);
    }

</style>

<script type="text/babel">
    import {mapGetters} from 'vuex'

    import Comment from './Comment.vue'
    import Checklist from './Checklist.vue'
    import EditableContent from '../../EditableContent.vue'

    export default {
        name: 'card-modal',
        data() {
            return {
                commentForm: {
                    body: '',
                },
                checklistForm: {
                    name: '',
                }
            }
        },
        components: {
            EditableContent,
            Checklist, Comment,
        },
        computed: {
            ...mapGetters([
                'sequence',
                'getCurrentBoard', 'getCurrentCard', 'getDraggingChecklist']),
            comments() {
                return this.getCurrentCard.comments.sort((a, b) => {
                    return a.id < b.id
                })
            },
            checklists() {
                return this.getCurrentCard.checklists.sort((a, b) => {
                    return a.index - b.index
                })
            }
        },
        created() {
            this.switchCard()
        },
        methods: {
            onDragStart(checklist) {
                if (this.getDraggingChecklistItem || this.getDraggingChecklist) return

                this.$store.commit('setDraggingChecklist', checklist)
            },
            onDragEnter(checklist) {
                if (this.getDraggingChecklistItem || !this.getDraggingChecklist) return

                let tmpIndex = checklist.index
                checklist.index = this.getDraggingChecklist.index
                this.$store.commit('updateDraggingChecklistIndex', tmpIndex)
            },
            onDragEnd() {
                this.$store.commit('setDraggingChecklist', null)
            },

            switchCard() {
                const card = this.$store.getters.findCardByCurrentBoard
                this.$store.commit('setCurrentCard', card)
            },
            saveComment() {
                console.log('aa')
                if (!this.commentForm.body) return
                console.log('a')

                this.$store.commit('incrementSequence', 'comment')
                this.getCurrentCard.comments.push({
                    id: this.sequence.comment,
                    body: this.commentForm.body,
                })
                this.commentForm.body = ''
            },
            onUpdateCardName(card, value) {
                this.$store.commit({
                    type: 'updateCard',
                    target: card,
                    params: {name: value}
                })
            },
            onUpdateCardDescription(card, value) {
                this.$store.commit({
                    type: 'updateCard',
                    target: card,
                    params: {description: value}
                })
            },
            addChecklist() {
                if (!this.checklistForm.name) return

                this.$store.commit('incrementSequence', 'checklist')
                this.getCurrentCard.checklists.push({
                    id: this.sequence.comment,
                    index: this.getCurrentCard.checklists.length,
                    name: this.checklistForm.name,
                    checklist_items: [],
                })
                this.checklistForm.name = ''
            },
        },
        watch: {
            $route(to, from) {
                this.switchCard()
            }
        }
    }
</script>
