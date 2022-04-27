<template>
  <div class="mt-2" id="notifications-list">
    <div class="container">
      <h2> Уведомления</h2>
      <hr/>
      <div v-show="notifications.length === 0">
        <h5>Нет уведомлений!</h5>
      </div>
      <div v-for="notification in notifications" :key="notification.id">
        <div :class="'card shadow p-2 mb-4 rounded ' + (notification.is_read ? 'bg-is_read' : 'bg-white')" @click="makeRead(notification)">
          <div class="card-body">
            <div class="d-flex justify-content-between">
              <div>
                <p class="card-title">{{ notification.note }}</p>
              </div>
              <div class="d-flex">
                <div class="px-2">
                  {{ renderTime(notification.time_create)}}
                </div>
                <div>
                  <button type="button" class="btn-close" aria-label="Close" @click="deleteNotification(notification)"></button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="text-center my-2" role="toolbar" aria-label="Buttons Toolbar">
      <div class="btn-group mr-2" role="group" aria-label="Pages Group">
        <button v-show="previous" @click="getNotifications(previous)" class="btn btn-sm btn-outline-success my-1">
          &#8592;
        </button>
        <button v-show="next" @click="getNotifications(next)" class="btn btn-sm btn-outline-success my-1">
          &#8594;
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { axios } from "@/common/api.service.js";
import {getTime} from "@/common/timeHandler";

export default {
  emits: ['changePage', 'updateNotifications'],
  name: "NotificationsView",
  props: {
    currentUser: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      notifications: [],
      next: null,
      previous: null,
      name: "NotificationsView",
      current: null
    }
  },
  methods: {
    async getNotifications(endpoint) {
      try {
        const response = await axios.get(endpoint)
        this.current = endpoint
        this.notifications = response.data.results
        const body = document.getElementById("viewport")
        body.scrollTo(0,0)
        if (response.data.next) {
          this.next = response.data.next
        } else {
          this.next = null
        }
        if (response.data.previous) {
          this.previous = response.data.previous
        } else {
          this.previous = null
        }
      } catch (error) {
        console.log(error.response)
      }
    },
    renderTime(time) {
      return getTime(time)
    },
    async makeRead(notification) {
      if (!notification.is_read) {
        try {
          notification.is_read = true
          await axios.put(`/api/v1/notifications/${notification.id}/`, {'is_read': 1})
          this.$emit('updateNotifications')
        } catch (error) {
          console.log(error.response)
        }
      }
    },
    async deleteNotification(notification) {
      try {
          await axios.delete(`/api/v1/notifications/${notification.id}/`)
          await this.getNotifications(this.current)
          this.$emit('updateNotifications')
        } catch (error) {
          console.log(error.response)
        }
    }
  },
  created() {
    this.$emit('changePage', this.name)
    document.title = "Уведомления"
    let endpoint = "/api/v1/notifications/"
    this.getNotifications(endpoint);

  },
}
</script>

<style>
.checked {
    color: #0e42ef;
}
.exercise-link{
  font-weight: 600;
  text-decoration: none;
  color: black;
}
.exercise-link:hover{
  color: #343a40;
}

.bg-is_read{
  background: darkgray;
}
</style>