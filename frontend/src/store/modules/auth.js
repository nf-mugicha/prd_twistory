/**
 * ログイン済みユーザーを管理するストア
 */
import firestore from '../../plugins/firebase'
import firebase from 'firebase'

// DBを呼び出す
const TwitterUsersInfo = firestore.collection('TwitterUsersInfo')
const currentUserInfo = firestore.collection('currentUserInfo')

const state = {
  user: null
}

const getters = {
  // ログインチェック
  check: state => !!state.user,
  // ログインユーザー
  user: state => state.user ? state.user : null
}

const mutations = {
  setUser (state, user) {
    console.log('setUser')
    console.log(user)
    state.user = user
    // console.log(state.user)
  }
}

const actions = {
  async login (context) {
    console.log('user login now')
    // twitterログイン
    const provider = new firebase.auth.TwitterAuthProvider()
    await firebase.auth().signInWithPopup(provider)
      .then((userCredential) => {
        // ユーザー情報を取り出す
        const userInfo = userCredential.additionalUserInfo.profile
        // firestoreに送る
        TwitterUsersInfo.doc(userInfo.id_str).get()
          .then(function (docs) {
            console.log(docs)
            // 新規ユーザーだったらDBに登録
            if (docs.exists) {
              console.log('user exist')
              console.log(userInfo)
            } else {
              console.log('regist user')
              TwitterUsersInfo.doc(userInfo.id_str).set({
                userInfo,
                'timestamp': firebase.firestore.FieldValue.serverTimestamp()
              }, { merge: true })
                .then(doc => {
                  // ミューテーションの外でステート管理しない
                })
            }
            // currentUserテーブルに登録
            firebase.auth().onAuthStateChanged(function (user) {
              if (user) {
                console.log(user)
                // console.log(this.userInfo)
                console.log(userInfo)
                // firestoreに送る
                console.log('regist current users table')
                if (!userInfo.profile_banner_url) {
                  userInfo.profile_banner_url = null
                }
                const payload = {
                  'displayName': user.displayName,
                  'photoURL': user.photoURL,
                  'backgroundPhoto': userInfo.profile_banner_url,
                  'uid': user.uid,
                  'screenName': userInfo.screen_name,
                  'description': userInfo.description,
                  'id_str': userInfo.id_str,
                  'twitterURL': 'https://twitter.com/' + userInfo.screen_name,
                  'timestamp': firebase.firestore.FieldValue.serverTimestamp()
                }
                currentUserInfo.doc(user.uid).set(payload, { merge: true })
                // context.commit('setUser', payload)
                //   .then(doc => {
                //     // ミューテーションの外でステート管理しない
                //   })
              } else {
                context.commit('setUser', null)
              }
            })
          })
      })
      .catch((error) => {
        console.log(error)
      })
  },
  async logout (context) {
    console.log('logout')
    await firebase.auth().signOut()
    context.commit('setUser', null)
  },
  currentUser (context, user) {
    console.log('currentUser')
    console.log(user)
    // ログインしていたら、認証情報からDBを引く
    if (!user) {
      context.commit('setUser', null)
    } else {
      console.log(user.uid)
      const currentUser = currentUserInfo.doc(user.uid)
      console.log(currentUser)
      console.log(typeof currentUser)
      console.log(currentUser.get())
      currentUser.get().then(function (doc) {
        console.log(doc.data())
        // ステート更新
        context.commit('setUser', doc.data())
      })
    }
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
}
