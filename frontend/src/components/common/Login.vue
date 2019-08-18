<template>
  <div class="login__auth">
    <!-- <template v-if="isAuth && userName && userPic">
      <div class="header__user-image">
        <img :src="userPic" />
      </div>
      <p class="header__user-name">
        {{ userName }}
        {{ user }}
        {{ userinfo }}
      </p>
    </template>-->
    <v-btn dark color="#2196F3" v-if="isAuth" @click="signOut">Sign-Out</v-btn>
    <v-btn dark color="#2196F3" v-else @click="signIn">Twitter Login</v-btn>
  </div>
  <!-- <router-view :isAuth="isAuth" :userName="userName" :userPic="userPic"></router-view> -->
</template>

<script>
// firebase構成をインポートする
import firebase from 'firebase'
import Navbar from './Navbar'

export default {
  name: 'Login',
  components: {
    Navbar
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
      // this.$router.push('/')
    },
    signOut: function () {
      this.$store.dispatch('auth/logout')
      // this.$router.push('/')
    }
  }
}
</script>
