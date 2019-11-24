<template>
  <div class="tweetlist index__conteiner text-center">
    <h5>自分botを作ってみよう！</h5>
    <h6 class="index__description">Aitter -ついじぇね- は、機械学習を使って「あなたっぽい」ツイートを自動生成するサービスです</h6>
    <not-found v-if="NotFound"></not-found>
    <div v-else>
     <v-card
     v-if="generatedTweet"
     class="mx-auto"
     color="#26c6da"
     dark
     width="100%"
     >
     <v-card-title>
       <span class="title font-weight-light">
         Generated {{ userinfo.displayName }}bot Tweet
       </span>
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
         <!-- <v-list-item-content
         class="twitter__displayname"
         > -->
           <!-- <v-list-item-title>
             {{ userinfo.displayName }}
           </v-list-item-title>
         </v-list-item-content> -->
         <v-row
         align="center"
         justify="end"
         >
         <v-btn class="pink lighten-3 text-center white--text">
           <font-awesome-icon :icon="['fab', 'twitter']"></font-awesome-icon>
           ツイートする
         <!-- <span class="subheading">45</span> -->
         </v-btn>
         </v-row>
       </v-list-item>
     </v-card-actions>
     </v-card>
     <v-btn
     class="primary btn__tweetgenerate"
     @click.prevent="TweetGenerate"
     :disabled="processing"
     :loading="processing"
     :block=true
     >ツイート生成する</v-btn>
     </div>
  </div>
</template>

<script>
import LinkPhoto from '../LinkPhoto'
import OneLink from '../OneLink'
import LinkListCard from '../LinkListCard'
import LinkListForm from '../LinkListForm'
import UserProfile from '../UserProfile'
import axios from 'axios'
import NotFound from '../pages/NotFound'
import { setTimeout } from 'timers'

export default {
  name: 'LinkList',
  components: {
    'link-photo': LinkPhoto,
    'one-link': OneLink,
    'link-list-card': LinkListCard,
    'link-list-form': LinkListForm,
    'user-profile': UserProfile,
    'not-found': NotFound
  },
  data () {
    return {
      generatedTweet: null,
      NotFound: false,
      processing: false
    }
  },
  props: [
    'screen_name'
  ],
  // pathの:idを直接書き換えた時の対応
  beforeRouteUpdate (to, from, next) {
    // 動的セグメントが変わった場合は、コールバック関数でtargetIdを更新する
    console.log('URL書き換え')
    console.log(to.params)
    this.screen_name = to.params.screen_name
    // this.$route.replace('/404')
    next()
    // this.isTrueURL()
  },
  mounted () {
    setTimeout(() => {
      this.isTrueURL()
    }, 2000)
  },
  methods: {
    TweetGenerate (btn) {
      if (this.processing) return
      this.processing = true
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
          this.processing = false
        })
        .catch(error => {
          console.log(error)
          this.processing = false
          this.generatedTweet = 'ツイート生成に失敗しました。もう一度試してみてください'
        })
    },
    isTrueURL () {
      console.log('ページが正しいか判定')
      const userurl = this.$store.getters['auth/user']
      if (userurl) {
        console.log('ログインしてる')
        if (userurl.screenName === this.$route.params.screen_name) {
          console.log('正しいURL')
          console.log(userurl.screenName)
          this.NotFound = false
        } else {
          console.log('正しくないURL')
          this.NotFound = true
        }
      } else {
        console.log('インデックスに飛ばす')
        this.$router.push('/')
      }
    }
  },
  // computedには結果がキャッシュされる
  // getterには引数は渡せない
  // ゲッター
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
<style>
.tweetlist {
  margin: auto;
  display: grid;
  width: 100%;
  height: fit-content;
}

.row__test__delete {
  margin: auto;
}

.index__description {
  font-size: small;
  padding: 10px;
}

.twitter__displayname {
  width: 50px;
}
</style>
