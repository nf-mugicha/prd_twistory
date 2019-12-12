<template>
  <v-card flat tile
  >
    <v-toolbar dense>
      <div>
      <v-toolbar-title
      class="nav__title"
      to="/"
      >AItter -ついじぇね-</v-toolbar-title>
      </div>
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
        v-if="userinfo.photoURL"
        :src="userinfo.photoURL"
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
import LinkList from '../pages/LinkList'
import UserProfile from '../UserProfile'

export default {
  name: 'Navbar',
  components: {
    Login,
    LinkList,
    UserProfile
  },
  data () {
    return {
      screenName: this.userinfo ? this.userinfo.screenName : null,
      drawer: null
    }
  },
  // props: {
  //   'screen_name': {
  //     type: Object,
  //     required: true
  //   }
  // },
  // pathの:idを直接書き換えた時の対応
  beforeRouteUpdate (to, from, next) {
    // 動的セグメントが変わった場合は、コールバック関数でtargetIdを更新する
    console.log('URL書き換え')
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
}
</style>
