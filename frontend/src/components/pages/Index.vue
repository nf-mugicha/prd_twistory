<template>
  <div class="index__conteiner text-center">
    <h5>自分botを作ってみよう！</h5>
    <h6 class="index__description">Aitter -ついじぇね- は、機械学習を使って「あなたっぽい」ツイートを自動生成するサービスです</h6>
      <login />
  </div>
</template>

<script>
import Login from '../common/Login'
import LinkList from '../pages/LinkList'
export default {
  name: 'Index',
  components: {
    'login': Login,
    'link-list': LinkList
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

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
.index__description {
  font-size: small;
  padding: 10px;
}
.index__conteiner {
  margin: auto;
}
</style>
