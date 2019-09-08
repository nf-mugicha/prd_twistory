<template>
  <v-app id="app">
    <Navbar />
    <v-content class="main__conteiner">
      <router-view></router-view>
    </v-content>
    <Footer />
  </v-app>
</template>

<script>
import Navbar from './components/common/Navbar'
import Login from './components/common/Login'
import Footer from './components/common/Footer'

export default {
  name: 'App',
  components: {
    Navbar,
    Login,
    Footer
  },
  data: () => ({
    //
  })
}
</script>
<style>
.main__conteiner {
  margin: auto;
  padding: 20px !important;
}
</style>
