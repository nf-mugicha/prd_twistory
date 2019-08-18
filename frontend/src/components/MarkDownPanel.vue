<template>
    <div class="panel">
        <div class="panel-header">
            <figure class="avatar avata-lg">
                <img src="http://i.pravata.cc/320" alt="avatar">
            </figure>
            <div class="panel-title">User Name</div>
        </div>
        <div class="panal-nav">
            <ul class="tab">
                <li clss="tab-item"
                    :class="{ active: activeTab === 1 }"
                >
                <a href="#"
                    @click.prevent="activeTab = 1"
                >
                Write
                </a>
                <li class="tab-item"
                    :class="{ active: activeTab == 2 }"
                >
                <a href="#"
                    @click.prevent="activeTab = 2"
                >
                Preview
                </a>
                </li>
            </ul>
        </div>
        <div class="panel-body" v-show="activeTab === 1">
            <MarkdownEditor v-model="linkinfo.linkname"></MarkdownEditor>
            <markdown-editor v-model="linkinfo.linkurl"></markdown-editor>
        </div>
        <div class="panel-body" v-show="activeTab === 2">
            <MarkdownPreview :linkinfo="this.linkinfo" ></MarkdownPreview>
        </div>
        <div class="panel-footer">
            <div class="text-right">
                <button class="btn btn-primary">Submit</button>
            </div>
        </div>
    </div>
</template>

<script>
import MarkdownEditor from './MarkDownEditor'
import MarkdownPreview from './MarkDownPreview.vue'

export default {
  components: {
    MarkdownEditor,
    MarkdownPreview
  },
  data () {
    return {
      activeTab: 1,
      linkinfo: {linkname: '', linkurl: ''}
    }
  }
}
</script>
