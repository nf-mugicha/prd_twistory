/**
 * ログイン済みユーザーを管理するストア
 */
import firestore from '../../plugins/firebase'

// DBを呼び出す
const currentUserInfo = firestore.collection('currentUserInfo')

const state = {
  user: null
}

const getters = {
  // ログインユーザー
  userProfile: state => state.user ? state.user : null
}

const mutations = {
  setUser (state, user) {
    console.log('setUser')
    console.log(user)
    state.user = user
  }
}

const actions = {
  userData (context, screenName) {
    console.log(screenName)
    console.log(currentUserInfo.where('screenName', '==', screenName).get())
    currentUserInfo.where('screenName', '==', screenName.screen_name).get().then((querySnapshot) => {
      querySnapshot.forEach((doc) => {
        console.log(doc.id)
        console.log(doc.data())
        context.commit('setUser', doc.data())
      })
    })
    // return this.doc.data()
      .catch(function (error) {
        console.log('Error getting documents: ', error)
      })
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
}
