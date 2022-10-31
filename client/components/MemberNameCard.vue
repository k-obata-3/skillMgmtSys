<template>
  <div class="member-name-card card">
    <div class="name-row">
      <h5>{{this.last_name}}&nbsp;{{this.first_name}}</h5>
    </div>
    <div>
      <div class="department-row">
        <div>部署</div>
        <div>{{this.department}}</div>
      </div>
      <div class="position-row">
        <div>役職</div>
        <div>{{this.position}}</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "MemberNameCard",
  components: {
  },
  props: {
    list: Object
  },
  data() {
    return {
      first_name: this.list.first_name,
      last_name: this.list.last_name,
      department: this.list.department,
      position: this.list.position,
      state: this.list.userInfo.state,
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
.member-name-card {
  overflow: hidden;
  height: 10.5rem;
}

.name-row {
  border-bottom: solid 1px steelblue;
  text-align: left;
  position: relative;
}

.name-row h5 {
  margin: 0.5rem;
  display: inline-block;
}

.department-row {
  padding-top: 0.5rem;
}

.department-row, .position-row {
  height: 3.5rem;
  margin-left: 1rem;
  text-align: left; 
}

.department-row div:first-child, .position-row div:first-child {
  /* display: inline-block; */
  color: #008080;
  font-weight: bold;
}

.department-row div:last-child, .position-row div:last-child {
  margin-left: 1rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
