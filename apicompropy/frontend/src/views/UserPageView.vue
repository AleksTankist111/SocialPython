<template>
  <div class="mt-2" id="userPage">
    <div>
      <div class="page-header">
        <div class="d-flex p-3 justify-content-between">
          <div class="d-flex">
            <img :src="getAvatarURL" class="shadow-4 profile-pic" alt="Avatar" />
            <div class="px-3">
              <h4><strong>{{user.first_name}} {{user.last_name}}</strong>
                <span style="font-size: 20px">{{"\t(" + user.online_status + ")"}}</span>
              </h4>
              <h6 class="card-subtitle mb-2">{{user.username}}</h6>
              <div class="header-additional pt-2">
                <span class="nonimportant_text">email: {{user.email}}</span>
                <br>
                <span class="nonimportant_text">Город: {{user.town}}</span>
              </div>
            </div>
          </div>
          <div>
            <h6 style="float: right;"><strong>Рейтинг: {{user.rating}}</strong></h6>
            <br>
            <button v-show="currentUser && !isMyPage() && !user.is_subscribed" @click="subcribe"
                    type="button" class="btn btn-outline-info" >
              Подписаться
            </button>
            <button v-show="currentUser && !isMyPage() && user.is_subscribed" @click="unsubscribe"
                    type="button" class="btn btn-outline-info" >
              Отписаться
            </button>
            <button v-show="currentUser && isMyPage()"
                    type="button" class="btn btn-outline-info" style="float:right">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pen" viewBox="0 0 16 16">
                <path d="m13.498.795.149-.149a1.207 1.207 0 1 1 1.707 1.708l-.149.148a1.5 1.5 0 0 1-.059 2.059L4.854 14.854a.5.5 0 0 1-.233.131l-4 1a.5.5 0 0 1-.606-.606l1-4a.5.5 0 0 1 .131-.232l9.642-9.642a.5.5 0 0 0-.642.056L6.854 4.854a.5.5 0 1 1-.708-.708L9.44.854A1.5 1.5 0 0 1 11.5.796a1.5 1.5 0 0 1 1.998-.001zm-.644.766a.5.5 0 0 0-.707 0L1.95 11.756l-.764 3.057 3.057-.764L14.44 3.854a.5.5 0 0 0 0-.708l-1.585-1.585z"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
      <div class="page-body p-3">
        <h4><strong>О себе </strong></h4>
        <span class="nonimportant_text">{{user.about}}</span>
        <hr/>
        <h4><strong>Навыки </strong></h4>
        <span >{{user.skills}}</span>
        <hr/>
        <div class="accordion" id="accordionUser">
          <div class="accordion-item">
            <h6 class="accordion-header" id="headingUserOne">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseUserOne" aria-expanded="false" aria-controls="collapseUserOne">
                <strong>Выложенные задачи:</strong>
              </button>
            </h6>
            <div id="collapseUserOne" class="accordion-collapse collapse" aria-labelledby="headingUserOne" data-bs-parent="#accordionUser">
                <ol class="list-group list-group-numbered">
                  <li class="list-group-item" v-for="task in authoredTasks" :key="task.slug">
                    <router-link :to="{name: 'exercise', params: {slug: task.slug}}" style="font-size: 17px" class="rate_link">
                      <strong>{{task.title}}</strong>
                    </router-link>
                  </li>
                </ol>
            </div>
          </div>
          <div class="accordion-item">
            <h6 class="accordion-header" id="headingUserTwo">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseUserTwo" aria-expanded="false" aria-controls="collapseUserTwo">
                <strong>Решенные задачи: </strong>
              </button>
            </h6>
            <div id="collapseUserTwo" class="accordion-collapse collapse" aria-labelledby="headingUserTwo" data-bs-parent="#accordionUser">
              <ol class="list-group list-group-numbered">
                <li class="list-group-item" v-for="task in solvedTasks" :key="task.slug">
                    <router-link :to="{name: 'exercise', params: {slug: task.slug}}" style="font-size: 17px" class="rate_link">
                      <strong>{{task.title}}</strong>
                    </router-link>
                </li>
              </ol>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {axios} from "@/common/api.service";

export default {
  emits: ['changePage'],
  name: "UserPageView",
  props: {
    userId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      name: "UserPageView",
      currentUser: null,
      user: {
        first_name: '',
        last_name: '',
        username: '',
        avatar: null,
      },
      authoredTasks: [],
      solvedTasks: []
    }
  },
  methods: {
    async getCurrentUserData(){
          const endpoint = `/api/v1/current_user/`
          try {
            const response = await axios.get(endpoint)
            this.currentUser = response.data
          } catch (error) {
            this.currentUser = null
          }
        },
    async getUserPageData(){
          const endpoint = `/api/v1/users/${this.userId}/`
          try {
            const response = await axios.get(endpoint)
            this.user = response.data
            document.title = `ComProPy - ${this.user.first_name} ${this.user.last_name}`
          } catch (error) {
            this.currentUser = null
          }
        },
    async getUserAuthoredTasksData(){
          const endpoint = `/api/v1/users/${this.userId}/authored/`
          try {
            const response = await axios.get(endpoint)
            this.authoredTasks = response.data
          } catch (error) {
            this.authoredTasks = []
          }
        },
    async getUserSolvedTasksData(){
          const endpoint = `/api/v1/users/${this.userId}/solved/`
          try {
            const response = await axios.get(endpoint)
            this.solvedTasks = response.data
          } catch (error) {
            this.solvedTasks = []
          }
        },
    async subcribe(){
      const endpoint = `/api/v1/subscriptions/`
          try {
            await axios.post(endpoint, {followed: this.userId})
            await this.getUserPageData()
          } catch (error) {
            console.log(error)
          }
    },
    async unsubscribe(){
      const endpoint = `/api/v1/subscriptions/${this.user.is_subscribed}/`
          try {
            await axios.delete(endpoint)
            await this.getUserPageData()
          } catch (error) {
            console.log(error)
          }
    },
    isMyPage(){
      return this.userId === String(this.currentUser.id)
    },
  },
  computed: {
    getAvatarURL(){
      if (this.user.avatar) {
        let pathname = new URL(this.user.avatar).pathname;
        const y = pathname.split('/')
        y.shift()
        return require(`../../../uploads/user_avatars/${y[2]}/${y[3]}`)
      }
      return '#'
    }
  },
  created() {

    this.getCurrentUserData().then(() => {
        this.getUserPageData().then(() => {
          if (this.isMyPage()) {
            this.name = 'MyPageView'
          }
          this.$emit('changePage', this.name)
          })
      })
    this.getUserAuthoredTasksData()
    this.getUserSolvedTasksData()
  }
}
</script>

<style>
.profile-pic {
  object-fit: cover;
  border-radius: 10%;
  height: 150px;
  /*width: 150px;*/
}

.nonimportant_text{
  font-weight: 400;
}
</style>