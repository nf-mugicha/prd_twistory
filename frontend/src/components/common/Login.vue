<template>
  <div class="login__auth">
    <span dark color="#2196F3" v-if="isLogin" @click="signOut">Sign-Out</span>
    <span dark color="#2196F3" v-else @click="signIn">Twitter Login</span>
  </div>
</template>

<script>
// firebase構成をインポートする
import firebase from 'firebase'
import Navbar from './Navbar'
import LinkList from '.././pages/LinkList'
import { setTimeout } from 'timers'

export default {
  name: 'Login',
  components: {
    Navbar,
    LinkList
  },
  data: function () {
    return {
      user: firebase.auth().currentUser,
      userName: null,
      userPic: null,
      userEmail: null,
      userEmailVerified: null,
      userUid: null,
      isSignedIn: null,
      // ログイン/ ログアウト確認
      isAuth: true
    }
  },
  // computedには結果がキャッシュされる
  computed: {
    isLogin () {
      return this.$store.getters['auth/check']
    },
    userinfo () {
      return this.$store.getters['auth/user']
    }
  },
  mounted: function () {
    firebase.auth().onAuthStateChanged(
      user => {
        this.user = user || {}
        this.isAuth = !!user
        this.userName = user
          ? this.user.displayName : null
        this.userPic = user
          ? this.user.photoURL : null
        this.userEmail = user
          ? this.user.email : null
        this.userEmailVerified = user
          ? this.user.emailVerified : null
        this.userUid = user
          ? this.user.uid : null
      })
  },
  methods: {
    signIn: function () {
      this.$store.dispatch('auth/login')
      setTimeout(() => {
        const userlogin = this.$store.getters['auth/user']
        console.log(userlogin)
        this.$router.push(userlogin.screenName)
      }, 10000)
    },
    signOut: function () {
      this.$store.dispatch('auth/logout')
      this.$router.push('/')
    }
  }
}
</script>
