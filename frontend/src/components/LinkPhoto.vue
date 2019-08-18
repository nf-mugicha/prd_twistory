<template>
    <div class="photo">
        <figure class="photo__wrapper">
            {{ link_list }}
            <img
                class="photo__image photo__image--portrait"
                :src="'link_list.link_photo'"
                :alt="'{{ link_list }}'"
            >
        </figure>
        <router-link
        class="photo_overlay"
        :to="'/${link_list.user_id}/${link_list.create_num}'"
        :title="'View the photo by ${link_list.user_name}'"
        >
        <div class="photo__controls">
            <button
                class="photo__action photo__action--like"
                title="Like photo"
            >
                <i class="icon ion-md-heart"></i>12
            </button>
        </div>
        </router-link >
    </div>
</template>

<script>
export default {
  name: 'LinkPhoto',
  props: {
    linklist: {
      type: Object,
      required: true
    }
  }
}
</script>
