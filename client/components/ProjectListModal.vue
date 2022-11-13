<template>
  <div class="project-list-modal">
    <div class="title">
      <div class="title-label">
        <font-awesome-icon :icon="['fas', 'project-diagram']" class="fa-2x" />
        <div>プロジェクト一覧</div>
      </div>
    </div>
    <div class="closed-button">
      <el-button type="secondary" v-on:click="onClosed($event)">閉じる</el-button>
    </div>
    <ProjectListView ref="refList" :limit="this.limit" :isEdit="false" @onSelectProject="onSelectProject" @getProjectList="getProjectList"></ProjectListView>
  </div>
</template>

<script>
import ProjectListView from '@/components/ProjectListView.vue'

export default {
  name: 'ProjectListModal',
  components: {
    ProjectListView,
  },
  props: {
    isEdit: Boolean,
  },
  data() {
    return{
      limit: 10,
    }
  },
  beforeCreated() {
  },
  created() {
  },
  beforeMount() {
  },
  mounted() {
    this.getProjectList(1)
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
    getProjectList(page){
      var items = [];
      var vm = this;
      var offset = page * this.limit - this.limit
      this.$apiService.getProjectList(this.limit, offset, function(res) {
        if(res != null) {
          var data = JSON.parse(res.data);
          if (data.project.length) {
            data.project.forEach(info => {
              var career = {
                id: info.id,
                projectName: info.name,
                overview: info.overview,
                startDate: vm.$utils.GetSlashDate(info.start_date),
                endDate: vm.$utils.GetSlashDate(info.end_date)
              }
              items.push(career)
            });
          vm.$refs.refList.setPager(items, data.totalCount, page);
          }
        }
      });
    },
    onSelectProject(record) {
      this.$emit('onSelectProject', record);
    },
    onClosed() {
      this.$emit('onClosed');
    },
  }
}
</script>

<style scoped>
.project-list-modal {
  overflow: scroll;
  padding-top: 2rem;
  padding-bottom: 2rem;
  z-index: 1;
}

.project-list-view {
  width: 90%;
  margin-left: 5%;
}

.title {
  width: 90%;
  margin-left: 5%;
  display: inline-block;
}

.closed-button {
  width: 90%;
  margin-left: 5%;
  /* bottom: 0; */
  padding: 1rem;
  text-align: right;
}

</style>