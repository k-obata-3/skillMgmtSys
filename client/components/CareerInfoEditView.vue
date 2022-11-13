<template>
  <div class="career-info-edit-view">
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
    <div class="career-info-form">
      <el-form autocomplete="off">
        <el-form-item class="require" label="プロジェクト名">
          <el-input v-model="form.project_name"></el-input>
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
        <el-form-item>
          <div class="input-form-group">
            <div>機種</div>
            <el-button class="add-input-btn" v-on:click="addInput(modelInput)" size="mini" icon="el-icon-edit" circle></el-button>
          </div>
          <el-select v-model="modelInput[index]" v-for="(item, index) in modelInput" v-bind:key="index" clearable placeholder="選択してください">
            <el-option v-for="item in modelOptions" :key="item" :value="item"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <div class="input-form-group">
            <div>言語</div>
            <el-button class="add-input-btn" v-on:click="addInput(langInput)" size="mini" icon="el-icon-edit" circle></el-button>
          </div>
          <el-select v-model="langInput[index]" v-for="(item, index) in langInput" v-bind:key="index" clearable placeholder="選択してください">
            <el-option v-for="item in langOptions" :key="item" :value="item"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <div class="input-form-group">
            <div>DB</div>
            <el-button class="add-input-btn" v-on:click="addInput(dbInput)" size="mini" icon="el-icon-edit" circle></el-button>
          </div>
          <el-select v-model="dbInput[index]" v-for="(item, index) in dbInput" v-bind:key="index" clearable placeholder="選択してください">
            <el-option v-for="item in dbOptions" :key="item" :value="item"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <div class="input-form-group">
            <div>OS</div>
            <el-button class="add-input-btn" v-on:click="addInput(osInput)" size="mini" icon="el-icon-edit" circle></el-button>
          </div>
          <el-select v-model="osInput[index]" v-for="(item, index) in osInput" v-bind:key="index" clearable placeholder="選択してください">
            <el-option v-for="item in osOptions" :key="item" :value="item"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <div class="input-form-group">
            <div>フレームワーク</div>
            <el-button class="add-input-btn" v-on:click="addInput(frameworkInput)" size="mini" icon="el-icon-edit" circle></el-button>
          </div>
          <el-select v-model="frameworkInput[index]" v-for="(item, index) in frameworkInput" v-bind:key="index" clearable placeholder="選択してください">
            <el-option v-for="item in frameworkOptions" :key="item" :value="item"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <div class="input-form-group">
            <div>ツール</div>
            <el-button class="add-input-btn" v-on:click="addInput(toolInput)" size="mini" icon="el-icon-edit" circle></el-button>
          </div>
          <el-select v-model="toolInput[index]" v-for="(item, index) in toolInput" v-bind:key="index" clearable placeholder="選択してください">
            <el-option v-for="item in toolOptions" :key="item" :value="item"></el-option>
          </el-select>
        </el-form-item>
        <div class="in-charge">
          <el-form-item label="作業担当"></el-form-item>
          <el-checkbox-group class="checkbox-form" v-model="selectedInCharge">
            <el-checkbox v-for="item in inChargeOptions" v-bind:key="item.value" :label="item.text"></el-checkbox>
          </el-checkbox-group>
        </div>
        <div class="role">
          <el-form-item label="役割"></el-form-item>
          <el-checkbox-group class="checkbox-form" v-model="selectedRole">
            <el-checkbox v-for="item in roleOptions" v-bind:key="item.value" :label="item.text"></el-checkbox>
          </el-checkbox-group>
        </div>
        <el-form-item label="メモ">
          <el-input type="textarea" v-model="form.other" :rows="5"></el-input>
        </el-form-item>

        <div class="btn-area-bottom">
          <div class="delete-btn" v-show="this.careerId != null">
            <el-button type="danger" v-on:click="onDelete($event)">削除</el-button>
          </div>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  name: "CareerInfoEditView",
  components: {
  },
  props: {
      id: null,
  },
  data() {
    return {
      langInput: [],
      dbInput: [],
      osInput: [],
      frameworkInput: [],
      toolInput: [],
      modelInput: [],
      form: {
        project_name: null,
        overview: null,
        start_date: null,
        end_date: null,
        other: null,
      },
      modelOptions: [],
      osOptions: [],
      toolOptions: [],
      langOptions: [],
      dbOptions: [],
      frameworkOptions: [],
      inChargeOptions: [
        { text: "CN：コンサルテーション", value: 1 },
        { text: "SA：システム分析", value: 2 },
        { text: "SD：システム設計", value: 3 },
        { text: "PD：詳細設計", value: 4 },
        { text: "PG：プログラム製造", value: 5 },
        { text: "ST：システムテスト", value: 6 },
        { text: "OP：運用", value: 7 },
        { text: "その他", value: 8 },
      ],
      roleOptions: [
        { text: "PM：プロジェクトマネージャー", value: 1 },
        { text: "PL：プロジェクトリーダー", value: 2 },
        { text: "TL：チームリーダー", value: 3 },
      ],
      selectedInCharge: [],
      selectedRole: [],
      careerId: null,
      userId: null,
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
    getMasterItem(){
      var vm = this;
      this.$apiService.getMasterItemAllList((res) => {
        if(res != null) {
          var masterItem = [];
          if (Object.keys(res.data).length) masterItem = JSON.parse(res.data);
          vm.$utils.AddFormInput(vm.modelOptions, masterItem['model']);
          vm.$utils.AddFormInput(vm.osOptions, masterItem['os']);
          vm.$utils.AddFormInput(vm.toolOptions, masterItem['tool']);
          vm.$utils.AddFormInput(vm.langOptions, masterItem['language']);
          vm.$utils.AddFormInput(vm.dbOptions, masterItem['database']);
          vm.$utils.AddFormInput(vm.frameworkOptions, masterItem['framework']);
        }
      })
    },
    onDelete() {
      this.$confirm('経歴情報を削除します。よろしいですか？', '確認', {
        confirmButtonText: 'OK',
        cancelButtonText: 'キャンセル',
        type: 'warning',
        center: true
      }).then(() => {
        var vm = this;
        this.$apiService.deleteCareerInfo(this.careerId, function (res) {
          if (res != null) {
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
      this.$confirm('経歴情報を登録します。よろしいですか？', '確認', {
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
      let selectedIncharge = null;
      if(this.selectedInCharge.length != 0) {
        selectedIncharge = this.selectedInCharge.map(function(incharge) {
          return vm.inChargeOptions.filter(v => v.text == incharge).map(m => m.value).join();
        });
      }
      let selectedRole = null;
      if(this.selectedRole.length != 0) {
        selectedRole = this.selectedRole.map(function(role) {
          return vm.roleOptions.filter(v => v.text == role).map(m => m.value).join();
        });
      }

      var os = this.osInput.filter((v) => !!v).length == 0 ? null : this.osInput.filter((v) => !!v).map((item) => item).join(",");
      var db = this.dbInput.filter((v) => !!v).length == 0 ? null : this.dbInput.filter((v) => !!v).map((item) => item).join(",");
      var lang = this.langInput.filter((v) => !!v).length == 0 ? null : this.langInput.filter((v) => !!v).map((item) => item).join(",");
      var framework = this.frameworkInput.filter((v) => !!v).length == 0 ? null : this.frameworkInput.filter((v) => !!v).map((item) => item).join(",");
      var tool = this.toolInput.filter((v) => !!v).length == 0 ? null : this.toolInput.filter((v) => !!v).map((item) => item).join(",");
      var model = this.modelInput.filter((v) => !!v).length == 0 ? null : this.modelInput.filter((v) => !!v).map((item) => item).join(",");
      var incharge = selectedIncharge != null ? selectedIncharge.join() : null;
      var role = selectedRole != null ? selectedRole.join() : null;
      var projectName = this.form.project_name == "" ? null : this.form.project_name;
      var overview = this.form.overview == "" ? null : this.form.overview;
      var startDate = this.form.start_date == "" ? null : this.form.start_date;
      var endDate = this.form.end_date == "" ? null : this.form.end_date;
      var other = this.form.other == "" ? null : this.form.other;
      var data = {
        careerId: this.careerId,
        user: this.userId,
        project_name: projectName,
        overview: overview,
        start_date: startDate,
        end_date: endDate,
        os: os,
        database: db,
        language: lang,
        framework: framework,
        tool: tool,
        other: other,
        model: model,
        incharge: incharge,
        role: role,
      };
      let param = JSON.parse(JSON.stringify(data));
      if (this.careerId == null) {
        this.$apiService.createCareerInfo(param, function(createRes) {
          if (createRes != null) {
            // 親コンポーネントに onRegistered イベントを渡す
            vm.$emit("onRegistered");
          }
        });
      } else {
        this.$apiService.updateCareerInfo(param, function(updateRes) {
          if (updateRes != null) {
            // 親コンポーネントに onClosed イベントを渡す
            vm.$emit("onRegistered");
          }
        });
      }
    },
    callApi(id, userId) {
      this.clearInputForm();
      this.userId = userId;
      this.careerId = id;
      if (id == null) {
        return;
      }

      var vm = this;
      this.$apiService.getCareerInfo(vm.careerId, function (getRes) {
        if (getRes != null) {
          var careerInfo = [];
          if (Object.keys(getRes.data).length) {
            careerInfo = JSON.parse(getRes.data);
            vm.form.project_name = careerInfo.career_info.project_name;
            vm.form.overview = careerInfo.career_info.overview;
            vm.form.start_date = vm.$utils.GetDate(careerInfo.career_info.start_date);
            vm.form.end_date = vm.$utils.GetDate(careerInfo.career_info.end_date);
            vm.$utils.AddFormInput(vm.langInput, careerInfo.language);
            vm.$utils.AddFormInput(vm.dbInput, careerInfo.database);
            vm.$utils.AddFormInput(vm.osInput, careerInfo.os);
            vm.$utils.AddFormInput(vm.frameworkInput, careerInfo.framework);
            vm.$utils.AddFormInput(vm.toolInput, careerInfo.tool);
            vm.$utils.AddFormInput(vm.modelInput, careerInfo.model);
            if (careerInfo.incharge != null) {
              let selectedIncharge = careerInfo.incharge.map(function(incharge) {
                return vm.inChargeOptions.filter(v => v.value == incharge).map(m => m.text).join(',');
              });
              vm.selectedInCharge = selectedIncharge;
            }

            if (careerInfo.role != null) {
              let selectedRole = careerInfo.role.map(function(role) {
                return vm.roleOptions.filter(v => v.value == role).map(m => m.text).join(',');
              });
              vm.selectedRole = selectedRole;
            }
            vm.form.other = careerInfo.other;
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
      this.form.project_name = "";
      this.form.overview = "";
      this.form.other = "";
      this.form.start_date = "";
      this.form.end_date = "";
      this.langInput = [];
      this.dbInput = [];
      this.osInput = [];
      this.frameworkInput = [];
      this.toolInput = [];
      this.modelInput = [];
      this.selectedInCharge = [];
      this.selectedRole = [];
      this.langOptions = [],
      this.modelOptions = [],
      this.osOptions = [],
      this.toolOptions = [],
      this.dbOptions = [],
      this.frameworkOptions = [],
      this.careerId = null;
    },
    setInputFormfromProjectList(item, userId) {
      this.userId = userId;
      this.careerId = null;
      this.form.project_name = item.projectName;
      this.form.overview = item.overview;
      this.form.start_date = this.$utils.GetDate(item.startDate);
      this.form.end_date = this.$utils.GetDate(item.endDate);
    }
  },
};
</script>

<style scoped>
.career-info-form {
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

.career-info-form div {
  padding: 0.3rem;
}

.in-charge,
.career-info-edit-view .role {
  max-width: 80%;
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