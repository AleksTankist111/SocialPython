<template>
  <div class="home">
    <h1>Главная страница</h1>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: 'HomeView',
  data(){
    return {
      name: "HomeView"
    }
  },
  created() {
    document.title = "ComProPy"
    this.$emit('changePage', this.name)
  }
}
</script>
