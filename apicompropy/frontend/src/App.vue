<template>

  <!--  Header  -->
  <div id="nav">
      <NavbarComponent :currentUser="user"/>
  </div>
  <div id="viewport">

    <div class="row" style="width: 100%">

      <!--  Left Sidebar  -->
      <div id="sidebar-left" class="col-2">
        <SidebarLeftComponent :currentPage="page" :currentUser="user"/>
      </div>

      <!--  Main  -->
      <div class="col-8 main bg-light">
        <router-view @changePage="changePage($event)" @updateNotifications="getCurrentUserData"/>
      </div>

      <!--  Right Sidebar  -->
      <div id="sidebar-right" class="col-2">
        <SidebarRightComponent />
      </div>
    </div>
  </div>
</template>


<script>
import NavbarComponent from "@/components/Navbar.vue"
import SidebarLeftComponent from "@/components/Sidebar.vue";
import SidebarRightComponent from "@/components/Rightbar.vue"
import {axios} from "@/common/api.service";

export default {
  name: "App",
  components: {
    SidebarLeftComponent,
    SidebarRightComponent,
    NavbarComponent
  },
  data() {
    return {
      page: 'Main',
      user: null
    }
  },
  methods: {
    changePage(name) {
      this.page = name
    },
    async getCurrentUserData(){
      const endpoint = `/api/v1/current_user/`
      try {
        const response = await axios.get(endpoint)
        this.user = response.data
      } catch (error) {
        this.user = null
      }
    }
  },
  created() {
    this.getCurrentUserData()
  }
}
</script>
<style>
      body {
        font-family: "Montserrat Alternates", sans-serif;
        font-weight: 600;
        overflow: hidden;

      }
      .main {
        margin-left: 270px;
        position: relative;
        margin-right: 0;
        margin-top: 0.5rem;
        opacity: 95%;
        border:  solid 1px #1d3557;
        border-radius: 5px;
      }

      #viewport{
        top: 53px;
        width: 100%;
        height: calc(100% - 53px);
        position: fixed;
        overflow-y: auto;
        background: rgb(2,0,36);
        padding-bottom: 0.5rem;
        background: radial-gradient(circle, rgba(2,0,36,1) 0%, rgba(9,14,124,1) 0%, rgba(9,9,121,1) 8%,
        rgba(7,46,146,1) 31%, rgba(6,82,169,1) 51%, rgba(4,132,202,1) 92%, rgba(0,212,255,1) 100%);
      }

      #sidebar-right{
        position: fixed;
      }
</style>
