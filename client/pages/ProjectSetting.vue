<template>
  <div class="project-setting">
    <div class="title-label">
      <font-awesome-icon :icon="['fas', 'list-check']" class="fa-2x" />
      <div>プロジェクト管理</div>
    </div>
    <div class="contents">
      <div class="career-info-table" v-show="!isEditMode">
        <div class="header">
          <el-button type="secondary" v-on:click="add()">追加</el-button>
        </div>
        <ProjectListView ref="refList" :limit="this.limit" :isEdit="true" @onEdit="onEdit" @getProjectList="getProjectList"></ProjectListView>
      </div>
      <div class="career-info-edit" v-show="isEditMode">
        <ProjectEditView ref="refEdit" @onDelete="onDelete" @onCancel="onCancel" @onRegistered="onRegistered"></ProjectEditView>
      </div>
    </div>
  </div>
</template>

<script>
import ProjectListView from '@/components/ProjectListView.vue'
import ProjectEditView from '@/components/ProjectEditView.vue'

export default {
  name: 'ProjectSetting',
  components: {
    ProjectListView,
    ProjectEditView,
  },
  props: {
  },
  data() {
    return{
      companyId: this.$utils.getCompanyId(),
      isEditMode: false,
      list: [],
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
    this.setListMode();
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
      this.$apiService.getProjectList(this.companyId, this.limit, offset, function(res) {
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
    onRegistered(){
      this.setListMode();
    },
    onDelete(){
      this.setListMode();
    },
    onEdit(record) {
      this.setEditMode(record.id, this.companyId);
    },
    onCancel(){
      this.setListMode();
    },
    add() {
      this.setEditMode(null, this.companyId);
    },
    setListMode() {
      this.getProjectList(1);
      this.isEditMode = false;
    },
    setEditMode(id) {
      this.$refs.refEdit.callApi(id, this.companyId);
      this.isEditMode = true;
    }
  }
}
</script>

<style scoped>
.project-setting {

}

.header {
  text-align: right;
  padding: 0.5rem;
}

.edit-form, .add-form {
  margin-top: 1rem;
  padding: 1rem;
  border: solid 1px #ced4da;
}
</style>
