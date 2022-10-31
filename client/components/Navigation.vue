<template>
  <div class="navigation">
    <div class="nav-row" v-bind:class="{hidden: page.meta.hidden}" v-for="page in this.routes" v-bind:key="page.path" v-on:click="newPage(page, $event)">
      <span class="nav-row-name" v-show="isShowNav" v-bind:class="{select: page.meta.select}">
        {{page.name}}
      </span>
      <span v-show="!isShowNav" v-bind:class="{selectIcon: page.meta.select}">
        <font-awesome-icon :icon="page.meta.icon" size="lg" />
      </span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Navigation',
  components: {
  },
  props: {
    isShowNav: true,
  },
  data() {
    return {
      routes: this.getRoutes(),
    }
  },
  mounted() {
    this.routes.forEach(x => {
      if(x.name == this.$route.name) {
        x.meta.select = true;
      }
      else {
        x.meta.select = false;
      }
    });
  },
  methods: {
    getRoutes() {
      const defaultRouter = this.$router.options.routes.slice(1).filter(r => r['meta'].hidden === false); 
      if (this.$utils.getAuth() != 0) {
        // 管理者ではない場合、管理者メニュー以外を表示
        return defaultRouter.filter(r => r['meta'].requiresAuth === false); 
      }
      return defaultRouter;
    },
    newPage(page) {
      if(this.$route.path == page.path || page.meta.hidden) {
        return;
      }
      scrollTo(0, 0);
      if(page.path == '/' || page.path == '/logout') {
        this.$confirm('ログアウトします。よろしいですか？', '確認', {
          confirmButtonText: 'OK',
          cancelButtonText: 'キャンセル',
          type: 'warning',
          center: true
        }).then(() => {
          this.$utils.clearLoginInfo();
          this.$router.replace(this.$router.options.routes[0]);
        }).catch(() => {

        });
      }
      else if(page.path && this.$route.path !== page.path) {
        this.$router.push(page);
      }
    }
  },
  watch: {
    '$route'() {
      this.routes.forEach(x => {
        if(x.name == this.$route.name) {
          x.meta.select = true;
        }
        else {
          x.meta.select = false;
        }
      });
    }
  }
}
</script>

<style scoped lang="css">
.navigation {
}

.nav-row {
  min-width: 100%;
  min-height: 4rem;
  display: grid;
  place-items: center;
  color: white;
  font-size: 1rem;
  font-family: "Montserrat","游ゴシック",YuGothic,"ヒラギノ角ゴ ProN W3","Hiragino Kaku Gothic ProN","メイリオ",Meiryo,sans-serif;
  /* background-color: #ffffff; */
}

.nav-row:not(.hidden) {
  cursor: pointer;
}

.nav-row .nav-row-name {
  width: 80%;
  height: 2rem;
  line-height: 2rem;
  text-align: center;
  border-radius: 10% / 50%;
}

.nav-row:hover:not(.hidden) .nav-row-name, .select { 
  background: white;
  color: #333333;
}

.nav-row:hover:not(.hidden), .selectIcon { 
  color: #333333;
}

.nav-row .nav-row-name:not(.select) {
  color: white;
}

.hidden {
  opacity: 0.1;
}

</style>
