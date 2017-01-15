<template>
    <md-card>

        <div class="container">
            <div class="container-main">
                <editable-content
                        :text="checklist.name"
                        :obj="checklist"
                        @save="onUpdateChecklistName"
                        display="inline">
                </editable-content>
            </div>
            <div>
                <md-button v-if="not_done_only" @click="not_done_only = false">show all items</md-button>
                <md-button v-else href="#" @click="not_done_only = true">hide done items</md-button>
            </div>
        </div>

        <md-card-content>
            <div v-show="checklist_items.length"
                 v-for="checklist_item in checklist_items"
                 :key="checklist_item.id"
                 draggable="true"
                 @dragenter="onDragEnter(checklist_item)"
                 @dragstart="onDragStart(checklist_item)"
                 @dragend="onDragEnd">
                <md-checkbox v-model="checklist_item.is_done"
                             :id="String(checklist_item.id)"
                             :name="String(checklist_item.id)">
                    <editable-content
                            :text="checklist_item.body"
                            :obj="checklist_item"
                            @save="onUpdateChecklistItemBody"
                            display="inline"
                            addingText="Add a checklist ...">
                    </editable-content>
                </md-checkbox>
            </div>
            <div @dragenter="onDragEnter_checklist_item(checklist)"
                 @dragend="onDragEnd">
                <editable-content
                        :text="form.body"
                        :obj="form"
                        :reset="true"
                        @save="onAddChecklistItem"
                        display="inline"
                        addingText="Add an item ...">
                </editable-content>
            </div>
        </md-card-content>

    </md-card>
</template>

<style>
    .container {
        display: flex;
    }
    .container-main {
        width: 75%;
        margin: 16px 0 0 16px;
    }

</style>

<script type="text/babel">
    import {mapGetters} from 'vuex'

    import EditableContent from '../../EditableContent.vue'

    export default {
        name: 'checklist',
        props: {
            checklist: {
                type: Object,
                required: true,
            }
        },
        data () {
            return {
                not_done_only: false,
                form: {
                    body: '',
                },
            }
        },
        computed: {
            checklist_items() {
                let checklist_items = this.checklist.checklist_items
                if (this.not_done_only) {
                    checklist_items = checklist_items.filter(v => !v.is_done)
                }
                return checklist_items.sort((a, b) => {
                    return a.index - b.index
                })
            },
            ...mapGetters([
                'sequence',
                'getCurrentCard',
                'getDraggingChecklist',
                'getDraggingChecklistItem'])
        },
        methods: {
            onDragStart(checklist_item) {
                if (this.getDraggingChecklist || this.getDraggingChecklistItem) return

                this.$store.commit('setDraggingChecklistItem', checklist_item)
            },
            onDragEnter(checklist_item) {
                if (this.getDraggingChecklist || !this.getDraggingChecklistItem) return

                let currentChecklist = this.findChecklistByChecklistItemId(this.getDraggingChecklistItem.id)
                let targetChecklist = this.findChecklistByChecklistItemId(checklist_item.id)
                const isSameChecklist = currentChecklist == targetChecklist
                if (isSameChecklist) {
                    this.swapIndex(checklist_item)
                } else {
                    targetChecklist.checklist_items.push(this.getDraggingChecklistItem)
                    currentChecklist.checklist_items.splice(this.getDraggingChecklistItem.index, 1)
                    this.$store.commit('regenerateChecklistItemIndex', targetChecklist)
                    this.$store.commit('regenerateChecklistItemIndex', currentChecklist)
                }
            },
            onDragEnter_checklist_item(targetChecklist) {
                let currentChecklist = this.findChecklistByChecklistItemId(this.getDraggingChecklistItem.id)
                targetChecklist.checklist_items.push(this.getDraggingChecklistItem)
                currentChecklist.checklist_items.splice(this.getDraggingChecklistItem.index, 1)
                this.$store.commit('regenerateChecklistItemIndex', targetChecklist)
                this.$store.commit('regenerateChecklistItemIndex', currentChecklist)
            },
            onDragEnd() {
                this.$store.commit('setDraggingChecklistItem', null)
            },
            swapIndex(checklist) {
                let tmpIndex = checklist.index
                checklist.index = this.getDraggingChecklistItem.index
                this.$store.commit('updateDraggingChecklistItemIndex', tmpIndex)
            },
            findChecklistByChecklistItemId(checklistItemId) {
                let checklist_items = []
                this.getCurrentCard.checklists.forEach(checklist => {
                    checklist.checklist_items.forEach(checklist_item => {
                        checklist_items.push({
                            checklist: checklist,
                            checklist_item: checklist_item,
                        })
                    })
                })
                const ob = checklist_items.find(ob => {
                    if (ob.checklist_item.id == checklistItemId) return ob
                })
                return ob.checklist
            },
            onUpdateChecklistName(checklist, value) {
                this.$store.commit({
                    type: 'updateChecklist',
                    target: checklist,
                    params: {name: value}
                })
            },
            onUpdateChecklistItemBody(checklist_item, value) {
                this.$store.commit({
                    type: 'updateChecklistItem',
                    target: checklist_item,
                    params: {body: value}
                })
            },
            onAddChecklistItem(obj, value) {
                this.$store.commit('incrementSequence', 'checklistItem')
                this.checklist.checklist_items.push({
                    id: this.sequence.checklist_item,
                    index: 1000,
                    body: value,
                    is_done: false,
                })
                this.$store.commit('regenerateChecklistItemIndex', this.checklist)
                this.form.body = ''
            },
        },
        components: {
            EditableContent
        },
    }
</script>