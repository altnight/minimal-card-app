import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import data from '../data'

Vue.use(Vuex)


const mutations = {
    setCurrentBoard(state, board) {
        state.current.board = board
    },
    setCurrentCard(state, card) {
        state.current.card = card
    },
    setDraggingCard(state, card) {
        state.dragging.card = card
    },
    setDraggingList(state, list) {
        state.dragging.list = list
    },
    setDraggingChecklist(state, checklist) {
        state.dragging.checklist = checklist
    },
    setDraggingChecklistItem(state, checklist_item) {
        state.dragging.checklistItem = checklist_item
    },

    updateList(state, payload) {
        if (!!payload.params.index) payload.target.index = payload.params.index
        if (!!payload.params.name) payload.target.name = payload.params.name
    },
    updateCard(state, payload) {
        if (!!payload.params.name) payload.target.name = payload.params.name
        if (!!payload.params.description) payload.target.description = payload.params.description
    },
    updateComment(state, payload) {
        if (!!payload.params.body) payload.target.body = payload.params.body
    },
    updateChecklist(state, payload) {
        if (!!payload.params.name) payload.target.name = payload.params.name
    },
    updateChecklistItem(state, payload) {
        if (!!payload.params.body) payload.target.body = payload.params.body
    },

    updateDraggingCardIndex(state, index) {
        state.dragging.card.index = index
    },
    updateDraggingChecklistIndex(state, index) {
        state.dragging.checklist.index = index
    },
    updateDraggingChecklistItemIndex(state, index) {
        state.dragging.checklistItem.index = index
    },

    regenerateCardIndex(state, list) {
        list.cards.forEach((card, i) => {
            card.index = i
        })
    },
    regenerateChecklistItemIndex(state, checklist) {
        checklist.checklist_items.forEach((checklist_item, i) => {
            checklist_item.index = i
        })
    },

    incrementSequence(state, type) {
        switch (type) {
            case 'board':
                state.seq.board++
                break;
            case 'list':
                state.seq.list++
                break;
            case 'card':
                state.seq.card++
                break;
            case 'comment':
                state.seq.comment++
                break;
            case 'checklist':
                state.seq.checklist++
                break;
            case 'checklistItem':
                state.seq.checklist_item++
                break;
            default:
                break;
        }
    },
}

const getters = {
    findBoardById: (state, getters) => {
        return getters.getBoards.find((board) => {
            if (board.id == state.route.params.board_id) return true
        })
    },
    findCardByCurrentBoard: (state, getters) => {
        let cards = []
        getters.getCurrentBoard.lists.forEach(list => {
            list.cards.forEach(card => cards.push(card))
        })
        return cards.find(_card => {
            if (_card.id == state.route.params.card_id) {
                return _card
            }
        })
    },

    getCurrentBoard: (state) => {
        return state.current.board
    },
    getCurrentCard: (state) => {
        return state.current.card
    },

    getBoards: (state) => {
        return state.boards
    },
    sequence: (state) => {
        return state.seq
    },

    getDraggingList: (state) => {
        return state.dragging.list
    },
    getDraggingCard: (state) => {
        return state.dragging.card
    },
    getDraggingChecklist: (state) => {
        return state.dragging.checklist
    },
    getDraggingChecklistItem: (state) => {
        return state.dragging.checklistItem
    },
}

export default new Vuex.Store({
    state: {
        user: {
            id: 1,
            name: 'some'
        },
        current: {
            board: null,
            card: null,
        },
        dragging: {
            list: null,
            card: null,
            checklist: null,
            checklistItem: null,
        },
        boards: data.results,
        seq: data.seq,
    },
    mutations,
    actions: {},
    getters,
    plugins: [createPersistedState({
        paths: ['user', 'boards', 'seq']
    })],
    // strict: true,
})
