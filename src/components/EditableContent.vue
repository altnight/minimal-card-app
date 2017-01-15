<template>
    <div v-if="editing">
        <input class="input-inline"
               v-if="display == 'inline'"
               v-model="form.editingText"
               @keyup.enter.prevent="save"
               @blur="cancel">
        <textarea v-else-if="display == 'block'"
                  class="input-block"
                  v-model="form.editingText"
                  @keyup.ctrl.enter.prevent="save"
                  @blur="cancel">
        </textarea>
    </div>
    <div v-else
         @click="edit">
        <div v-if="marked && display == 'block'"
             v-html="markedText"
             class="block-marked">
        </div>
        <div v-else
             v-text="displayText_"
             class="block-text">
        </div>
    </div>
</template>

<style>
    .input-inline {
        width: 100%;
        height: 100%;
        font-size: 14px;
    }
    .input-block {
        width: 100%;
        height: 100%;
        padding: 0 8px;
        margin: 14px 0;
        font-size: 14px;
    }
    .block-marked {
        padding: 0 8px;
        min-height: 16px;
    }
    .block-text {
        padding: 0 8px;
        min-height: 16px;
    }
</style>

<script type="text/babel">
    import MarkdownIt from 'markdown-it'

    const md = new MarkdownIt()

    export default {
        name: 'editable-content',
        props: {
            text: {
                type: String,
                required: true,
            },
            marked: {
                type: Boolean,
                required: false,
                default: false,
            },
            display: {
                type: String,
                required: false,
                default: 'block',
                validator: (value) => {
                    return ['block', 'inline'].includes(value)
                }
            },
            obj: {
                type: Object,
                required: false,
            },
            reset: {
                type: Boolean,
                default: false,
            },
            addingText: {
                type: String,
                default: 'Add XXX ...',
            }
        },
        data() {
            return {
                editing: false,
                displayText: '',
                form: {
                    editingText: '',
                },
            }
        },
        computed: {
            markedText() {
                return md.render(this.displayText)
            },
            displayText_() {
                if (!this.displayText) {
                    return this.addingText
                }
                return this.displayText
            }
        },
        created() {
            this.displayText = this.text
            this.form.editingText = this.text
        },
        methods: {
            edit() {
                if (!this.form.editingText) {
                    this.form.editingText = this.displayText
                }
                this.editing = true
            },
            save() {
                if (!this.form.editingText) {
                    return
                }
                this.$emit('save', this.obj, this.form.editingText)
                if (this.reset) {
                    this.displayText = ''
                    this.form.editingText = ''
                } else {
                    this.displayText = this.form.editingText
                }
                this.editing = false
            },
            cancel() {
                this.editing = false
            },
        },
    }
</script>