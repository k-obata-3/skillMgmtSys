<template>
  <div>
    <div class="left" v-bind:style="leftStyles">
      <div class="menu-bar" v-on:click="onMenuClick()">
        <font-awesome-icon :icon="['fa', 'bars']" class="fa-2x" />
      </div>
      <div class="nav-title">
        <h3 v-if="this.isShowNav"><span>スキル管理システム</span></h3>
      </div>
      <Navigation v-if="this.onLogin" :isShowNav="this.isShowNav"></Navigation>
    </div>
    <div class="right" v-bind:style="rightStyles">
      <Nuxt/>
    </div>
  </div>
</template>

<script>
import Navigation from '@/components/Navigation.vue'

export default ({
  components: {
    Navigation,
  },
  data() {
    return {
      onLogin: false,
      isShowNav: true,
      leftStyles: {
        width: '200px',
      },
      rightStyles: {
        width: 'calc(100% - 4rem - 200px)',
        left: '200px',
      },
    }
  },
  beforeCreated() {
  },
  created() {
  },
  beforeMount() {
  },
  mounted() {
    if(this.$route.path != '/') {
      this.onLogin = true;
    }
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
    onMenuClick() {
      this.isShowNav = !this.isShowNav;
      if(this.isShowNav) {
        this.leftStyles = {
          width: '200px',
        };
        this.rightStyles = {
          width: 'calc(100% - 4rem - 200px)',
          left: '200px',
        };
      } else {
        this.leftStyles = {
          width: '50px',
        };
        this.rightStyles = {
          width: 'calc(100% - 4rem - 50px)',
          left: '50px',
        };
      }

    },
  },
  watch: {
    '$route'() {
      if (this.$route.path == '/') {
        this.onLogin = false;
      }
      else {
        this.onLogin = true;
      }
    },
    '$store.state.errorMsg'() {
      if(this.$store.state.errorMsg == null) {
        return;
      }

      this.$message({type: 'error', message: this.$store.state.errorMsg});
      this.$store.commit('setErrorMsg', null);
    }
  }
})
</script>

<style>
body {
  overflow-y: scroll;
  letter-spacing: 1px;
  font-family: "ヒラギノ角ゴ Pro W3", "Hiragino Kaku Gothic Pro", "メイリオ", "Meiryo", sans-serif;
}

.left {
  position: fixed;
  min-height: 100vh;
  width: 200px;
  top: 0;
  left: 0;
  bottom: 0;
  box-shadow: 0px 0px 5px #000000;
  background-image: url(~/assets/left-menu-background.png);
  background-repeat: no-repeat;
}

.right {
  position: absolute;
  /* min-height: 100vh; */
  width: calc(100% - 4rem - 200px);
  top: 0;
  left: 200px;
  bottom: 0;
  padding: 2rem;
  /* background-image: url(~/assets/right-background.png); */
  background-repeat: no-repeat;
  background-size: cover;
}

.nav-title {
  min-width: 100%;
  min-height: 4rem;
  display: grid;
  place-items: center;
  color: #ffffff;
  font-size: 1rem;
  font-weight: bold;
  text-align: center;
  border-bottom: solid 2px #ffffff;
}

/* スクロールバー非表示 */
::-webkit-scrollbar {
  /* display: none; */
  /* -webkit-appearance: none; */
}

.menu-bar {
  width: 30px;
  padding-left: 10px;
  margin-top: 10px;
  color: white;
  cursor: pointer;
}

</style>
