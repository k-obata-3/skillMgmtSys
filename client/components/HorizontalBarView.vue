<template>
  <div class="horizontal-bar-view">
    <table>
      <template v-if="canShow">
        <tr v-for="(item, index) in barData" :key="index">
          <td>
            <el-tooltip placement="left-start" :content="item[0]" effect="light">
              <div>{{item[0]}}</div>
            </el-tooltip>
          </td>
            <td><div v-bind:style="setBarStyle(item[1])"></div></td>
            <td>{{item[1]}}</td>
        </tr>
      </template>
      <template v-if="!canShow">
        <tr>データが登録されていません</tr>
      </template>
    </table>
  </div>
</template>

<script>
export default {
  name: "HorizontalBarView",
  components: {
  },
  props: {
  },
  data() {
    return {
      barData: Object,
      canShow: false,
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
    updated(obj) {
      this.barData = obj;
      this.canShow = obj != null;
    },
    setBarStyle(num) {
      return {'max-width': `${num.toString()}rem`};
    },
  }
}
</script>

<style scoped>

table {
  width: 100%;
}

td {
  text-align: left;
}

tr td:nth-child(1) {
  width: 30%;
}

tr td:nth-child(1) div {
  width: 80%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

tr td:nth-child(2) {
  width: 40%;
}

tr td:nth-child(3) {
  width: 30%;
  padding-left: 1rem;
  text-align: right;
}

tr td:nth-child(2) div {
  background: steelblue;
  height: 1rem;
}

tr td:nth-child(3)::after {
  content: '年';
}
</style>
