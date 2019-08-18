<template>
    <div v-if="isLogin" class="card md-2 float-lg-left" style="width: 18rem;">
      <v-card class="elevation-12">
        <div class="card-header text-left">
            <input type="text" class="form-control" placeholder="link_title" v-model.trim="link.link_title">
        </div>
        <div class="card-body text-left">
            <textarea class="form-control" placeholder="descriptioin" v-model.trim="link.description"></textarea>
        </div>
        <!-- <button class="button" @click="showForm = ! showForm">
          <i class="icon ion-md-add"></i>
          photo upload
        </button> -->
        <!-- <PhotoUpload v-model="showForm" /> -->
                <output class="form__output" v-if="preview">
                    <img
                        :src="preview"
                        alt=""
                        width="200px"
                        >
                </output>
                <v-card-actions>
                    <v-spacer></v-spacer>
                <v-btn color="primary"
                label="Select Image"
                @click="pickFile"
                v-model="imageName"
                prepend-icon="attach_file"
                >
                アイキャッチ画像
                <input
                type="file"
                style="display: none"
                ref="image"
                accept="image/*"
                @change="onFilePicked"
                />
                </v-btn>
                </v-card-actions>
        <div class="card-footer text-right">
            <button class="btn-sm btn-secondary" type="submit" v-on:click.prevent="addLink">add</button>
        </div>
        </v-card>
    </div>
</template>
<script>
import CONSTANTS from './constants'
// import PhotoUpload from './PhotoUpload'
import firebase from 'firebase'
// import firestore from '../plugins/firebase'

export default {
  name: 'LinkListForm',
  components: {
    // PhotoUpload
  },
  data () {
    return {
      link: this.emptyLink(),
      showForm: false,
      preview: null,
      photo: null,
      photo_url: null,
      dialog: false,
      imageName: null,
      imageURL: null,
      imageFile: null
    }
  },
  methods: {
    addLink () {
      if (!this.link.link_title || !this.link.description) {
        return
      }
      console.log('add new Link')
      console.log(new Date())
      //   console.log(this.emptyLink())
      this.link.platforms = []
      this.link.million = false
      this.link.createAt = new Date()
      this.link.userinfo = this.userinfo
      this.link.screenName = this.userinfo.screenName
      this.link.uid = this.userinfo.uid
      this.link.id_str = this.userinfo.id_str
      if (!this.imageName) {
        console.log(this.link)
        // ステートを変更
        this.$store.dispatch('links/addLink', this.link)
        // 空に戻す
        this.link = this.emptyLink()
      }
      // ストレージオブジェクト作成
      const storageRef = firebase.storage().ref()
      // ファイルパス設定
      // eslint-disable-next-line no-template-curly-in-string
      const mountainRef = storageRef.child('linkEyeCatchImage/' + this.imageFile.name)
      // ファイルを適用してファイルアップロード
      mountainRef.put(this.imageFile).then(snapshot => {
        snapshot.ref.getDownloadURL().then(downloadURL => {
          this.imageURL = downloadURL
          console.log(this.imageURL)
          this.link.photoURL = downloadURL
          // firestore.collection('LinkPage').add({
          //   'photoURL': downloadURL
          // })
          console.log(this.link)
          // ステートを変更
          this.$store.dispatch('links/addLink', this.link)
          // 空に戻す
          this.link = this.emptyLink()
          this.preview = null
        })
      })
    },
    emptyLink () {
      console.log('empty link')
      return CONSTANTS.NEW_EMPTY_MEMO()
    },
    pickFile () {
      this.$refs.image.click()
    },
    onFilePicked (event) {
      // フォームでファイルが選択されたら実行される
      console.log(event.target.files)
      if (event.target.files.length === 0) {
        console.log(event.target.files.length)
        this.reset()
        return false
      }
      // ファイルが画像でなかったら処理中断
      if (!event.target.files[0].type.match('image/*')) {
        console.log(event.target.files[0].type)
        this.reset()
        return false
      }
      // ファイルリーダーを立ち上げる
      const reader = new FileReader()
      reader.readAsDataURL(event.target.files[0])
      reader.addEventListener('load', () => {
        this.imageURL = reader.result
        this.imageFile = event.target.files[0]
        this.imageName = event.target.files[0].name
        // console.log(this.preview)
        // this.uploadPhoto()
      })
      // 画像が読み込まれたタイミングで実行される
      reader.onload = e => {
        // previewに読み込み結果（データURL）を代入する
        // previewに値が入ると<output>につけたv-ifがtrueと判定される
        // また、<output>内部の<img>のsrc属性はpreviewの値を参照しているので、結果として画像が表示される
        this.preview = e.target.result
        console.log(this.preview)
      }
      // ファイルを読み込む
      // 読み込まれたファイルはデータURL形式で受け取れる（上記onload参照）
      reader.readAsDataURL(event.target.files[0])
    },
    reset () {
      this.preview = ''
      this.$el.querySelector('input[type="file]').value = null
    },
    // 画像アップロード処理
    uploadPhoto () {
      // ストレージオブジェクト作成
      const storageRef = firebase.storage().ref()
      // ファイルパス設定
      // eslint-disable-next-line no-template-curly-in-string
      const mountainRef = storageRef.child('linkEyeCatchImage/' + this.imageFile.name)
      // ファイルを適用してファイルアップロード
      mountainRef.put(this.imageFile).then(snapshot => {
        snapshot.ref.getDownloadURL().then(downloadURL => {
          this.imageURL = downloadURL
          console.log(this.imageURL)
          this.link.photoURL = downloadURL
          // firestore.collection('LinkPage').add({
          //   'photoURL': downloadURL
          // })
        })
      })
    }
  },
  computed: {
    isLogin () {
      return this.$store.getters['auth/check']
    },
    userinfo () {
      return this.$store.getters['auth/user']
    }
  },
  watch: {
    'link' (n, o) {
      console.log('new: %s, old: %s', JSON.stringify(n), JSON.stringify(o))
    }
  }
}
</script>
