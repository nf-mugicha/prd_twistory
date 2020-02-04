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
    setUser(state, user) {
        state.user = user
    }
}

const actions = {
    async login(context) {
        // twitterログイン
        const provider = new firebase.auth.TwitterAuthProvider()
        await firebase.auth().signInWithRedirect(provider)
        firebase.auth().getRedirectResult()
            .then((userCredential) => {
                // ユーザー情報を取り出す
                const userInfo = userCredential.additionalUserInfo.profile
                const userToken = userCredential.credential.accessToken
                const userSecretToken = userCredential.credential.secret
                    // firestoreに送る
                TwitterUsersInfo.doc(userInfo.id_str).get()
                    .then(function(docs) {
                        // 新規ユーザーだったらDBに登録
                        if (docs.exists) {} else {
                            TwitterUsersInfo.doc(userInfo.id_str).set({
                                    userInfo,
                                    'userAccessToken': userToken,
                                    'userSecretToken': userSecretToken,
                                    'timestamp': firebase.firestore.FieldValue.serverTimestamp()
                                }, { merge: true })
                                .then(doc => {
                                    // ミューテーションの外でステート管理しない
                                })
                        }
                        // currentUserテーブルに登録
                        firebase.auth().onAuthStateChanged(function(user) {
                            if (user) {
                                // firestoreに送る
                                if (!userInfo.profile_banner_url) {
                                    userInfo.profile_banner_url = null
                                }
                                const payload = {
                                    'accessToken': userToken,
                                    'secretToken': userSecretToken,
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
    async logout(context) {
        await firebase.auth().signOut()
        context.commit('setUser', null)
    },
    currentUser(context, user) {
        // ログインしていたら、認証情報からDBを引く
        if (!user) {
            context.commit('setUser', null)
        } else {
            const currentUser = currentUserInfo.doc(user.uid)
            currentUser.get().then(function(doc) {
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