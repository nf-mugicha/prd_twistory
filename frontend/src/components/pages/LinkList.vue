<template>
  <div class="tweetlist">
    <!-- <user-profile
    v-bind:user_profile="screen_name"
     /> -->
     <v-card
     v-if="generatedTweet"
     class="mx-auto"
     color="#26c6da"
     dark
     max-width="400"
     >
     <v-card-title>
       <v-icon
       large
       left
       >
       mdi-twitter
       </v-icon>
       <span class="title font-weight-light">Twitter</span>
     </v-card-title>
     <v-card-text class="headline font-weight-bold">
        {{ generatedTweet }}
     </v-card-text>
     <v-card-actions>
       <v-list-item class="grow">
         <v-list-item-avatar color="grey darken-3">
         <v-img
         class="elevation-6"
         :src="userinfo.photoURL"
         ></v-img>
         </v-list-item-avatar>
         <v-list-item-content>
           <v-list-item-title>
             Even You
           </v-list-item-title>
         </v-list-item-content>
         <v-row
         align="center"
         justify="end"
         >
         <v-icon class="mr-1">mdi-heart</v-icon>
         <span class="subheading mr-2">256</span>
         <span class="mr-1">.</span>
         <v-icon class="mr-1">mdi-share0cariant</v-icon>
         <span class="subheading">45</span>
         </v-row>
       </v-list-item>
     </v-card-actions>
     </v-card>
     <v-btn
     class="primary"
     @click="TweetGenerate"
     >ツイート生成する</v-btn>
  </div>
</template>

<script>
import LinkPhoto from '../LinkPhoto'
import OneLink from '../OneLink'
import LinkListCard from '../LinkListCard'
import LinkListForm from '../LinkListForm'
import UserProfile from '../UserProfile'
import axios from 'axios'

export default {
  name: 'LinkList',
  components: {
    'link-photo': LinkPhoto,
    'one-link': OneLink,
    'link-list-card': LinkListCard,
    'link-list-form': LinkListForm,
    'user-profile': UserProfile
  },
  data () {
    return {
      generatedTweet: null
    }
  },
  props: [
    'screen_name'
  ],
  // pathの:idを直接書き換えた時の対応
  // beforeRouteUpdate (to, from, next) {
  //   // 動的セグメントが変わった場合は、コールバック関数でtargetIdを更新する
  //   console.log('URL書き換え')
  //   console.log(to.params)
  //   this.screen_name = to.params.screen_name
  //   next()
  //   console.log('beforeRouteUpdateだよ')
  //   this.init()
  //   this.start(this.screen_name)
  //   this.getUser(this.screen_name)
  // },
  // mounted () {
  //   console.log('mountedだよ')
  //   this.init()
  //   this.start(this.screen_name)
  //   // this.getUser(this.screen_name)
  // },
  // destroyed () {
  //   this.stop()
  // },
  methods: {
    TweetGenerate () {
      // POST送信する
      axios.post(
        'http://127.0.0.1:5000/generate',
        {
          account: this.screen_name
        }
      )
      // 送信完了
        .then((res) => {
          console.log(res)
          console.log(res.data)
          this.generatedTweet = res.data
        })
        .catch(error => {
          console.log(error)
        })
    }
  },
  //   init () {
  //     console.log('メモを検索する')
  //     this.$store.dispatch('links/clear')
  //   },
  //   start (screenName) {
  //     console.log(screenName)
  //     this.$store.dispatch('links/startListener', {screenName})
  //   },
  //   stop () {
  //     this.$store.dispatch('links/stopListener')
  //   },
  //   remove (id) {
  //     console.log(this.$store.dispatch('links/deleteLink', {id}))
  //     this.$store.dispatch('links/deleteLink', {id})
  //   },
  //   getUser (userProfile) {
  //     this.$store.dispatch('user/userData', {screen_name: userProfile})
  //   }
  // },
  // computedには結果がキャッシュされる
  // getterには引数は渡せない
  // ゲッター
  computed: {
    userinfo () {
      console.log('userinfo取得')
      return this.$store.getters['auth/user']
    },
    isLogin () {
      console.log('ログイン判定取得')
      return this.$store.getters['auth/check']
    }
    // links () {
    //   console.log('getter')
    //   return this.$store.getters['links/data']
    // },
    // userdata () {
    //   return this.$store.getters['user/userProfile']
    // }
  }
}
</script>
<style>
.tweetlist {
  margin: auto;
}

.row__test__delete {
  margin: auto;
}
</style>
