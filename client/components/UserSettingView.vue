<template>
  <div class="user-setting-view">
    <div class="user-setting-form">
      <template>
        <el-tabs type="card" @tab-click="tabClick" value="userSetting">
          <el-tab-pane label="個人設定" name="userSetting"></el-tab-pane>
          <el-tab-pane label="パスワード変更" name="passChange"></el-tab-pane>
        </el-tabs>
      </template>

      <div v-if="this.isUserSetting">
        <div class="user-edit-btn-area">
          <div class="user-edit-registered-btn">
            <el-button type="secondary" v-on:click="onUpdate($event)">更新</el-button>
          </div>
        </div>
        <el-form autocomplete="off">
          <div class="first-last-name">
            <el-form-item class="require" label="姓（カナ）">
              <el-input v-model="form.last_name_kana"></el-input>
            </el-form-item>

            <el-form-item class="require" label="名（カナ）">
              <el-input v-model="form.first_name_kana"></el-input>
            </el-form-item>
          </div>

          <div class="first-last-name">
            <el-form-item class="require" label="姓">
              <el-input v-model="form.last_name"></el-input>
            </el-form-item>

            <el-form-item class="require" label="名">
              <el-input v-model="form.first_name"></el-input>
            </el-form-item>
          </div>

          <div class="birthday">
            <el-form-item class="require" label="生年月日">
              <el-date-picker v-model="form.birthday" type="date" format="yyyy/MM/dd " value-format="yyyy-MM-dd"></el-date-picker>
            </el-form-item>
          </div>

          <div class="department">
            <el-form-item label="部署"></el-form-item>
            <el-checkbox-group class="checkbox-form" v-model="selectedDepartment">
              <el-checkbox v-for="item in departmentOptions" v-bind:key="item.value" :label="item.text"></el-checkbox>
            </el-checkbox-group>
          </div>

          <div class="position">
            <el-form-item label="役職">
              <el-input v-model="form.position"></el-input>
            </el-form-item>
          </div>
        </el-form>
      </div>

      <div v-if="!this.isUserSetting">
        <div class="user-edit-btn-area">
          <div class="user-edit-registered-btn">
            <el-button type="secondary" v-on:click="onPasswordChange($event)">変更</el-button>
          </div>
        </div>
        <el-form autocomplete="off">
          <div class="pass-change-form">
            <el-form-item class="require" label="現在のパスワード">
              <el-input v-model="passChangeform.currentPassword"></el-input>
            </el-form-item>

            <el-form-item class="require" label="新しいパスワード">
              <el-input v-model="passChangeform.newPassword"></el-input>
            </el-form-item>
          </div>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserInfoEditView',
  components: {
  },
  data() {
    return{
      form: {
        first_name_kana: '',
        last_name_kana: '',
        first_name: '',
        last_name: '',
        birthday: '',
        department: [],
        position: '',
      },
      selectedDepartment: [],
      departmentOptions: [],
      passChangeform: {
        currentPassword: null,
        newPassword: null,
      },
      isUserSetting: true,
    }
  },
  beforeCreated() {
  },
  created() {
  },
  beforeMount() {
  },
  mounted() {
    this.callApi();
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
    tabClick(tab, event) {
      if(tab['name'] == 'userSetting') {
        this.isUserSetting = true;
      } else {
        this.isUserSetting = false;
      }
      this.clearPassChangeForm();
    },
    onUpdate(event){
      this.$confirm('ユーザ情報を更新します。よろしいですか？', '確認', {
        confirmButtonText: 'OK',
        cancelButtonText: 'キャンセル',
        type: 'warning',
        center: true
      }).then(() => {
        var vm = this;
        var selecteds = this.selectedDepartment.map(function(department) {
          return vm.departmentOptions.filter(v => v.text == department).map(m => m.value).join(',');
        });
        var inputData = {
          'first_name_kana': this.form.first_name_kana,
          'last_name_kana': this.form.last_name_kana,
          'first_name': this.form.first_name,
          'last_name': this.form.last_name,
          'birthday': this.form.birthday,
          'department': selecteds,
          'position': this.form.position == '' ? null : this.form.position,
        }

        var param = JSON.parse(JSON.stringify(inputData))
        this.$apiService.updateLoginUserInfo(param, (res) => {
          if(res != null) {
            this.$message({type: 'success', message: '更新しました。'});
          }
        });
      }).catch(() => {

      });
    },
    onPasswordChange(event){
      this.$confirm('パスワードを変更します。よろしいですか？', '確認', {
        confirmButtonText: 'OK',
        cancelButtonText: 'キャンセル',
        type: 'warning',
        center: true
      }).then(() => {
        var p = {
          'current_password': this.$utils.getHashText(this.passChangeform.currentPassword),
          'new_password': this.$utils.getHashText(this.passChangeform.newPassword),
        }
        var param = JSON.parse(JSON.stringify(p));
        this.$apiService.updatePassword(param, (res) => {
          if(res != null) {
            this.$message({type: 'success', message: '変更しました。'});
            this.clearPassChangeForm();
          }
        });
      }).catch(() => {

      });
    },
    callApi(){
      var vm = this;
      this.$apiService.getLoginUserInfo((res) => {
        if(res != null) {
          this.setForm(res, vm);
        }
      });
    },
    setForm(res, vm){
      var userInfo = userInfo = JSON.parse(res.data);
      vm.form.first_name_kana = userInfo.first_name_kana;
      vm.form.last_name_kana = userInfo.last_name_kana;
      vm.form.first_name = userInfo.first_name;
      vm.form.last_name = userInfo.last_name;
      vm.form.position = userInfo.position;
      vm.form.birthday = vm.$utils.GetDate(userInfo.birthday);

      userInfo.department.forEach(department => {
        vm.departmentOptions.push({text: department.name, value: department.id})
        if(department.selected) {
            vm.selectedDepartment.push(department.name)
        }
      });
    },
    clearForm(){
      this.form.first_name_kana = '';
      this.form.last_name_kana = '';
      this.form.first_name = '';
      this.form.last_name = '';
      this.form.birthday = '';
      this.form.department = [];
      this.form.position = '';
      this.selectedDepartment = [];
      this.departmentOptions = [];
    },
    clearPassChangeForm() {
      this.passChangeform.currentPassword = null;
      this.passChangeform.newPassword = null;
    }
  }
}
</script>

<style scoped>
.first-last-name .el-form-item {
  display: inline-block;
  min-width: 40%;
  padding-right: 2rem;
}

.department, .pass-change-form {
  width: calc(80% + 2rem);
}

.position {
  display: inline-block;
  min-width: 40%;
}

.birthday {
  display: inline-block;
}

</style>