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
      <img
        v-if="isLogin"
        class="title__logo__img"
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
        v-if="userinfo.photoURL"
        :src="userinfo.photoURL"
        alt="profile"
        >
    </v-avatar>
    <v-avatar v-else>
      <img class="title__logo__img"
        src="../../assets/twigene_logo.png"
        alt="twigene"
      >
    </v-avatar>
      </v-app-bar-nav-icon>
    </v-toolbar>

    <v-navigation-drawer
    v-model="drawer"
    fixed
    temporary
    text-center
    >
    <v-list-item>
      <v-col>
        <v-btn
          v-for="link in links"
          :key="link"
          color="grey"
          text
          rounded
          class="footer__col1"
          :to="link.path"
        >
          {{ link.name }}
        </v-btn>
      </v-col>
    </v-list-item>
    <v-list-item>
      <v-col>
      <v-btn
        color="grey"
        text
        rounded
        class="footer__col1"
        href="https://twitter.com/twigene_aitter"
        >
        公式Twitter
      </v-btn>
      </v-col>
    </v-list-item>
    <v-list-item>
      <v-col>
      <v-btn
        color="grey"
        text
        rounded
        class="footer__col1"
        href="https://forms.gle/euY2WbdRziXjFSUk9"
        >
        お問い合わせ
      </v-btn>
      </v-col>
    </v-list-item>
    <v-list-item>
      <v-col>
      <login />
      </v-col>
    </v-list-item>
    </v-navigation-drawer>
  </v-card>
</template>
<script>
import Login from './Login'
import Index from '../pages/Index'
import UserProfile from '../UserProfile'
import TermsOfService from '../pages/TermsOfService'
import PrivacyPlicy from '../pages/PrivacyPolicy'

export default {
  name: 'Navbar',
  components: {
    Login
  },
  data () {
    return {
      screenName: this.userinfo ? this.userinfo.screenName : null,
      drawer: null,
      links: [
        { name: 'Home', path: '/', component: Index },
        { name: 'プライバシーポリシー', path: '/privacy-policy', component: PrivacyPlicy },
        { name: '利用規約', path: '/service', component: TermsOfService }
      ]
    }
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
