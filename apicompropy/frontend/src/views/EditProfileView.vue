<template>
  <div class="mt-2" id="userPage">
    <form v-show="!loading" @submit.prevent="updateUserData">
      <div class="page-header">
        <div class="p-3">
          <h4 class="mb-3"><strong>Изменить информацию о себе:</strong></h4>
          <div class="row">
            <div class="col-4">
              <img :src="getAvatarURL" class="shadow-4 profile-pic" alt="Avatar" />
              <br>
              <label for="avatar" class="form-label">Загрузить новый аватар</label>
              <input class="form-control form-control-sm" type="file"
                     id="avatar" name="avatar" ref="avatar" @change="changeAvatar">
            </div>
            <div class="px-3 col-6">
              <div class="mb-3 d-flex">
                <div class="mx-3">
                  <label for="firstName" class="form-label">Имя:</label>
                  <input type="text" class="form-control" id="firstName" placeholder="Введите имя" required
                       v-model="currentUser.first_name">
                </div>
                <div class=" mx-3">
                  <label for="lastName" class="form-label">Фамилия:</label>
                  <input type="text" class="form-control" id="lastName" placeholder="Введите фамилию" required
                       v-model="currentUser.last_name">
                </div>

              </div>
              <div class="m-3">
                <label for="username" class="form-label">Юзернейм:</label>
                <input type="text" class="form-control" id="username" placeholder="Введите юзернейм" required
                       v-model="currentUser.username">
              </div>
              <div class="m-3">
                <label for="email" class="form-label">Email:</label>
                <input type="email" class="form-control" id="email" placeholder="Введите email" required
                       v-model="currentUser.email">
              </div>
              <div class="m-3">
                <label for="town" class="form-label">Город:</label>
                <input type="text" class="form-control" id="town" placeholder="Откуда вы" required
                       v-model="currentUser.town">
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="page-body p-3">
        <h4><strong>О себе </strong></h4>
        <span class="nonimportant_text">{{currentUser.about}}</span>
        <hr/>
        <h4><strong>Навыки </strong></h4>
        <span >{{currentUser.skills}}</span>
      </div>
      <div class="col-auto text-center">
        <button type="submit" class="btn mb-3">Подтвердить изменения</button>
      </div>
    </form>
    <div v-show="loading">
      Загрузка...
    </div>
  </div>
</template>

<script>
import {axios} from "@/common/api.service";

export default {
  emits: ['changePage'],
  name: "EditProfileView",
  data() {
    return {
      name: "MyPageView",
      currentUser: null,
      loading: true,
      changed: false
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
    async updateUserData() {
      const endpoint = `/api/v1/users/${this.currentUser.id}/`
          try {
            await axios.put(endpoint, {
              first_name: this.currentUser.first_name,
              last_name: this.currentUser.last_name,
              username: this.currentUser.username,
              email: this.currentUser.email,
              town: this.currentUser.town,
            })
          } catch (error) {
            console.log(error)
          }
          finally {
            this.$router.push({name: "user-page", params: {userId: this.currentUser.id }})
          }

    },
    changeAvatar(e) {
      e.preventDefault();
      let files = e.target.files
      if (!files.length) {
        return;
      }
      let reader = new FileReader();
      reader.onload = (e) => {
        this.currentUser.avatar = e.target.result;
      };
      reader.readAsDataURL(files[0]);
      this.changed = true

    }
  },
  computed: {
    getAvatarURL(){
      if (this.currentUser) {
        if (this.changed) {
          return this.currentUser.avatar
        }
        let pathname = this.currentUser.avatar
        const y = pathname.split('/')
        y.shift()
        if (y.length === 4) {
          return require(`../../../uploads/user_avatars/${y[2]}/${y[3]}`)
        }
        else {
          return require(`../../../uploads/user_avatars/${y[2]}`)
        }
      }
      return '#'
    }
  },
  created() {
    this.getCurrentUserData().then(() => {this.loading = false})
    this.$emit('changePage', this.name)
    document.title = 'ComProPy - Редактировать профиль'
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