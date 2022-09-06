<template>
  <div class="career-info-graph-view">
    <div>
      <template>
        <!-- <div>技術シェア</div> -->
        <div class="chart-1">
          <div class="chart-title">言語</div>
          <DoughnutChart1 class="chart" ref="chart1" :chartLabel="lang_labels" :chartData="lang_datas"></DoughnutChart1>
          <div class="chart-item-list">
            <div v-for="(item, index) in this.langList" v-bind:key="index">
              <p>{{item.name}}</p>
              <p>{{getLangRatio(item.value)}}</p>
            </div>
          </div>
        </div>
        <div class="chart-2">
          <div class="chart-title">データべ－ス</div>
          <DoughnutChart2 class="chart" ref="chart2" :chartLabel="db_labels" :chartData="db_datas"></DoughnutChart2>
          <div class="chart-item-list">
            <div v-for="(item, index) in this.dbList" v-bind:key="index">
              <p>{{item.name}}</p>
              <p>{{getDbRatio(item.value)}}</p>
            </div>
          </div>
        </div>
        <div class="chart-3">
          <div class="chart-title">フレームワーク</div>
          <DoughnutChart3 class="chart" ref="chart3" :chartLabel="framework_labels" :chartData="framework_datas"></DoughnutChart3>
          <div class="chart-item-list">
            <div v-for="(item, index) in this.frameworkList" v-bind:key="index">
              <p>{{item.name}}</p>
              <p>{{getFrameworkRatio(item.value)}}</p>
            </div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
import DoughnutChart1 from "@/components/DoughnutChart.vue";
import DoughnutChart2 from "@/components/DoughnutChart.vue";
import DoughnutChart3 from "@/components/DoughnutChart.vue";

export default {
  name: "CareerInfoGraphView",
  components: {
    DoughnutChart1,
    DoughnutChart2,
    DoughnutChart3,
  },
  props: {},
  data() {
    return {
      db_labels: [],
      db_datas: [],
      lang_labels: [],
      lang_datas: [],
      framework_labels: [],
      framework_datas: [],
      langList: [],
      dbList: [],
      frameworkList: [],
    };
  },
  beforeCreated() {},
  created() {},
  beforeMount() {},
  mounted() {
    this.callApi();
  },
  beforeUpdate() {},
  updated() {},
  beforeDestroy() {},
  destroyed() {},
    methods: {
      callApi() {
        var vm = this;
        this.$apiService.getCareerInfoAllList(this.$utils.getCompanyId(), (res) => {
          if (res != null) {
            var list = [];
            if (Object.keys(res.data).length) {
              list = JSON.parse(res.data);
            }

            var langDic = vm.$utils.splitPythonDic(list.career_info_lang);
            vm.langList = Array(langDic.length);
            langDic.forEach((x, index) => {
              var val = x.split(":");
              vm.langList[index] = { name: val[0], value: parseInt(val[1]) }
            });

            var dbDic = vm.$utils.splitPythonDic(list.career_info_db);
            vm.dbList = Array(dbDic.length);
            dbDic.forEach((x, index) => {
              var val = x.split(":");
              vm.dbList[index] = { name: val[0], value: parseInt(val[1]) }
            });

            var frameworkDic = vm.$utils.splitPythonDic(list.career_info_framework);
            vm.frameworkList = Array(frameworkDic.length);
            frameworkDic.forEach((x, index) => {
              var val = x.split(":");
              vm.frameworkList[index] = { name: val[0], value: parseInt(val[1]) }
            });

            vm.langList.slice(0, 5).forEach((x) => {
              vm.lang_labels.push(x['name']);
              vm.lang_datas.push(x['value']);
            });

            vm.dbList.slice(0, 5).forEach((x) => {
              vm.db_labels.push(x['name']);
              vm.db_datas.push(x['value']);
            });

            vm.frameworkList.slice(0, 5).forEach((x) => {
              vm.framework_labels.push(x['name']);
              vm.framework_datas.push(x['value']);
            });

            vm.$refs.chart1.draw();
            vm.$refs.chart2.draw();
            vm.$refs.chart3.draw();
          }
        });
      },
      getLangRatio(num) {
        var total = this.langList.reduce(function(sum, el){
          return sum + el.value;
        }, 0);

        return String(Math.round(num / total * 100)) + '%';
      },
      getDbRatio(num) {
        var total = this.dbList.reduce(function(sum, el){
          return sum + el.value;
        }, 0);

        return String(Math.round(num / total * 100)) + '%';
      },
      getFrameworkRatio(num) {
        var total = this.frameworkList.reduce(function(sum, el){
          return sum + el.value;
        }, 0);

        return String(Math.round(num / total * 100)) + '%';
      },
    },
};
</script>

<style scoped>
.career-info-graph-view {
  /* display: flex; */
  /* justify-content: center; */
  /* align-items: center; */
}

.chart-1,
.chart-2,
.chart-3 {
  display: inline-block;
  border: solid 1px #ced4da;
  margin: 1rem;
  width: calc(50% - 3rem);
}

.chart {
  display: inline-block;
  padding-top: 0.5rem;
  padding-right: 0.5rem;
  padding-left: 0.5rem;
  width: 45%;
  height: 250px;
  justify-content: center;
  align-items: center;
}

.chart-item-list {
  display: inline-block;
  width: 45%;
  height: 245px;
  overflow-y: scroll;
}

.chart-item-list div {
  height: 2rem;
}

.chart-item-list p {
  display: inline-block;
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow: hidden;
}
.chart-item-list p:nth-child(1) {
  width: calc(90% - 50px);
}
.chart-item-list p:nth-child(2) {
  width: 50px;
}

.chart-title {
    width: 90%;
    margin-left: 5%;
    padding-top: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: solid 1px steelblue;
}
</style>
