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
    >
    {{ link }}
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
export default {
  name: 'Footer',
  components: {
    Login
  },
  data: () => ({
    links: [
      'Home',
      'プライバシーポリシー',
      '利用規約',
      '公式Twitter'
    ]
  })
}
</script>
<style>
.footer__col1 {
  font-size: 10px;
}
</style>
