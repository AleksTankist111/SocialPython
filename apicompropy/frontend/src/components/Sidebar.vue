<template>
  <div class="d-flex flex-column flex-shrink-0 p-3 bg-light bd-sidebar">
    <ul class="nav nav-pills flex-column mb-auto">
      <li class="nav-item">
        <router-link :class="'nav-link ' + (currentPage === 'MyPageView' ? 'active' : 'link-dark')"
                     :to="{name: 'user-page', params: {userId: (currentUser ? currentUser.id : 1)}}">
          Моя страница
        </router-link>
      </li>
      <li>
        <router-link :class="'nav-link ' + (currentPage === 'ExercisesListView' ? 'active' : 'link-dark')"
                     :to="{name: 'exercises-list'}">
          Задачи
        </router-link>
      </li>
      <li>
        <router-link :class="'nav-link ' + (currentPage === 'NotificationsView' ? 'active' : 'link-dark')"
                     :to="{name: 'notifications'}">
          Уведомления
          <span v-show="currentUser && currentUser.notifications_number" class="badge bg-primary rounded-pill">
            {{ currentUser ? currentUser.notifications_number : ''}}</span>
        </router-link>
      </li>
      <li>
        <a href="#" :class="'nav-link ' + (currentPage === 'SubscriptionsView' ? 'active' : 'link-dark')">
          Подписки
        </a>
      </li>
      <li>
        <a href="#" :class="'nav-link ' + (currentPage === 'SubscribersView' ? 'active' : 'link-dark')">
          Подписчики
        </a>
      </li>
      <li>
        <a href="#" :class="'nav-link ' + (currentPage === 'SubscribersView' ? 'active' : 'link-dark')">
          Пользователи
        </a>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "SidebarLeftComponent",
  props: {
    currentPage: {
      type: String,
      required: true
    },
    currentUser: {
      type: Object,
      required: false
    }
  }
}
</script>

<style>
.bd-sidebar {
  position: fixed;
  z-index: 1000;
  margin-top: 0.5rem;
  border-radius: 5px;
  width: 250px;
  left: 250px;
  margin-left: -250px;
  overflow-y: auto;
  -webkit-transition: all 0.5s ease;
  -moz-transition: all 0.5s ease;
  -o-transition: all 0.5s ease;
  transition: all 0.5s ease;
  opacity: 90%;
}
</style>