<template>
    <div>
        <div class="empty" v-if="linkinfo.linkname === ''">
            No content yet.
        </div>
        <div v-else v-html="html"></div>
    </div>
</template>

<script>
export default {
  props: {
    linkinfo: {
      type: Object,
      required: true
    }
  },
  computed: {
    html () {
      return '<a href=' +
      this.linkinfo.linkurl +
      "target='_blank'>" +
      this.linkinfo.linkname +
      '</a>'
    }
  }
}
</script>
