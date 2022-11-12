<template>
  <div class="project-list-view">
    <el-table :data="this.list" style="width: 100%" stripe>
      <el-table-column prop="projectName" label="プロジェクト名"></el-table-column>
      <el-table-column prop="overview" label="概要"></el-table-column>
      <el-table-column prop="startDate" label="開始日"></el-table-column>
      <el-table-column prop="endDate" label="終了日"></el-table-column>
      <el-table-column width="100" align="center" v-if="this.isEdit">
        <template slot-scope="scope">
          <el-button size="mini" @click="onEdit(scope.row)">編集</el-button>
        </template>
      </el-table-column>
      <el-table-column width="100" align="center" v-if="!this.isEdit">
        <template slot-scope="scope">
          <el-button size="mini" @click="onSelectProject(scope.row)">選択</el-button>
        </template>
      </el-table-column>
    </el-table>
    <Pager ref="pager" :currentPage="this.currentPage" :limit="this.limit" :total="this.total" @changePage="changePage"></Pager>
  </div>
</template>

<script>
import Pager from '@/components/Pager.vue'

export default {
  name: 'ProjectListView',
  components: {
    Pager,
  },
  props: {
    limit: Number,
    isEdit: Boolean,
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
    onSelectProject(record) {
      this.$emit('onSelectProject', record);
    },
    onEdit(record) {
      this.$emit('onEdit', record);
    },
    changePage(page) {
      this.$emit('getProjectList', page);
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