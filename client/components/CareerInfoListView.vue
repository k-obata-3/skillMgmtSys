<template>
  <div class="career-info-list-view">
    <el-table :data="this.list" style="width: 100%" stripe>
      <el-table-column prop="projectName" label="プロジェクト名"></el-table-column>
      <el-table-column prop="overview" label="概要"></el-table-column>
      <el-table-column prop="startDate" label="開始日"></el-table-column>
      <el-table-column prop="endDate" label="終了日"></el-table-column>
      <el-table-column width="150" align="center">
        <template slot-scope="scope">
          <el-button size="mini" @click="onEdit(scope.row)">編集</el-button>
          <el-button size="mini" @click="onPreview(scope.row)">詳細</el-button>
        </template>
      </el-table-column>
    </el-table>
    <Pager ref="pager" :currentPage="this.currentPage" :limit="this.limit" :total="this.total" @changePage="changePage"></Pager>
  </div>
</template>

<script>
import Pager from '@/components/Pager.vue'

export default {
  name: 'CareerInfoListView',
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
    onPreview(record) {
      this.$emit('onPreview', record);
    },
    changePage(page) {
      this.$emit('getCareerInfoList', page);
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

</style>