import firestore from '../../plugins/firebase'
import CONSTANS from '../../components/constants'
/**
 * リンクページで表示するリンク一件分のデータを管理する
 */

// DBを呼び出す
const LinkRef = firestore.collection('LinkList')
// const currentUserInfo = firestore.collection('currentUserInfo')

export default {
  namespaced: true,
  unsubscribe: null,
  state () {
    return {
      // 一件分なので
      data: {}
    }
  },
  mutations: {
    // 受け取ったデータpayloadをステートに格納
    init (state, payload) {
      console.log('init')
      console.log(payload)
      state.data = payload
    },
    // リンク追加時
    add (state, payload) {
      state.data.push(payload)
    },
    // 呼び出すとき
    set (state, payload) {
      const index = state.data.findIndex(link => link.id === payload.id)
      if (index !== -1) {
        state.data[index] = payload
      }
    },
    // 削除時
    remove (state, payload) {
      const index = state.data.findIndex(link => link.id === payload.id)
      if (index !== -1) {
        state.data.splice(index, 1)
      }
    }
  },
  // コンポーネントはゲッターを通して状態監視する
  getters: {
    data (state) {
      console.log(state.data)
      return state.data
    }
  },
  actions: {
    clear ({ commit }) {
      commit('init', CONSTANS.NEW_EMPTY_MEMO())
    },
    // リスナーの起動
    startListener ({ commit }, payload) {
      if (this.unsubscribe) {
        console.warn('listener is already running. ', this.unsubscribe)
        this.unsubscribe()
        this.unsubscribe = null
      }
      // firestoreからデータを検索する
      console.log(payload)
      console.log(payload.id)
      console.log(payload.link_id)
      console.log('link.jsssss')
      this.unsubscribe = LinkRef.where('link_id', '==', payload.link_id).onSnapshot(function (querySnapshot) {
        querySnapshot.forEach(function (doc) {
          console.log('link.js')
          // データが更新されるたびに呼び出される
          commit('init', {
            id: doc.id,
            link_id: doc.data().link_id,
            create_num: doc.data().create_num,
            link_title: doc.data().link_title,
            description: doc.data().description,
            platforms: doc.data().platforms,
            million: doc.data().million,
            createAt: new Date(doc.data().createAt.seconds * 1000),
            photo: doc.data().photo
          })
        })
        // doc => {
        //   console.log('link.js')
        //   console.log(doc.docs.map)
        //   console.log(doc.docs.keys())
        //   console.log(doc.docs.link_id)
        //   // データが更新されるたびに呼び出される
        //   commit('init', {
        //     id: doc.id,
        //     link_id: doc.data().link_id,
        //     create_num: doc.data().create_num,
        //     link_title: doc.data().link_title,
        //     description: doc.data().description,
        //     platforms: doc.data().platforms,
        //     million: doc.data().million,
        //     createAt: new Date(doc.data().createAt.seconds * 1000),
        //     photo: doc.data().photo
        //   })
        // }
      })
    },
    // リスナーの停止
    stopListener () {
      if (this.unsubscribe) {
        console.log('listener is stopping ', this.unsubscribe)
        this.unsubscribe()
        this.unsubscribe = null
      }
    },
    updateMillion ({ state }) {
      const million = !state.data.million
      LinkRef.doc(state.data.id).update({ million: million })
        .then(() => {

        })
        .catch(err => {
          console.err('Error updateing document: ', err)
        })
    },
    updatePlatforms ({ state }, payload) {
      const platforms = [].concat(state.data.platforms)
      if (platforms.includes(payload.platforms)) {
        platforms.splice(platforms.indexOf(payload.platforms), 1)
      } else {
        platforms.push(payload.platform)
      }
      LinkRef.doc(state.data.id).update({ platforms: platforms })
        .then(() => {

        })
        .catch(err => {
          console.error('Error updating document: ', err)
        })
    }
  }
}
