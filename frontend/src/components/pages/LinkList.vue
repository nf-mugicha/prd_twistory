<template>
  <div class="tweetlist index__conteiner text-center">
    <not-found v-if="NotFound"></not-found>
    <div v-else>
     <v-card
     v-if="generatedTweet"
     class="mx-auto"
     color="#FFFFFF"
     width="100%"
     >
     <v-card-title
     class="amber darken-4 title__displayname"
     dark
     >
       <span class="font-weight">
         {{ userinfo.displayName }} bot のツイート
       </span>
     </v-card-title>
     <v-card-text class="headline font-weight-bold text__description">
        {{ generatedTweet }}
     </v-card-text>
     <v-card-actions>
       <v-list-item class="grow">
         <v-list-item-avatar color="grey darken-3">
         <v-img
         class="elevation-6"
         :src="user.providerData[0].photoURL"
         ></v-img>
         </v-list-item-avatar>
         <v-row
         align="center"
         justify="end"
         >
         <v-btn
         class="light-blue darken-1 text-center white--text"
         @click.prevent="TweetPost"
         :disabled="processing"
         :loading="processing"
         >
           <font-awesome-icon :icon="['fab', 'twitter']"></font-awesome-icon>
           結果をツイートする
         </v-btn>
         </v-row>
       </v-list-item>
     </v-card-actions>
     </v-card>
     <v-btn
     class="amber darken-4 btn__tweetgenerate"
     dark
     @click.prevent="TweetGenerate"
     :disabled="processing"
     :loading="processing"
     :block=true
     >ツイート生成する</v-btn>
     </div>
  </div>
</template>

<script>
import axios from 'axios'
import NotFound from '../pages/NotFound'
import CONSTANT from '../constants/index'
import firebase from 'firebase'

export default {
  name: 'LinkList',
  components: {
    'not-found': NotFound
  },
  data () {
    return {
      generatedTweet: null,
      NotFound: false,
      processing: false,
      tweetUrl: '',
      tweetText: '',
      user: firebase.auth().currentUser
    }
  },
  mounted: function () {
    firebase.auth().onAuthStateChanged(
      user => {
        this.user = user || {}
      })
  },
  props: {
    screen_name: {
      type: String,
      default: null
    }
  },
  // pathの:idを直接書き換えた時の対応
  beforeRouteUpdate (to, from, next) {
    // 動的セグメントが変わった場合は、コールバック関数でtargetIdを更新する
    this.screen_name = to.params.screen_name
    next()
  },
  methods: {
    PostingTweet (btn) {
      if (this.processing) return
      this.processing = true
      const userinfo = this.$store.getters['auth/user']
      // POST送信する
      axios.post(
        CONSTANT.TWEET_URL,
        {
          account: this.screen_name,
          generated_text: this.generatedTweet,
          accessToken: userinfo.accessToken,
          secretToken: userinfo.secretToken,
          displayName: userinfo.displayName
        }
      )
      // 送信完了
        .then((res) => {
          this.processing = false
          if (res.data['status'] !== 200) {
            const tweetPage = this.createTweetUrl()
            if (!window.open(tweetPage)) {
              window.location.href = tweetPage
            } else {
              window.open(tweetPage)
            }
          } else if (res.data['status'] === 200) {
            alert(res.data['res_text'])
          }
        })
        .catch(error => {
          console.log(error)
          this.processing = false
          // alert('ツイートに失敗しました。投稿画面を開きます')
          const tweetPage = this.createTweetUrl()
          window.location.href = tweetPage
        })
    },
    TweetPost (btn) {
      if (this.processing) return
      this.processing = true
      const userinfo = this.$store.getters['auth/user']
      const tweetPage = this.createTweetUrl()
      if (!window.open(tweetPage)) {
        window.location.href = tweetPage
      } else {
        window.open(tweetPage)
      }
    },
    createTweetUrl () {
      // Twitter用のurl作成
      const url = encodeURIComponent(location.href)
      const hashTags = encodeURI('ついじぇね,自分bot')
      const generatedText = encodeURI(this.generatedTweet + '\n\n')
      this.tweetUrl = 'https://twitter.com/intent/tweet?text=' + generatedText + '&hashtags=' + hashTags + '&url=' + url
      return this.tweetUrl
    },
    TweetGenerate (btn) {
      if (this.processing) return
      this.processing = true
      // POST送信する
      axios.post(
        CONSTANT.GENERATE_URL,
        {
          account: this.screen_name
        }
      )
      // 送信完了
        .then((res) => {
          this.generatedTweet = res.data
          this.processing = false
        })
        .catch(error => {
          this.processing = false
          this.generatedTweet = 'ツイート生成に失敗しました。もう一度試してみてください'
          axios.post(
            CONSTANT.SLACK_SERVER_ERROR,
            {
              text: this.generatedTweet + "\n" + error,
              username: this.screen_name
            }).then( res => {

          }).catch(err => {
            console.log("error: ", err)
          })
        })
    },
    isTrueURL () {
      const userurl = this.$store.getters['auth/user']
      if (userurl) {
        if (userurl.screenName === this.$route.params.screen_name) {
          this.NotFound = false
        } else {
          this.NotFound = true
        }
      } else {
        this.$router.push('/')
      }
    }
  },
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
  /* font-size: small; */
  /* padding: 10px; */
}

.twitter__displayname {
  width: 50px;
}

.title__displayname {
  font-size: 1rem;
  color: #ffffff;
}

.text__description {
  padding-top: 16px !important;
}
</style>
