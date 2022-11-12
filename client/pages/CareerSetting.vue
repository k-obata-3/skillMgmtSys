<template>
  <div class="career-setting">
    <div class="title-label">
      <font-awesome-icon :icon="['fas', 'user-edit']" class="fa-2x" />
      <div>経歴編集</div>
    </div>
    <div class="contents">
      <div class="career-info-table" v-show="!this.isEditMode">
        <div class="btn-area-top-right"></div>
        <div class="btn-area-top-left">
          <div class="add-btn">
            <el-button type="secondary" v-on:click="showProjectList()">プロジェクト一覧</el-button>
            <el-button type="secondary" v-on:click="add()">追加</el-button>
          </div>
        </div>
        <CareerInfoListView ref="refList" :limit="this.limit" @onEdit="onEdit" @onPreview="onPreview" @getCareerInfoList="getCareerInfoList"></CareerInfoListView>
      </div>
      <div class="career-info-edit" v-show="this.isEditMode">
        <CareerInfoEditView ref="refEdit" @onDelete="onDelete" @onCancel="onCancel" @onRegistered="onRegistered"></CareerInfoEditView>
      </div>
    </div>
    <transition name="modal">
      <div v-show="this.isModalShow">
        <!-- <div class="overlay" v-on:click="onClosed()"></div> -->
        <div class="overlay"></div>
        <ProjectListModal class="modal-view" ref="projectModal" v-show="this.isProjectListMode" @onSelectProject="onSelectProject" @onClosed="onClosed"></ProjectListModal>
        <CareerInfoPreview class="modal-view" ref="preview" v-show="this.isPreviewMode" @onClosed="onClosed"></CareerInfoPreview>
      </div>
    </transition>
  </div>
</template>

<script>
import CareerInfoListView from '@/components/CareerInfoListView.vue'
import CareerInfoEditView from '@/components/CareerInfoEditView.vue'
import ProjectListModal from '@/components/ProjectListModal.vue'
import CareerInfoPreview from '@/components/CareerInfoPreview.vue'

export default {
  name: 'CareerSetting',
  components: {
    CareerInfoListView,
    CareerInfoEditView,
    ProjectListModal,
    CareerInfoPreview,
  },
  props: {
  },
  data() {
    return {
      userId: this.$utils.getUserId(),
      isEditMode: false,
      isPreviewMode: false,
      isProjectListMode: false,
      isModalShow: false,
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
    getCareerInfoList(page){
      var items = [];
      var vm = this;
      var offset = page * this.limit - this.limit
      this.$apiService.getCareerInfoList(this.userId, this.limit, offset, function(res) {
        if(res != null) {
          var data = JSON.parse(res.data);
          if (data.careerInfo.length) {
            data.careerInfo.forEach(info => {
              var career = {
                id: info.id,
                projectName: info.project_name,
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
      this.$message({type: 'success', message: '登録しました。'});
      this.setListMode();
    },
    onDelete(){
      this.$message({type: 'success', message: '削除しました。'});
      this.setListMode();
    },
    onEdit(record) {
      this.setEditMode(record.id, this.userId);
      this.$refs.refEdit.getMasterItem();
    },
    onPreview(record) {
      this.setPreviewMode(record.id);
    },
    onCancel(){
      this.setListMode();
    },
    add() {
      this.setEditMode(null, this.userId);
      this.$refs.refEdit.getMasterItem();
    },
    setListMode() {
      this.getCareerInfoList(1);
      this.isEditMode = false;
    },
    setEditMode(id) {
      this.$refs.refEdit.callApi(id, this.userId);
      this.isEditMode = true;
    },
    setPreviewMode(id) {
      this.isPreviewMode = true;
      this.isModalShow = true;
      this.$refs.preview.callApi(id);
    },
    showProjectList() {
      this.isModalShow = true;
      this.isProjectListMode = true;
    },
    onSelectProject(record) {
      this.isProjectListMode = false;
      this.isModalShow = false;
      this.isEditMode = true;
      this.$refs.refEdit.getMasterItem();
      this.$refs.refEdit.setInputFormfromProjectList(record, this.userId);
    },
    onClosed() {
      this.isEditMode = false;
      this.isPreviewMode = false;
      this.isProjectListMode = false;
      this.isModalShow = false;
    },
  }
}
</script>

<style scoped>
.add-btn {
  text-align: right;
  padding: 0.5rem;
}
</style>
