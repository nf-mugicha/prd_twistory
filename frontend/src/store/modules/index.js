import Vue from 'vue'
import Vuex from 'vuex'

import auth from '../auth'
import CONSTANTS from '../../components/constants'
import { ADD, REMOVE, UPDATE_MILLION, UPDATE_PLATFORMS } from './mutation-types'

Vue.use(Vuex)

const store = new Vuex.Store({
  // ストアで管理するデータを定義する
  state: {
    // リンク詳細リスト（後々DBに書く）
    links: [
      { id: 1, user_id: 'adam', link_title: 'onelink_title1', description: 'this is description1', million: false, createAt: new Date(), link_photo: 'https://picsum.photos/id/108/50/50' },
      { id: 2, user_id: 'ben', link_title: 'onelink_title2', description: 'this is description2', million: false, createAt: new Date(), link_photo: 'https://picsum.photos/id/200/50/50' },
      { id: 3, user_id: 'chimmy', link_title: 'onelink_title3', description: 'this is description3', million: false, createAt: new Date(), link_photo: 'https://picsum.photos/id/300/50/50' },
      { id: 5, user_id: 'chimmy', link_title: 'onelink_title3', description: 'this is description3', million: false, createAt: new Date(), link_photo: 'https://picsum.photos/id/300/50/50' },
      { id: 4, user_id: 'leo', link_title: 'onelink_title4', description: 'this is description4', million: false, createAt: new Date(), link_photo: 'https://picsum.photos/id/400/50/50' }
    ],
    nextId: 5

  },
  // stateに定義したデータを参照するメソッドを定義する
  getters: {
    // 全件を返す
    links (state) {
      return state.links
    },
    // idで指定した１件を返す
    byId (state) {
      return function (_id) {
        var link = state.links.find(
          link => link.id === _id
        )
        if (link) {
          return link
        }
        console.log('link not found')
        console.log(link)
        return CONSTANTS.ERROR_MEMO
      }
    }

  },
  // stateに定義したデータを更新するメソッドを定義
  // 第一引数にstateオブジェクト、第二引数に更新するデータを受け取るpayloadオブジェクトを記載
  mutations: {
    // リンクを一件追加
    [ADD] (state, payload) {
      payload.id = state.nextId
      state.links.push(payload)
      state.nextId++
    },
    // idで指定したリンクを削除
    [REMOVE] (state, payload) {
      var index = state.links.findIndex(link => link.id === payload.id)
      // もしインデックスが存在すればidを1つ消す
      if (index !== -1) {
        state.links.splice(index, 1)
      }
    },
    // idで指定したリンクのミリオンを反転させる
    [UPDATE_MILLION] (state, payload) {
      var index = state.links.findIndex(link => link.id === payload.id)
      if (index !== -1) {
        state.links[index].million = !state.links[index].million
      }
    },
    // idで指定したリンクのプラットフォーム配列を操作する。同じ要素があれば削除、なければ追加
    [UPDATE_PLATFORMS] (state, payload) {
      var index = state.links.findIndex(link => link.id === payload.id)
      if (index !== -1) {
        var platforms = state.links[index].platforms
        if (platforms.includes(payload.platform)) {
          platforms.splice(platforms.indexOf(payload.platform), 1)
        } else {
          platforms.push(payload.platform)
        }
      }
    }
  },
  actions: {
    addLink ({ commit }, payload) {
      commit(ADD, payload)
    },
    deleteLink ({ commit }, payload) {
      commit(REMOVE, payload)
    },
    updateMillion ({ commit }, payload) {
      commit(UPDATE_MILLION, payload)
    },
    updatePlatforms ({ commit }, payload) {
      commit(UPDATE_PLATFORMS, payload)
    }

  },
  modules: {
    auth
  }
})

export default store
