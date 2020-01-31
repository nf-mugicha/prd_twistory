import Vue from 'vue'
import VueRouter from 'vue-router'
// import firebase from 'firebase'
// // 状態管理のストアをインポートする
// import store from '../store'

// ページコンポーネントのインポート
import NotFound from '../components/pages/NotFound'
import Index from '../components/pages/Index'
import TermsOfService from '../components/pages/TermsOfService'
import PrivacyPolicy from '../components/pages/PrivacyPolicy'
import AllTweetsList from '../components/pages/AllTweetsList'
import OneTweetPage from '../components/pages/OneTweetPage'
import UserPage from '../components/pages/UserPage'

// VueRouterプラグインを使用する
// これによって<RouterView />コンポーネントなどを使うことができる
Vue.use(VueRouter)

// パスとコンポーネントのマッピング
const routes = [{
        path: '/',
        component: Index
    },
    {
        path: '/all',
        name: 'AllTweetsList',
        component: AllTweetsList
    },
    {
        path: '/u/:screen_name/:id',
        name: 'OneTweetPage',
        component: OneTweetPage,
        props: true, // データの受け渡しを可能にする
        meta: {
            title: 'details of link'
        }
    },
    {
        path: '/u/:screen_name',
        name: 'UserPage',
        component: UserPage,
        props: true,
        meta: {
            title: 'users tweets list'
        }
    },
    {
        path: '/404',
        component: NotFound
    },
    {
        name: 'TermsOfService',
        path: '/service',
        component: TermsOfService
    },
    {
        name: 'PrivacyPolicy',
        path: '/privacy-policy',
        component: PrivacyPolicy
    },
    {
        path: '*',
        redirect: '/404'
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