<template>
  <footer class="footer">
    <v-footer
    color="primary lighten-1"
    padless
    >
    <v-row
    justify="center"
    no-gutters
    class="amber lighten-5 py-4 text-center grey--text"
    >
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
    <v-btn
    color="grey"
    text
    rounded
    class="footer__col1"
    href="https://twitter.com/twigene_aitter"
    >
    公式Twitter
    </v-btn>
    <v-btn
    color="grey"
    text
    rounded
    class="footer__col1"
    href="https://forms.gle/euY2WbdRziXjFSUk9"
    >
    お問い合わせ
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
    class="amber lighten-5 py-4 text-center grey--text"
    cols="12"
    >
    {{ new Date().getFullYear() }} -- <strong>Aitter - ついじぇね - </strong>
    </v-col>
    </v-row>
    </v-footer>
  </footer>
</template>

<script>
import Login from './Login'
import Index from '../pages/Index'
import TermsOfService from '../pages/TermsOfService'
import PrivacyPlicy from '../pages/PrivacyPolicy'
export default {
  name: 'Footer',
  components: {
    Login,
    Index,
    TermsOfService,
    PrivacyPlicy
  },
  data: () => ({
    links: [
      { name: 'Home', path: '/', component: Index },
      { name: 'プライバシーポリシー', path: '/privacy-policy', component: PrivacyPlicy },
      { name: '利用規約', path: '/service', component: TermsOfService }
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
