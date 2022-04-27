<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light fixed-top my-navbar">
      <div style="width: 250px">
        <router-link class="navbar-brand" :to="{name: 'home'}">
          <img src="@/assets/python.png" width="35" height="35" class="d-inline-block align-bottom" alt="">
          <strong>ComProPy</strong>
        </router-link>
      </div>
      <div class="header-active">
          <form class="d-flex mr-auto">
            <input class="form-control me-2" type="search" placeholder="Искать..." aria-label="Search">
            <button class="btn btn-outline-success" type="submit">Поиск!</button>
          </form>
          <ul class="navbar-nav ms-auto">
            <li v-if="currentUser" class="nav-item px-2">
              <a class="btn btn-outline-secondary" href="/auth/logout/">Выйти</a>
            </li>
            <li v-else class="nav-item px-2">
              <a class="btn btn-outline-secondary" href="/auth/login/">Войти</a>
            </li>

          </ul>
      </div>
  </nav>
</template>


<script>
export default {
  name: "NavbarComponent",
  props: {
    currentUser: {
      type: Object,
      required: false
    }
  }
}
</script>

<style>
.navbar-brand {
  font-weight: bold;
  font-size: 150%;
  padding-left: 1rem;

}
.navbar-brand:hover {
  color: #dc3545 !important;
}

.btn{
  border: solid 2px #5c767c;
  color: black;
}
.btn:hover{
  background-color: #476d76;
  border: solid 2px #9DD899;
}

.my-navbar{
  border-bottom: 1px solid #ddd;
  height: 53px;
  box-shadow: 0px 3px 3px gray;
}

.navbar-toggler{
  float: right;
}
.pr-1{
  float: right;
  padding-right: 1rem;
}

.header-active{
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-right: 1rem;
  margin-left: 250px;
  padding-left: 1rem;
  position:fixed;
  width: calc(100% - 250px);
}


</style>