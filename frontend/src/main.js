import '@babel/polyfill'
// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import vuetify from './plugins/vuetify'
// ルートコンポーネントをインポートする
import App from './App'
// ルーティングの定義をインポートする
import router from './router'
// firebase構成をインポートする
import './plugins/firebase'
// 状態管理のストアをインポートする
import store from './store'
// CSRF対策
// import '../static/js/bootstrap'
// CSS有効化
import moment from 'vue-moment'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import firebase from 'firebase'
// font awesomeをインポート
import { library } from '@fortawesome/fontawesome-svg-core'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { fab } from '@fortawesome/free-brands-svg-icons'
import { far } from '@fortawesome/free-regular-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(fas, fab, far)
Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.use(moment)

Vue.config.productionTip = false

let createApp = (callback) => {
  firebase.auth().onAuthStateChanged(user => {
    if (user) {
      console.log(user)
      store.dispatch('auth/currentUser', user)
    } else {
      store.dispatch('auth/currentUser', null)
    }
  })

  /* eslint-disable no-new */
  new Vue({
    el: '#app',

    // 他のコンポーネトから、this.$routerやthis.$storeという方法でルーターや洗濯したパラメータの情報にアクセスできる
    'router': router,
    'store': store,
    components: { App },
    vuetify,
    template: '<App/>'
  })
}
createApp()
