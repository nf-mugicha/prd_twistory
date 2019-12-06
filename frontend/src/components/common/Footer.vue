<template>
  <footer class="footer">
    <v-footer
    color="primary lighten-1"
    padless
    >
    <v-row
    justify="center"
    no-gutters
    class="yellow darken-4 py-4 text-center white--text"
    >
    <v-btn
    v-for="link in links"
    :key="link"
    color="white"
    text
    rounded
    class="footer__col1"
    :to="link.path"
    >
    {{ link.name }}
    </v-btn>
    <v-btn
    color="white"
    text
    rounded
    class="footer__col1"
    >
      <Login />
    </v-btn>
    <v-col
    class="yellow darken-4 py-4 text-center white--text"
    cols="12"
    >
    {{ new Date().getFullYear() }} -- <strong>Aitter -ついじぇね- </strong>
    </v-col>
    </v-row>
    </v-footer>
  </footer>
</template>

<script>
import Login from './Login'
import LinkList from '../pages/LinkList'
import Index from '../pages/Index'
import TermsOfService from '../pages/TermsOfService'
import PrivacyPlicy from '../pages/PrivacyPolicy'
export default {
  name: 'Footer',
  components: {
    Login,
    LinkList,
    Index,
    TermsOfService,
    PrivacyPlicy
  },
  data: () => ({
    links: [
      { name: 'Home', path: '/', component: Index },
      { name: 'プライバシーポリシー', path: '/privacy-policy', component: PrivacyPlicy },
      { name: '利用規約', path: '/service', component: TermsOfService },
      { name: '公式Twitter', path: '/', component: Index }
    ]
  }),
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
.footer__col1 {
  font-size: 10px;
}
</style>
