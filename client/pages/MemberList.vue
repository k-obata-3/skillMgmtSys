<template>
  <div class="member-list">
    <div class="title-label">
      <font-awesome-icon :icon="['fas', 'users']" class="fa-2x" />
      <div>メンバー一覧</div>
    </div>
    <div class="contents">
      <div class="card-item">
        <div v-for="item in list" v-bind:key="item.key" v-on:click="onClick(item)">
          <MemberNameCard :list='item'></MemberNameCard>
        </div>
      </div>
      <Pager ref="pager" :currentPage="currentPage" :limit="this.limit" :total="this.total" @changePage="changePage"></Pager>
    </div>
    <transition name="modal">
      <div v-show="this.isModalShow">
        <!-- <div class="overlay" v-on:click="onClosed()"></div> -->
        <div class="overlay"></div>
        <MemberInfoView class="modal-view" ref="child" @onClosed="onClosed"></MemberInfoView>
      </div>
    </transition>
  </div>
</template>

<script>
import MemberNameCard from '@/components/MemberNameCard.vue'
import MemberInfoView from '@/components/MemberInfoView.vue'
import Pager from '@/components/Pager.vue'

export default {
  name: 'MemberList',
  components: {
    MemberNameCard,
    MemberInfoView,
    Pager,
  },
  props: {
  },
  data() {
    return {
      list:[],
      isModalShow: false,
      total: 0,
      limit: 10,
      currentPage: 1,
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
    this.callApi(1);
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
    callApi(page) {
      var vm = this;
      var offset = page * this.limit - this.limit
      this.$apiService.getUserInfoList(this.limit, offset, function(res) {
        if(res != null) {
          var data = JSON.parse(res.data);
          const temp = [];
          if(data.userInfoList.length) {
            data.userInfoList.forEach(function(user) {
              var userDepartment= [];
              user.department.forEach(function(d) {
                userDepartment.push(d.name)
              });
              temp.push({
                first_name: user.first_name,
                last_name: user.last_name,
                department: userDepartment.length == 0 ? '-' : userDepartment.join('、'),
                position: user.position ?? '-',
                userInfo: user,
                career_info: user.career_info,
                career_info_dic: user.career_info_dic,
              });
            });
          }
          vm.list = temp;
          vm.$refs.pager.refreshPage(data.totalCount, page);
        }
      });
    },
    onClick(item) {
      // 子コンポーネントのイベントを呼び出す
      this.$refs.child.onRefresh(item);
      this.isModalShow = true;
    },
    onClosed() {
      this.isModalShow = false;
    },
    changePage(page) {
      this.list = [];
      this.callApi(page);
    }
  }
}
</script>

<style scoped>
.member-list .card-item {
  width: 100%;
  /* display: flex; */
  /* justify-content: center; */
  margin: auto;
}

.member-list .card-item > div:hover div {
  background-color: #e9f6f6;
}

.member-list .card-item > div {
  display: inline-block;
  width: 20rem;
  padding:  0 1rem 1rem 1rem;
  cursor: pointer;
}
</style>
