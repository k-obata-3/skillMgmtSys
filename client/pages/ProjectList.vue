<template>
  <div class="project-list">
    <div class="title-label">
      <font-awesome-icon :icon="['fas', 'project-diagram']" class="fa-2x" />
      <div>プロジェクト一覧</div>
    </div>
    <div class="contents">
      <div v-for="item  in list" v-bind:key="item.key">
        <ProjectItemCard :list='item'></ProjectItemCard>
      </div>
    </div>
  </div>
</template>

<script>
import ProjectItemCard from '@/components/ProjectItemCard.vue'

export default {
  name: "ProjectList",
  components: {
    ProjectItemCard
  },
  props: {
  },
  data() {
    return {
      list:[
        {name: 'WEB予約管理システム開発案件', language: ['Java'], framework: ['SpringBoot'], os: ['Linux'], dataBase: ['MySql'], contents: ['要件定義','設計','製造','試験'], startDate: '20xx/xx/xx', endDate: '20xx/xx/xx', member: ['田中太郎', '田口涼子', '野田大吾', '小原正', '山田健']},
        {name: 'Androidアプリ開発案件', language: ['C#'], framework: ['.NET'], os: ['Android', 'Linux'], dataBase: ['SQLite', 'SQLServer'], contents: ['要件定義','設計','製造','試験', 'デザイン'], startDate: '20xx/xx/xx', endDate: '20xx/xx/xx', member: ['斎藤敦', '太田清', '上田尚人']},
        {name: 'WEBシステム開発案件', language: ['PHP'], framework: ['Laravel'], os: ['Linux'], dataBase: ['MySql'], contents: ['要件定義','設計','製造','試験'], startDate: '20xx/xx/xx', endDate: '20xx/xx/xx', member: ['菊池彩', '佐藤花子']},
      ]
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
  }
}
</script>

<style scoped>
.project-list {
}

.project-list .left, .project-list .right {
}

.project-list .project-item-card {
  margin-bottom: 2rem;
}
</style>