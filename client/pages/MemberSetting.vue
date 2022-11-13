<template>
  <div class="member-setting">
    <div class="title-label">
      <font-awesome-icon :icon="['fas', 'users-cog']" class="fa-2x" />
      <div>メンバー管理</div>
    </div>
    <div class="contents">
      <template v-if="isList">
        <div class="header">
          <el-button type="secondary" v-on:click="onAdd()">追加</el-button>
        </div>
        <UserInfoListView ref="refList" :limit="this.limit" @onEdit="onEdit" @getUserList="getUserList"></UserInfoListView>
      </template>
      <template v-if="isEdit">
        <div class="user-edit-view">
          <el-button type="secondary" v-on:click="onEditCancel($event)">キャンセル</el-button>
          <div class="edit-form">
            <div class="user-edit-btn-area">
              <div class="user-edit-registered-btn">
                <el-button type="secondary" v-on:click="onUpdate($event)">更新</el-button>
              </div>
            </div>
            <UserInfoEditView ref="userEdit" :usesrId="this.userId" :isAdd="false" @onUpdateComplete="onUpdateComplete"></UserInfoEditView>
            <div class="password-reset-btn">
              <el-button type="warning" v-on:click="onPasswordReset($event)">パスワード初期化</el-button>
            </div>
          </div>
        </div>
      </template>
      <template v-if="isAdd">
        <div class="add-view">
          <el-button type="secondary" v-on:click="onAddCancel($event)">キャンセル</el-button>
          <div class="add-form">
            <div class="user-add-btn-area">
              <div class="user-add-registered-btn">
                <el-button type="secondary" v-on:click="onRegistered($event)">登録</el-button>
              </div>
            </div>
            <UserInfoEditView ref="userAdd" :usesrId="null" :isAdd="true" @onAddComplete="onAddComplete"></UserInfoEditView>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
import Vue from 'vue'
import UserInfoListView from '@/components/UserInfoListView.vue'
import UserInfoEditView from '@/components/UserInfoEditView.vue'

export default {
  name: 'MemberSetting',
  components: {
    UserInfoListView,
    UserInfoEditView,
  },
  props: {
  },
  data() {
    return{
      userId: null,
      isEdit: false,
      isAdd: false,
      isList: true,
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
    this.setup(false, false);
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
    getUserList(page) {
      var vm = this;
      var offset = page * this.limit - this.limit
      this.$apiService.getUserInfoExcludeSelfList(this.limit, offset, function(res) {
        var users = [];
        if(res != null) {
          var data = JSON.parse(res.data);
          data.userInfoList.forEach(info => {
            var user = {
              id: info.id,
              name: info.last_name + ' ' + info.first_name,
              department: info.department.map(v => v.name).join('、'),
              position: info.position,
              authority: info.authority,
              state: info.state,
              lastLogin: vm.$utils.GetSlashDateTime(info.last_login),
            }
            users.push(user)
          });
          vm.$refs.refList.setPager(users, data.totalCount, page);
        }
      })
    },
    onAdd() {
      this.setup(true, false);
      this.setUserId(null);
      Vue.nextTick(() => {
        this.$refs.userAdd.getDepartment();
      });
    },
    onAddCancel() {
      this.setup(false, false);
    },
    onEditCancel() {
      this.setup(false, false);
    },
    onEdit(row) {
      this.setUserId(row.id);
      this.setup(false, true);
    },
    onUpdate(event) {
      this.$refs.userEdit.onRegistered(event);
    },
    onRegistered(event) {
      this.$refs.userAdd.onRegistered(event);
    },
    onPasswordReset() {
      this.$confirm('パスワードを初期化します。よろしいですか？', '確認', {
        confirmButtonText: 'OK',
        cancelButtonText: 'キャンセル',
        type: 'warning',
        center: true
      }).then(() => {
        var p = {}
        var param = JSON.parse(JSON.stringify(p));
        this.$apiService.resetPassword(this.userId, param, (res) => {
          if(res != null) {
            this.onPasswordResetComplete();
          }
        });
      }).catch(() => {

      });
    },
    onAddComplete() {
      this.$message({type: 'success', message: '登録しました。'});
      this.setup(false, false)
      this.setUserId(null);
    },
    onUpdateComplete() {
      this.$message({type: 'success', message: '登録しました。'});
      this.setup(false, false)
      this.setUserId(null);
    },
    onPasswordResetComplete() {
      this.$message({type: 'success', message: 'パスワードを初期化しました。'});
    },
    setUserId(id) {
      this.userId = id;
    },
    setup(isAdd, isEdit) {
      var isList = !isAdd && !isEdit;
      if(isList) {
        this.getUserList(1)
      }
      this.isList = isList
      this.isAdd = isAdd;
      this.isEdit = isEdit;
    },
  }
}
</script>

<style scoped>
.member-setting {
  display: block;
}

.member-setting .header {
  text-align: right;
  padding: 0.5rem;
}

.member-setting .member-table {
  /* position: absolute; */
  /* display: inline-block; */
  /* min-width: 30%; */
  /* padding: 0.5rem 2rem 0 0; */
}

.password-reset-btn {
  margin-top: 1rem;
  text-align: right;
  padding: 0.5rem;
}

.edit-form, .add-form {
  margin-top: 1rem;
  padding: 1rem;
  border: solid 1px #ced4da;
}

.member-table th:nth-child(1), .member-table td:nth-child(1) {
  display: none;
}

.member-table th:nth-child(2) {
  width: 5%;
}

.member-table td:nth-child(2), .member-table td:nth-child(6) {
  text-align: center;
  vertical-align: middle;
}

.member-table .custom-checkbox label {
  padding: 0;
}

.member-table th:nth-child(2) div, .member-table th:nth-child(6) div {
  visibility: hidden;
}

.member-table th:nth-child(4) {
  width: 20%;
}

.member-table th:nth-child(5) {
    width: 30%;
}
.member-table th:nth-child(6) {
  width: 10%;
}

.member-table td:nth-child(3), .member-table td:nth-child(4), .member-table td:nth-child(5) {
  vertical-align: middle;
}
</style>
