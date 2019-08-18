<template>
  <div class="hello">
    <!-- <h1>{{ msg }}</h1> -->
    <h5>ユーザー名をタップするとユーザーページに飛ぶよ</h5>
    <h6>ログインして書き込んでみてね</h6>
    <user-profile />
    <login />
  </div>
</template>

<script>
import Login from '../common/Login'
import IndexList from '../IndexList'
import UserProfile from '../UserProfile'
export default {
  name: 'Index',
  data () {
    return {
      msg: 'Index'
    }
  },
  components: {
    'login': Login,
    'index-list': IndexList,
    'user-profile': UserProfile
  },
  computed: {
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
</style>
