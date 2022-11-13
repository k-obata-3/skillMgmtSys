<template>
  <div class="master-setting-view">
    <template>
      <el-tabs type="card" @tab-click="tabClick" value="department">
        <el-tab-pane label="部署" name="department"></el-tab-pane>
        <el-tab-pane label="言語" name="language"></el-tab-pane>
        <el-tab-pane label="データベース" name="database"></el-tab-pane>
        <el-tab-pane label="フレームワーク" name="framework"></el-tab-pane>
        <el-tab-pane label="OS" name="os"></el-tab-pane>
        <el-tab-pane label="機種" name="model"></el-tab-pane>
        <el-tab-pane label="ツール" name="tool"></el-tab-pane>
      </el-tabs>
    </template>
    <div class="input-form">
        <div class="item-input">
            <el-input v-model="form.name"></el-input>
        </div>
        <div class="form-btn">
          <el-button type="secondary" v-on:click="onRegistered($event)">登録</el-button>
        </div>
    </div>
    <div class="cancel-btn">
      <el-button v-on:click="onCancel($event)" :disabled="!this.isEditing">キャンセル</el-button>
    </div>
    <div class="master-table">
        <el-table :data="this.list" max-height="520" border stripe>
          <el-table-column prop="name" :label="this.selectTabLabel"></el-table-column>
          <el-table-column width="160" align="center">
            <template slot-scope="scope">
              <el-button size="mini" @click="onEdit(scope.row)" :disabled="scope.row.isEditing">編集</el-button>
              <el-button size="mini" type="danger" @click="onDelete(scope.row)" :disabled="scope.row.isEditing">削除</el-button>
            </template>
          </el-table-column>
        </el-table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MasterSettingView',
  components: {

  },
  props: {
    limit: Number,
  },
  data() {
    return{
      isEditing: false,
      selectTabLabel: "部署",
      selectTabName: "department",
      selectItemId: null,
      list: [],
      form: {
        name: '',
      },
    }
  },
  beforeCreated() {
  },
  created() {
  },
  beforeMount() {
  },
  mounted() {
    this.refresh();
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
      this.selectTabLabel = tab['label'];
      this.selectTabName = tab['name'];
      this.refresh();
    },
    onCancel() {
      this.isEditing = false;
      this.list.forEach(item => {
        item.isEditing = this.isEditing;
      });
      this.form.name = '';
      this.selectItemId = null;
    },
    onEdit(row) {
      this.isEditing = true;
      this.list.forEach(item => {
        item.isEditing = this.isEditing;
      });
      this.selectItemId = row.id;
      this.form.name = row.name;
    },
    onRegistered() {
      if(this.form.name.trim() == '') return;

      var msg;
      if(this.selectTabName == 'department') {
        msg = "部署";
      } else {
        msg = "マスタ項目";
      }

      this.$confirm(msg + '情報を登録します。よろしいですか？', '確認', {
        confirmButtonText: 'OK',
        cancelButtonText: 'キャンセル',
        type: 'warning',
        center: true
      }).then(() => {
        this.callRegisterApi();
      }).catch(() => {

      });
    },
    onDelete(row) {
      var delItemName = row.name.length > 10 ? (row.name).slice(0, 10)+"..." : row.name;
      this.$confirm('「' + delItemName + '」' + 'を削除します。よろしいですか？', '確認', {
        confirmButtonText: 'OK',
        cancelButtonText: 'キャンセル',
        type: 'warning',
        center: true
      }).then(() => {
        this.callDeleteApi(row);
      }).catch(() => {

      });
      this.refresh();
    },
    callRegisterApi() {
      var name = this.form.name == "" ? null : this.form.name;
      var data = {
        id: this.selectItemId,
        key: this.selectTabName,
        name: name,
      };
      let param = JSON.parse(JSON.stringify(data));
      if(this.selectTabName == 'department') {
        this.createDepartment(param);
      } else {
        this.createMasterItem(param);
      }
    },
    callDeleteApi(row) {
      if(this.selectTabName == 'department') {
        this.deleteDepartment(row);
      } else {
        this.deleteMasterItem(row);
      }
    },
    refresh() {
      this.list = [];
      if(this.selectTabName == 'department') {
        this.getDepartment();
      } else {
        this.getMasterItem(this.selectTabName);
      }

      this.selectItemId = null;
      this.form.name = ''
      this.isEditing = false;
    },
    getDepartment(){
      var vm = this;
      this.$apiService.getDepartmentList((res) => {
        if(res != null) {
          var department = [];
          if (Object.keys(res.data).length) department = JSON.parse(res.data);
          department.department.forEach(department => {
            vm.list.push({id: department.id, name: department.name, isEditing: false})
          });
        }
      })
    },
    getMasterItem(key){
      if(key == null) return;

      var vm = this;
      this.$apiService.getMasterItemList(key, (res) => {
        if(res != null) {
          var masterItem = [];
          if (Object.keys(res.data).length) masterItem = JSON.parse(res.data);
          masterItem.forEach(masterItem => {
            vm.list.push({id: masterItem.id, name: masterItem.name, isEditing: false})
          });
        }
      })
    },
    createMasterItem(param) {
      var vm = this;
      this.$apiService.createMasterItem(param, function(createRes) {
        if(createRes != null) {
          vm.$message({type: 'success', message: '登録しました。'});
          vm.refresh();
        }
      }).then(() => {

      }).catch(() => {

      });
    },
    createDepartment(param) {
      var vm = this;
      this.$apiService.createDepartment(param, function(createRes) {
        if(createRes != null) {
          vm.$message({type: 'success', message: '登録しました。'});
          vm.refresh();
        }
      }).then(() => {

      }).catch(() => {

      });
    },
    deleteMasterItem(row) {
      var vm = this;
      this.$apiService.deleteMasterItem(row.id, function (res) {
        if(res != null) {
          vm.$message({type: 'success', message: '削除しました。'});
          vm.refresh();
        }
      }).then(() => {

      }).catch(() => {

      });
    },
    deleteDepartment(row) {
      var vm = this;
      this.$apiService.deleteDepartment(row.id, function (res) {
        if(res != null) {
          vm.$message({type: 'success', message: '削除しました。'});
          vm.refresh();
        }
      }).then(() => {

      }).catch(() => {

      });
    },
  }
}
</script>

<style scoped>
.master-table, .input-form, .cancel-btn {
  min-width: 400px;
  width: 50%;
}

.cancel-btn {
  text-align: right;
  padding-top: 1rem;
  padding-bottom: 1rem;
}

.input-form {
  padding-left: 1rem;
  padding-top: 2rem;
}

.item-input {
  display: inline-block;
  width: 50%;
  padding-right: 1rem;
}

.form-btn {
  display: inline-block;
}


.career-info-table tbody tr {
  cursor: pointer;
}

.btn-area-top-left, .btn-area-top-right {
  min-width: calc(50% - 1rem);
  display: inline-block;
}

.add-btn {
  text-align: right;
  padding: 0.5rem;
}
</style>