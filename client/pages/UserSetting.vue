<template>
  <div class="user-setting">
    <div class="title-label">
      <font-awesome-icon :icon="['fas', 'user-cog']" class="fa-2x" />
      <div>個人設定</div>
    </div>
    <div class="contents">
      <UserSettingView ref="child"></UserSettingView>
    </div>
  </div>
</template>

<script>
import UserSettingView from '@/components/UserSettingView.vue'

export default {
  name: 'UserSetting',
  components: {
    UserSettingView,
  },
  props: {
  },
  data() {
    return {
    }
  },
  beforeCreated() {
  },
  created() {
  },
  beforeMount() {
  },
  mounted() {
  },
  beforeUpdate() {
  },
  updated() {
  },
  beforeDestroy() {
  },
  destroyed() {
  },
  methods: {
  },
}
</script>

<style scoped>
.user-setting {

}

</style>
