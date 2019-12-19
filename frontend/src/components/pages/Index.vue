<template>
  <div class="index__conteiner text-center">
    <h1>自分botを作ってみよう！</h1>
    <h3 class="index__description">
      Aitter -ついじぇね- は、「あなたっぽい」ツイートを自動生成するサービスです。<br>ツイートすればするほどそれっぽくなります。
      <p class="index__attention">初めてのツイート生成は時間が掛かります！気長にお待ち下さい・・</p>
      </h3>
    <link-list
    v-if="isLogin"
    :screen_name="userinfo.screenName"
    >
    </link-list>
      <login v-else />
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
.index__attention {
  color:red;
  font-weight: bold;
}
</style>
