<template>
  <div>
    <div class="left">
      <div class="nav-title">
        <h3><span>スキル管理システム</span></h3>
      </div>
      <Navigation v-if="this.onLogin"></Navigation>
    </div>
    <div class="right">
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
</style>
