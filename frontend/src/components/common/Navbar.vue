<template>
  <v-card flat tile
  >
    <v-toolbar dense>
      <v-toolbar-title
      class="nav__title"
      >
      <router-link
      to="/"
      class="toolbar-title"
      >
      AItter -ついじぇね-
      </router-link></v-toolbar-title>
      <img class="title__logo__img"
        src="../../assets/twigene_logo.png"
        alt="twigene"
        >
      <v-spacer></v-spacer>
      <v-app-bar-nav-icon
      color="black"
      @click.stop="drawer=!drawer"
      >
      <v-avatar
      v-if="isLogin"
      color="grey lighten-4"
      >
      <img
        v-if="user"
        :src="user.providerData[0].photoURL"
        alt="profile"
        >
    </v-avatar>
      </v-app-bar-nav-icon>
    </v-toolbar>

    <v-navigation-drawer
    v-model="drawer"
    fixed
    temporary
    v-if="isLogin"
    >
    <v-list-item>
      <login />
    </v-list-item>
    <v-list-item>
      <UserProfile />
    </v-list-item>
    </v-navigation-drawer>
  </v-card>
</template>
<script>
import Login from './Login'
import UserProfile from '../UserProfile'
import firebase from 'firebase'

export default {
  name: 'Navbar',
  components: {
    Login,
    UserProfile
  },
  data () {
    return {
      screenName: this.userinfo ? this.userinfo.screenName : null,
      drawer: null,
      user: firebase.auth().currentUser
    }
  },
  mounted: function () {
    firebase.auth().onAuthStateChanged(
      user => {
        this.user = user || {}
      })
  },
  // pathの:idを直接書き換えた時の対応
  beforeRouteUpdate (to, from, next) {
    // 動的セグメントが変わった場合は、コールバック関数でtargetIdを更新する
    this.screen_name = to.params.id
    next()
  },
  methods: {
    signIn: function () {
      this.$store.dispatch('auth/login')
    }
  },
  computed: {
    isLogin () {
      return this.$store.getters['auth/check']
    },
    userinfo () {
      return this.$store.getters['auth/user']
    }
  }
}
</script>
<style>
.nav__title {
  color: #FF6F00;
  font-weight: bold;
}

.toolbar-title {
  color: #FF6F00 !important;
  text-decoration: inherit;
}
.title__logo {
  text-align: center;
}
.title__logo__img {
    height: 47px;
    width: 47px;
}
</style>
