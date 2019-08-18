import Vue from 'vue'
import Vuex from 'vuex'
import links from './modules/links'
import link from './modules/link'
import auth from './modules/auth'
import user from './modules/user'

Vue.use(Vuex)

const store = new Vuex.Store({
  modules: {
    links: links,
    link: link,
    auth: auth,
    user: user
  },
  strict: process.env.NODE_ENV !== 'production'
})

export default store
