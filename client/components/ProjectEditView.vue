<template>
  <div class="project-info-edit-view">
    <div class="btn-area-top-left">
      <div class="cancel-btn">
        <el-button type="secondary" v-on:click="onCancel($event)">キャンセル</el-button>
      </div>
    </div>
    <div class="btn-area-top-right">
      <div class="registered-btn">
        <el-button type="secondary" v-on:click="onRegistered($event)">登録</el-button>
      </div>
    </div>
    <div class="project-info-form">
      <el-form autocomplete="off">
        <el-form-item class="require" label="プロジェクト名">
          <el-input v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="概要">
          <el-input v-model="form.overview"></el-input>
        </el-form-item>
        <div class="start-end-date">
          <el-form-item label="開始日">
            <el-date-picker v-model="form.start_date" type="date" format="yyyy/MM/dd " value-format="yyyy-MM-dd"></el-date-picker>
          </el-form-item>

          <el-form-item label="終了日">
            <el-date-picker v-model="form.end_date" type="date" format="yyyy/MM/dd " value-format="yyyy-MM-dd"></el-date-picker>
          </el-form-item>
        </div>
        <div class="btn-area-bottom">
          <div class="delete-btn" v-show="this.projectId != null">
            <el-button type="danger" v-on:click="onDelete($event)">削除</el-button>
          </div>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  name: "ProjectInfoEditView",
  components: {},
  props: {
      id: null,
  },
  data() {
    return {
      form: {
        name: null,
        overview: null,
        start_date: null,
        end_date: null,
      },
      projectId: null,
    };
  },
  beforeCreated() {},
  created() {},
  beforeMount() {},
  mounted() {},
  beforeUpdate() {},
  updated() {},
  beforeDestroy() {},
  destroyed() {},
  methods: {
    onDelete() {
      this.$confirm('案件情報を削除します。よろしいですか？', '確認', {
        confirmButtonText: 'OK',
        cancelButtonText: 'キャンセル',
        type: 'warning',
        center: true
      }).then(() => {
        var vm = this;
        this.$apiService.deleteProject(this.projectId, function (res) {
          if (res != null) {
            vm.$message({type: 'success', message: '削除しました。'});
            // 親コンポーネントに onDelete イベントを渡す
            vm.$emit("onDelete");
          }
        });
      }).catch(() => {

      });
    },
    onCancel() {
      // 親コンポーネントに onCancel イベントを渡す
      this.$emit("onCancel");
    },
    onRegistered() {
      this.$confirm('案件情報を登録します。よろしいですか？', '確認', {
        confirmButtonText: 'OK',
        cancelButtonText: 'キャンセル',
        type: 'warning',
        center: true
      }).then(() => {
        this.callRegisterApi();
      }).catch(() => {

      });
    },
    callRegisterApi() {
      var vm = this;

      var name = this.form.name == "" ? null : this.form.name;
      var overview = this.form.overview == "" ? null : this.form.overview;
      var startDate = this.form.start_date == "" ? null : this.form.start_date;
      var endDate = this.form.end_date == "" ? null : this.form.end_date;
      var data = {
        project_id: this.projectId,
        name: name,
        overview: overview,
        start_date: startDate,
        end_date: endDate,
      };
      let param = JSON.parse(JSON.stringify(data));
      if (this.projectId == null) {
        this.$apiService.createProject(param, function(createRes) {
          if (createRes != null) {
            vm.$message({type: 'success', message: '登録しました。'});
            // 親コンポーネントに onRegistered イベントを渡す
            vm.$emit("onRegistered");
          }
        });
      } else {
        this.$apiService.updateProject(param, function(updateRes) {
          if (updateRes != null) {
            vm.$message({type: 'success', message: '登録しました。'});
            // 親コンポーネントに onClosed イベントを渡す
            vm.$emit("onRegistered");
          }
        });
      }
    },
    callApi(id, companyId) {
      this.clearInputForm();
      this.companyId = companyId;
      this.projectId = id;
      if (id == null) {
        return;
      }

      var vm = this;
      this.$apiService.getProjectInfo(id, function (getRes) {
        if (getRes != null) {
          var project = [];
          if (Object.keys(getRes.data).length) {
            project = JSON.parse(getRes.data);
            vm.form.name = project.name;
            vm.form.overview = project.overview;
            vm.form.start_date = vm.$utils.GetDate(project.start_date);
            vm.form.end_date = vm.$utils.GetDate(project.end_date);
          }
        }
      });
    },
    addInput(object) {
      if (object.length >= 5) {
        return;
      }
      object.push("");
    },
    clearInputForm() {
      this.form.name = "";
      this.form.overview = "";
      this.form.other = "";
      this.form.start_date = "";
      this.form.end_date = "";
      this.projectId = null;
    },
  },
};
</script>

<style scoped>
.project-info-form {
}

.add-input {
  display: inline-block;
  max-width: 10rem;
  margin-left: 0.5rem;
  margin-bottom: 0.5rem;
}

.input-form-group div {
  display: inline-block;
}

.project-info-form div {
  padding: 0.3rem;
}

.start-end-date > fieldset {
  display: inline-block;
  padding-right: 2rem;
}

.btn-area-top-left,
.btn-area-top-right {
  min-width: calc(50% - 0.5rem);
  display: inline-block;
}

.registered-btn,
.delete-btn {
  text-align: right;
}

.cancel-btn {
  text-align: left;
  padding: 0.5rem;
}
</style>