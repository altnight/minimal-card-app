<template>
    <md-card>
        <editable-content
                :text="comment.body"
                :marked="true"
                :obj="comment"
                @save="onUpdateCommentBody"
                display="block">
        </editable-content>
    </md-card>
</template>

<style scoped>
</style>

<script type="text/babel">
    import EditableContent from '../../EditableContent.vue'

    export default {
        name: 'comment',
        props: {
            comment: {
                type: Object,
                required: true,
            }
        },
        components: {
            EditableContent,
        },
        methods: {
            onUpdateCommentBody(comment, value) {
                this.$store.commit({
                    type: 'updateChecklistItem',
                    target: comment,
                    params: {body: value}
                })
            }
        }
    }
</script>