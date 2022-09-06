<template>
  <div class="project-item-card card">
    <div class="name-row">
        <h5>{{this.name}}</h5>
    </div>
    <div>
      <div class="row">
        <div>{{this.language}}</div>
      </div>
      <div class="row">
        <div>{{this.framework}}</div>
      </div>
      <div class="row">
        <div>{{this.os}}</div>
      </div>
      <div class="row">
        <div>{{this.dataBase}}</div>
      </div>
      <div class="row">
        <div>{{this.contents}}</div>
      </div>
      <div class="row">
        <div>{{this.startDate}}&nbsp;～&nbsp;{{this.endDate}}</div>
      </div>
      <div class="row">
        <div>{{this.member}}</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ProjectItemCard",
  components: {
  },
  props: {
    list: Object
  },
  data() {
    return {
      name: this.list.name,
      language: this.list.language.join('、'),
      framework: this.list.framework.join('、'),
      os: this.list.os.join('、'),
      dataBase: this.list.dataBase.join('、'),
      contents: this.list.contents.join('、'),
      startDate: this.list.startDate,
      endDate: this.list.endDate,
      member: this.list.member.join('、'),
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
.project-item-card .name-row + div {
  padding-top: 1rem;
}

.project-item-card .row {
  min-height: 2rem;
  text-align: center;
}
</style>
