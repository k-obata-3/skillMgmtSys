<template>
  <div class="user-setting">
    <div class="title-label">
      <font-awesome-icon :icon="['fas', 'user-cog']" class="fa-2x" />
      <div>個人設定</div>
    </div>
    <div class="contents">
      <div class="user-edit-btn-area">
        <div class="user-edit-registered-btn">
          <el-button type="secondary" v-on:click="onRegistered($event)">登録</el-button>
        </div>
      </div>
      <UserInfoEditView ref="child" :usesrId="this.id" :isAdd="false" :isSetting="false" @onUpdateComplete="onUpdateComplete"></UserInfoEditView>
    </div>
  </div>
</template>

<script>
import UserInfoEditView from '@/components/UserInfoEditView.vue'

export default {
  name: 'UserSetting',
  components: {
    UserInfoEditView,
  },
  props: {
  },
  data() {
    return {
      id: this.$utils.getUserId()
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
    onRegistered(event) {
      this.$refs.child.onRegistered(event);
    },
    onUpdateComplete() {
      this.$message({type: 'success', message: '登録しました。'});
    },
  },
}
</script>

<style scoped>
.user-setting {

}

</style>
