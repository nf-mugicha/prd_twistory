<template>
  <div class="index__conteiner text-center">
    <h1>自分botを作ってみよう！</h1>
    <h3 v-if="!isLogin" class="index__description">
      Aitter -ついじぇね- は、「あなたっぽい」ツイートを自動生成するサービスです。<br>ツイートすればするほどそれっぽくなります。
      </h3>
      <p class="index__attention">初めてのツイート生成は時間が掛かります。
        <br>また鍵アカウントはツイート生成できませんが、
        <br>初回ツイート生成時のみ鍵を外して頂けたら、それ以降は鍵アカウントも使用可能です。
      </p>
      <generate-tweet-button
      v-if="isLogin"
      :screen_name="userinfo.screenName"
      >
      </generate-tweet-button>
      <login v-else />
      <index-explain />
  </div>
</template>

<script>
import Login from '../common/Login'
import GenerateTweetButton from '../GenerateTweetButton'
import IndexExplain from '../IndexExplain'
export default {
  name: 'Index',
  components: {
    'login': Login,
    'generate-tweet-button': GenerateTweetButton,
    'index-explain': IndexExplain,
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
<style>
h1 {
  font-weight: bold;
  font-size: 24px;
}
h2 {
  font-weight: bold;
  font-size: 20px;
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
