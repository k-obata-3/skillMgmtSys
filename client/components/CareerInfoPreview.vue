<template>
  <div class="career-info-preview">
    <div class="career-info-preview-title">
      <div class="title-label">
        <font-awesome-icon :icon="['far', 'clipboard']" class="fa-2x" />
        <div>
          {{careerInfo.project_name}}
          <span>{{careerInfo.start_date}}</span>
          <span v-show="careerInfo.start_date != null || careerInfo.end_date != null">～</span>
          <span>{{careerInfo.end_date}}</span>
        </div>
      </div>
    </div>
    <div class="modal-closed-button">
      <el-button type="secondary" v-on:click="onClosed($event)">閉じる</el-button>
    </div>

    <div class="career-info">
      <div class="info-div">
        <p>概要</p>
        <p class="info-text">{{careerInfo.overview}}</p>
      </div>
      <div class="info-div">
        <p>機種</p>
        <div class="info-text" v-show="careerInfo.modelList.length != 0">
          <p v-for="(item, index) in careerInfo.modelList" v-bind:key="index">{{item}}</p>
        </div>
      </div>
      <div class="info-div">
        <p>OS</p>
        <div class="info-text" v-show="careerInfo.osList.length != 0">
          <p v-for="(item, index) in careerInfo.osList" v-bind:key="index">{{item}}</p>
        </div>
      </div>
      <div class="info-div">
        <p>言語</p>
        <div class="info-text" v-show="careerInfo.langList.length != 0">
          <p v-for="(item, index) in careerInfo.langList" v-bind:key="index">{{item}}</p>
        </div>
      </div>
      <div class="info-div">
        <p>データベース</p>
        <div class="info-text" v-show="careerInfo.dbList.length != 0">
          <p v-for="(item, index) in careerInfo.dbList" v-bind:key="index">{{item}}</p>
        </div>
      </div>
      <div class="info-div">
        <p>フレームワーク</p>
        <div class="info-text" v-show="careerInfo.frameworkList.length != 0">
          <p v-for="(item, index) in careerInfo.frameworkList" v-bind:key="index">{{item}}</p>
        </div>
      </div>
      <div class="info-div">
        <p>ツール</p>
        <div class="info-text" v-show="careerInfo.toolList.length != 0">
          <p v-for="(item, index) in careerInfo.toolList" v-bind:key="index">{{item}}</p>
        </div>
      </div>
      <div class="info-div">
        <p>作業担当</p>
        <div class="info-text" v-show="careerInfo.inChargeList.length != 0">
          <p v-for="(item, index) in careerInfo.inChargeList" v-bind:key="index">{{item}}</p>
        </div>
      </div>
      <div class="info-div">
        <p>役割</p>
        <div class="info-text" v-show="careerInfo.roleList.length != 0">
          <p v-for="(item, index) in careerInfo.roleList" v-bind:key="index">{{item}}</p>
        </div>
      </div>
      <div class="info-div">
        <p>メモ</p>
        <p class="info-text">{{careerInfo.other}}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CareerInfoPreview",
  components: {
  },
  props: {
  },
  data() {
    return {
      careerInfo: {
        project_name: '',
        overview: '',
        start_date: '',
        end_date: '',
        other: '',
        langList: [],
        dbList: [],
        osList: [],
        frameworkList: [],
        toolList: [],
        modelList: [],
        inChargeList: [],
        roleList: [],
      },
      inChargeOptions: [
        { text: "コンサルテーション(CN)", value: 1 },
        { text: "システム分析(SA)", value: 2 },
        { text: "システム設計(SD)", value: 3 },
        { text: "詳細設計(PD)", value: 4 },
        { text: "プログラム製造(PG)", value: 5 },
        { text: "システムテスト(ST)", value: 6 },
        { text: "運用(OP)", value: 7 },
        { text: "その他", value: 8 },
      ],
      roleOptions: [
        { text: "プロジェクトマネージャー(PM)", value: 1 },
        { text: "プロジェクトリーダー(PL)", value: 2 },
        { text: "チームリーダー(TL)", value: 3 },
      ],
    };
  },
  beforeCreated() {},
  created() {},
  beforeMount() {},
  mounted() {},
  beforeUpdate() {},
  updated() {},
  beforeDestroy() {},
  destroyed() {},
  methods: {
    callApi(id) {
      this.clearInputForm();
      var vm = this;
      this.$apiService.getCareerInfo(id, function (getRes) {
        if (getRes != null) {
          var careerInfo = [];
          if (Object.keys(getRes.data).length) {
            careerInfo = JSON.parse(getRes.data);

            vm.careerInfo.project_name = careerInfo.career_info.project_name;
            vm.careerInfo.overview = careerInfo.career_info.overview;
            vm.careerInfo.start_date = vm.$utils.GetSlashDate(careerInfo.career_info.start_date);
            vm.careerInfo.end_date = vm.$utils.GetSlashDate(careerInfo.career_info.end_date);
            vm.careerInfo.other = careerInfo.other;
            vm.$utils.AddFormInput(vm.careerInfo.modelList, careerInfo.model);
            vm.$utils.AddFormInput(vm.careerInfo.langList, careerInfo.language);
            vm.$utils.AddFormInput(vm.careerInfo.dbList, careerInfo.database);
            vm.$utils.AddFormInput(vm.careerInfo.osList, careerInfo.os);
            vm.$utils.AddFormInput(vm.careerInfo.frameworkList, careerInfo.framework);
            vm.$utils.AddFormInput(vm.careerInfo.toolList, careerInfo.tool);

            if (careerInfo.incharge.length != null) {
              let incharges = careerInfo.incharge.map(function(incharge) {
                return vm.inChargeOptions.filter(v => v.value == incharge).map(m => m.text).join(',');
              });
              vm.careerInfo.inChargeList = incharges;
            }

            if (careerInfo.role.length != null) {
              let roles = careerInfo.role.map(function(role) {
                return vm.roleOptions.filter(v => v.value == role).map(m => m.text).join(',');
              });
              vm.careerInfo.roleList = roles;
            }
          }
        }
      });
    },
    onClosed() {
      // this.onClear();
      // 親コンポーネントに onClosed イベントを渡す
      this.$emit('onClosed');
    },
    clearInputForm() {
      this.careerInfo.project_name = "";
      this.careerInfo.overview = "";
      this.careerInfo.other = "";
      this.careerInfo.start_date = "";
      this.careerInfo.end_date = "";
      this.careerInfo.langList = [];
      this.careerInfo.dbList = [];
      this.careerInfo.osList = [];
      this.careerInfo.frameworkList = [];
      this.careerInfo.toolList = [];
      this.careerInfo.modelList = [];
      this.careerInfo.inChargeList = [];
      this.careerInfo.roleList = [];
    },
  },
};
</script>

<style scoped>
.career-info-preview {
  overflow: scroll;
  padding-top: 2rem;
  padding-bottom: 2rem;
}

.career-info-preview-title {
  width: 90%;
  margin-left: 5%;
  display: inline-block;
}

.career-info {
  width: 80%;
  margin-left: 10%;
}

.info-div {
  border-bottom: solid 1px steelblue;
}

.info-div p:first-child:not(.info-text p) {
  font-weight: bold;
  padding-left: 0.5rem;
  /* margin-bottom: 0; */
}

.info-text {
  padding: 0 0 0.5rem 2rem;
  margin: 0;
}

.info-text p {
  display: inline-block;
  border-radius: 5px;
  padding: 0.5rem;
  background-image: linear-gradient(90deg, rgba(65, 160, 255, 1), rgba(60, 150, 240, 1));
  color: #ffffff;
  margin: 0.5rem 0.5rem 0 0;
}

.title-label div span {
  font-size: initial;
}
</style>