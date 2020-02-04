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

export default {
  name: 'Login',
  data: function () {
    return {
      processing: false,
    }
  },
  methods: {
    signIn: function () {
      try {
        this.processing = true
        this.$store.dispatch('auth/login')
      } catch (e) {
        this.processing = false
      } finally {
        this.processing = false
      }
    },
    signOut: function () {
      this.$store.dispatch('auth/logout')
      this.$router.push('/')
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
}
</script>
