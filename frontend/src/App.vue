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
  font-size: 0.75rem;
}

.main__conteiner h1 {
  font-size: 1.25rem;
}

.main__conteiner h2 {
  font-size: 1rem;
  margin: 2px;
}

.main__conteiner h3 {
  font-size: 13px;
}
</style>
