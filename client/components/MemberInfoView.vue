<template>
  <div class="member-info-view">
    <div class="member-info-title">
      <div class="title-label">
        <font-awesome-icon :icon="['fas', 'user']" class="fa-2x" />
        <div>詳細情報</div>
      </div>
    </div>
    <div class="modal-closed-button">
      <el-button type="secondary" v-on:click="onClosed($event)">閉じる</el-button>
    </div>
    <div class="member-info">
      <div class="member-info-row">
        <div class="title">名前</div>
        <div>{{this.first_name}}&nbsp;{{this.last_name}}</div>
        <div id="downloadBtn" v-show="this.$utils.getUserId() == this.userId || this.$utils.getAuth() == 0">
          <el-button type="" icon="el-icon-download" circle size="small" v-on:click="output()" v-loading.fullscreen.lock="downloadLoading"></el-button>
        </div>
      </div>
      <div class="member-info-row">
        <div class="title">年齢</div>
        <div>{{this.age}}</div>
      </div>
      <div class="member-info-row">
        <div class="title">部署</div>
        <div>{{this.department}}</div>
      </div>
      <div class="member-info-row">
        <div class="title">役職</div>
        <div>{{this.position}}</div>
      </div>
    </div>
    <div class="chart-area">
      <div class="chart-div">
        <div class="chart-1">
          <div class="chart-title">言語</div>
          <HorizontalBarView1 ref="barView1"></HorizontalBarView1>
        </div>
      </div>
        <div class="chart-div">
          <div class="chart-2">
            <div class="chart-title">データべ－ス</div>
            <HorizontalBarView2 ref="barView2"></HorizontalBarView2>
          </div>
        </div>
        <div class="chart-div">
          <div class="chart-3">
            <div class="chart-title">フレームワーク</div>
            <HorizontalBarView3 ref="barView3"></HorizontalBarView3>
          </div>
        </div>
    </div>
  </div>
</template>

<script>
import HorizontalBarView1 from '@/components/HorizontalBarView.vue';
import HorizontalBarView2 from '@/components/HorizontalBarView.vue';
import HorizontalBarView3 from '@/components/HorizontalBarView.vue';

export default {
  name: 'MemberInfoView',
  components: {
    HorizontalBarView1,
    HorizontalBarView2,
    HorizontalBarView3,
  },
  props: {
  },
  data() {
    return{
      first_name: '',
      last_name: '',
      age: '',
      department: '',
      position: '',
      userId: null,
      downloadLoading: false,
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
    onRefresh(item) {
      this.userId = item.userInfo.id;
      this.first_name = item.first_name;
      this.last_name = item.last_name;
      this.age = item.userInfo.age;
      this.department = item.department;
      this.position = item.position;
      var vm = this;

      this.$apiService.getCareerInfoDic(this.userId, function(res) {
        if(res != null) {
          var data = JSON.parse(res.data);
          if(data.career_info_dic != null) {
            var langVal = vm.$utils.splitPythonDic(data.career_info_dic.career_info_lang);
            var dbVal = vm.$utils.splitPythonDic(data.career_info_dic.career_info_db);
            var frameworkVal = vm.$utils.splitPythonDic(data.career_info_dic.career_info_framework);

            var langMap = vm.$utils.createChartMapData(langVal);
            var dbMap = vm.$utils.createChartMapData(dbVal);
            var frameworkMap = vm.$utils.createChartMapData(frameworkVal);

            vm.$refs.barView1.updated(langMap);
            vm.$refs.barView2.updated(dbMap);
            vm.$refs.barView3.updated(frameworkMap);
          }
        }
      });
    },
    onClosed() {
      this.onClear();
      // 親コンポーネントに onClosed イベントを渡す
      this.$emit('onClosed');
    },
    onClear() {
      this.userId = null;
    },
    output() {
      this.$confirm('経歴情報をダウンロードします。よろしいですか？', '確認', {
        confirmButtonText: 'OK',
        cancelButtonText: 'キャンセル',
        type: 'warning',
        center: true
      }).then(() => {
        this.downloadLoading = true;
        this.$apiService.outputCareerInfo(this.userId, () => {
          this.downloadLoading = false;
        })
      }).catch(() => {

      });
    },
  }
}
</script>

<style scoped>
.member-info-view {
  overflow: scroll;
  padding-top: 2rem;
  padding-bottom: 2rem;
}

#skill-sheet-output {
  margin-left: 2rem;
}

.member-info-title {
  width: 90%;
  margin-left: 5%;
  display: inline-block;
}

.member-info {
  width: 80%;
  margin-left: 10%;
}

.member-info-row {
  min-height: 3rem;
  margin: 1rem;
  border-bottom: solid 1px steelblue;
}

.member-info-row .title {
  display: inline-block;
  width: 50%;
  position: relative;
  text-align: right;
  vertical-align: middle;
  font-weight: bold;
  padding-right: 2rem;
}

.member-info-row .title + div {
  display: inline-block;
  text-align: left;
  vertical-align: middle;
  overflow-wrap: normal;
  padding: auto;
}

#downloadBtn {
  display: inline-block;
}

.chart-area {
  text-align: center;
  margin-top: 1rem;
}

.chart-div {
  display: inline-block;
  padding: 0.5rem;
  width: 30%;
}

.chart-1, .chart-2, .chart-3 {
  border: solid 1px #ced4da;
}

.horizontal-bar-view {
  width: 80%;
  margin-left: 10%;
  padding: 0.5rem 0;
}

.chart-title {
  width: 90%;
  margin-left: 5%;
  padding-top: 1rem;
  padding-bottom: 0.5rem;
  text-align: left;
  border-bottom: solid 1px steelblue;
}
</style>