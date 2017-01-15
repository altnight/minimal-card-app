<template>
    <router-link :to="{name: 'card', params: {card_id: card.id}}">
        <md-card>
            <md-card-header>
                {{ card.name }}
            </md-card-header>
        </md-card>
    </router-link>
</template>

<style>
</style>

<script type="text/babel">
    export default {
        name: 'card',
        props: {
            card: {
                type: Object,
                required: true,
            }
        },
    }
</script>