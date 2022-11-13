<template>
  <div class="user-info-edit-view">
    <div class="user-info-form">
      <el-form autocomplete="off">
        <div class="mail-address" v-if="this.isAdd">
          <el-form-item class="require" label="ID（メールアドレス）">
            <el-input v-model="form.mail_address"></el-input>
          </el-form-item>
        </div>

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

        <div class="authority">
          <el-form-item label="権限"></el-form-item>
          <el-radio v-model="form.authority" v-for="item in authorityOptions" :key="item.value" :value="item.value" :label="item.text" border></el-radio>
        </div>

        <div class="state" v-if="!this.isAdd">
          <el-form-item label="状態"></el-form-item>
          <el-radio v-model="form.state" v-for="item in stateOptions" :key="item.value" :value="item.value" :label="item.text" border></el-radio>
        </div>

      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserInfoEditView',
  components: {
  },
  props: {
    usesrId: null,
    isAdd: false,
  },
  data() {
    return{
      form: {
        mail_address: '',
        first_name_kana: '',
        last_name_kana: '',
        first_name: '',
        last_name: '',
        birthday: '',
        department: [],
        position: '',
        authority: '一般',
        state: '有効',
      },
      selectedDepartment: [],
      departmentOptions: [],
      authorityOptions: [
        {text: '管理者', value: 0},
        {text: '一般', value: 1},
      ],
      stateOptions: [
        {text: '有効', value: 1},
        {text: '停止', value: 0},
      ],
    }
  },
  beforeCreated() {
  },
  created() {
  },
  beforeMount() {
  },
  mounted() {
    this.callApi(this.usesrId);
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
    onRegistered(){
      this.$confirm('ユーザ情報を登録します。よろしいですか？', '確認', {
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
      var selecteds = this.selectedDepartment.map(function(department) {
        return vm.departmentOptions.filter(v => v.text == department).map(m => m.value).join(',');
      });
      var inputData = {
        'mail_address': this.form.mail_address,
        'password': null,
        'first_name_kana': this.form.first_name_kana,
        'last_name_kana': this.form.last_name_kana,
        'first_name': this.form.first_name,
        'last_name': this.form.last_name,
        'birthday': this.form.birthday,
        'department': selecteds,
        'position': this.form.position == '' ? null : this.form.position,
        'authority': this.authorityOptions.filter(v => v.text == this.form.authority)[0].value,
        'state': this.stateOptions.filter(v => v.text == this.form.state)[0].value,
      }

      if(this.usesrId == null) {
        var param = JSON.parse(JSON.stringify(inputData))
        this.$apiService.createUser(param, function(createRes) {
          if (createRes != null) {
            vm.$emit('onAddComplete')
          }
        });
      }
      else {
        var param = JSON.parse(JSON.stringify(inputData))
        this.$apiService.updateUserInfo(this.usesrId, param, (res) => {
          if(res != null) {
            vm.$emit('onUpdateComplete')
          }
        });
      }
    },
    callApi(id){
      var vm = this;
      if(!this.isAdd) {
        // 編集
        this.$apiService.getUserInfo(id, (res) => {
          if(res != null) {
            this.setForm(res, vm);
          }
        });
      }
    },
    getDepartment(){
      var vm = this;
      this.$apiService.getDepartmentList((res) => {
        if(res != null) {
          var department = [];
          if (Object.keys(res.data).length) department = JSON.parse(res.data);
          department.department.forEach(department => {
            vm.departmentOptions.push({text: department.name, value: department.id})
          });
        }
      })
    },
    setForm(res, vm){
      var userInfo = userInfo = JSON.parse(res.data);
      vm.form.first_name_kana = userInfo.first_name_kana;
      vm.form.last_name_kana = userInfo.last_name_kana;
      vm.form.first_name = userInfo.first_name;
      vm.form.last_name = userInfo.last_name;
      vm.form.position = userInfo.position;
      vm.form.birthday = vm.$utils.GetDate(userInfo.birthday);
      vm.form.authority = vm.authorityOptions.filter(v => v.value == userInfo.authority)[0].text;
      vm.form.state = vm.stateOptions.filter(v => v.value == userInfo.state)[0].text;

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
      this.form.authority = 'メンバー';
      this.form.state = '有効';
      this.selectedDepartment = [];
      this.departmentOptions = [];
    },
  }
}
</script>

<style scoped>
.mail-address, .password, .first-last-name .el-form-item {
  display: inline-block;
  min-width: 40%;
  padding-right: 2rem;
}

.department {
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