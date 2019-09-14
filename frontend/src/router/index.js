import Vue from 'vue'
import VueRouter from 'vue-router'
// import firebase from 'firebase'
// // 状態管理のストアをインポートする
// import store from '../store'

// ページコンポーネントのインポート
import LinkList from '../components/pages/LinkList'
import NotFound from '../components/pages/NotFound'
import MarkDownPanel from '../components/MarkDownPanel'
import Index from '../components/pages/Index'

// VueRouterプラグインを使用する
// これによって<RouterView />コンポーネントなどを使うことができる
Vue.use(VueRouter)

// パスとコンポーネントのマッピング
const routes = [{
  path: '/',
  component: Index
},
{
  path: '/:screen_name',
  name: 'LinkList',
  component: LinkList,
  props: true,
  meta: {
    title: 'link list'
  }
},
{
  path: '/404',
  component: NotFound
},
{
  path: '*',
  redirect: '/404'
},
{
  path: '/panel',
  component: MarkDownPanel
}
]

// VueRouterインスタンスを作成する
const router = new VueRouter({
  mode: 'history',
  routes,
  history
})

// VueRouterインスタンスをエクスポートする
// main.jsでインポートする
export default router
