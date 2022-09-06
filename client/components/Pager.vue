<template>
  <div class="pager">
    <div class="mt-3">
      <el-pagination
        ref="pagination"
        background
        layout="prev, pager, next"
        @current-change="changePage"
        :total="totalCount"
        :page-size="limitCount"
        :current-page.sync="currentPageVal">
      </el-pagination>
    </div>
  </div>
</template>

<script>
export default {
  name: "Pager",
  components: {
  },
  props: {
    total: Number,
    limit: Number,
    currentPage: Number,
  },
  data() {
    return {
      currentPageVal: this.currentPage,
      totalCount: this.total,
      limitCount: this.limit,
    }
  },
  computed: {
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
    changePage(page) {
      // console.log(page)
      // 親コンポーネントに changePage イベントを渡す
      this.$emit('changePage', page);
    },
    refreshPage(total, page) {
      this.currentPageVal = page;
      this.totalCount = total;
    },
  },
}
</script>

<style scoped>

</style>
