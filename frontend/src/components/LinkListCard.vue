<template>
<div class="linkcard">
  <v-card
  width="320px"
  raised
  elevation="10"
  >
    <v-container fill-height fluid pa-2>
      <v-layout align-center fill-height>
        <v-flex align-end xs12 flexbox>
          <!-- <v-img :src="link.src" max-height="100px"></v-img> -->
                        <router-link
                v-bind:to="{name: 'LinkPage',
            params: {link_id: link.link_id, id: link.id, screen_name: link.screenName} }"
              >
          <v-img
          src="https://cdn.vuetifyjs.com/images/cards/docks.jpg"
          height="200px"
          v-if="!link.photoURL"
          >
          <v-btn flat
          v-bind:to="{name: 'LinkList', params: {screen_name: link.screenName}}"
          >
          {{ link.userinfo.displayName }}
          </v-btn>
          </v-img>
          <v-img
          v-else
          :src="link.photoURL"
          height="200px"
          >
          <v-btn flat
          v-bind:to="{name: 'LinkList', params: {screen_name: link.screenName}}"
          >
          {{ link.userinfo.displayName }}
          </v-btn>
          </v-img>
          </router-link>
          <router-link v-bind:to="{name: 'LinkPage',
            params: {link_id: link.link_id, id: link.id, screen_name: link.screenName} }">
          <v-card-title class="card__title">
            <h3>{{ formatedTitle }}</h3>
              </v-card-title>
              </router-link>
              <v-card-text class="card__text">
                <h6 class="grey--text">{{ formatedDescription }}</h6>
              </v-card-text>
          <v-card-actions class="card__actions">
            <v-spacer></v-spacer>
            <v-btn icon>
              <v-icon>favorite</v-icon>
            </v-btn>
            <v-btn icon>
              <v-icon>share</v-icon>
            </v-btn>
          </v-card-actions>
        </v-flex>
      </v-layout>
    </v-container>
  </v-card>
  </div>
</template>

<script>
export default {
  name: 'LinkListCard',
  data () {
    return {releasedAtFromNow: this.getReleasedAtFromNow()
    }
  },
  moutend () {
    // releasedAtFromNowを1分ごとに更新する
    window.setInerval(() => {
      this.releasedAtFromNow = this.getReleasedAtFromNow()
    }, 1000 * 60)
  },
  props: {
    'link': {
      type: Object,
      required: true
    }
  },
  methods: {
    getReleasedAtFromNow () {
      if (!this.link || !this.link.createAt) {
        return ''
      }
      const createAt = new Date(this.link.createAt.seconds * 1000)
      return this.$moment(createAt).fromNow()
    },
    getOmissionAndPlusMidpoint (str, limit) {
      if (str.length < limit) {
        return str
      }
      return str.substr(0, limit) + '...'
    }
  },
  computed: {
    userdata () {
      return this.$store.getters['user/userProfile']
    },
    formatedTitle () {
      if (!this.link || !this.link.link_title) {
        return ''
      }
      return this.getOmissionAndPlusMidpoint(this.link.link_title, 16)
    },
    formatedDescription () {
      if (!this.link || !this.link.description) {
        return ''
      }
      return this.getOmissionAndPlusMidpoint(this.link.description, 60)
    }
  },
  watch: {
    'link' (n, o) {
      console.log('watch link')
    }
  }
}
</script>
<style>
.linkcard {
  padding:1px;
}
.card__title {
  padding-top:5px;
  padding-bottom: 5px;
  color:#000;
}
.card__text {
  padding-top:1px;
  padding-bottom: 5px;
}
.card__actions {
  padding:0px;
}
</style>
