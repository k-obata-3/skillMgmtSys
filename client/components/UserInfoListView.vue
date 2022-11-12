<template>
  <div class="user-info-list-view">
    <el-table :data="this.list" style="width: 100%" stripe>
      <el-table-column prop="name" label="名前"></el-table-column>
      <el-table-column prop="department" label="部署"></el-table-column>
      <el-table-column prop="position" label="役職"></el-table-column>
      <el-table-column prop="lastLogin" label="最終ログイン" width="170"></el-table-column>
      <el-table-column prop="authority" width="50">
        <template slot-scope="scope">
          <div class="authority" v-show="scope.row.authority==0">
            <font-awesome-icon :icon="['fa', 'user-tie']" class="fa-2x" />
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="state" width="50">
        <template slot-scope="scope">
          <div class="state" v-show="scope.row.state==0">
            <font-awesome-icon :icon="['fa', 'ban']" class="fa-2x" />
          </div>
        </template>
      </el-table-column>
      <el-table-column width="100" align="center">
        <template slot-scope="scope">
          <el-button size="mini" @click="onEdit(scope.row)">編集</el-button>
        </template>
      </el-table-column>
    </el-table>
    <Pager ref="pager" :currentPage="this.currentPage" :limit="this.limit" :total="this.total" @changePage="changePage"></Pager>
  </div>
</template>

<script>
import Pager from '@/components/Pager.vue'

export default {
  name: 'UserInfoListView',
  components: {
    Pager,
  },
  props: {
    limit: Number,
  },
  data() {
    return{
      total: 0,
      list: [],
      currentPage: 1,
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
  methods: {
    onEdit(record) {
      this.$emit('onEdit', record);
    },
    changePage(page) {
      this.$emit('getUserList', page);
    },
    setPager(list, totalCount, page) {
      this.list = list;
      this.total = totalCount;
      this.$refs.pager.refreshPage(totalCount, page);
    }
  }
}
</script>

<style scoped>
.authority {
  text-align: center;
  color: #4682b4;
}
.state {
  text-align: center;
  color: #F56C6C;
}

</style>