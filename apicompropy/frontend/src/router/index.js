import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ExercisesListView from "@/views/ExercisesListView";
import NotificationsView from "@/views/NotificationsView";
import App from "@/App";
import UserPageView from "@/views/UserPageView";
import EditProfileView from "@/views/EditProfileView";

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/exercises/',
    name: 'exercises-list',
    component: ExercisesListView
  },
  {
    path: '/exercises/:slug',
    name: 'exercise',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/ExerciseView.vue'),
    props: true
  },
  {
    path: '/notifications/',
    name: 'notifications',
    component: NotificationsView,
    props: {currentUser: App.currentUser}
  },
  {
    path: '/users/:userId/',
    name: 'user-page',
    component: UserPageView,
    props: route => ({userId: route.params.userId})
  },
  {
    path: '/users/edit/',
    name: 'edit-profile',
    component: EditProfileView,
  },
]

const router = createRouter({
  history: createWebHistory("/"),
  routes
})

export default router
