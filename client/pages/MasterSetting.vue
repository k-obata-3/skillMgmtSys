<template>
  <div class="master-setting">
    <div class="title-label">
      <font-awesome-icon :icon="['fas', 'cubes']" class="fa-2x" />
      <div>マスタ管理</div>
    </div>
    <div class="contents">
      <MasterSettingView></MasterSettingView>
    </div>
  </div>
</template>

<script>
import MasterSettingView from '@/components/MasterSettingView.vue'

export default {
    name: 'MasterSetting',
    components: {
        MasterSettingView,
    },
    data() {
      return{

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
    methods:{

    }
}
</script>

<style scoped>

</style>
