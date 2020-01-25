<template>
<div class="login__auth">
  <v-btn
    class="light-blue darken-1 white--text text-center"
    :disabled="processing"
    :loading="processing"
    :block=true
    v-if="isLogin" @click="signOut">
    Sign-Out
  </v-btn>
  <v-btn
    class="light-blue darken-1 white--text text-center"
    :disabled="processing"
    :loading="processing"
    :block=true
    v-else @click="signIn">Twitter Login
  </v-btn>
  </div>
</template>

<script>
// firebase構成をインポートする
import firebase from 'firebase'
import Navbar from './Navbar'

export default {
  name: 'Login',
  components: {
    'Navbar': Navbar
  },
  data: function () {
    return {
      processing: false,
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
      if (this.processing) return
      try {
        this.processing = true
        this.$store.dispatch('auth/login')
        setTimeout(() => {
          this.processing = false
        }, 10000)
        // this.processing = false
      } catch (e) {
        this.processing = false
      }
    },
    signOut: function () {
      this.$store.dispatch('auth/logout')
      this.$router.push('/')
    }
  }
}
</script>
