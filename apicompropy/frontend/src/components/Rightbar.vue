<template>
  <div class="d-flex flex-column flex-shrink-0 p-3 bg-light bd-rightbar">
    <div class="accordion" id="accordionExample">
      <div class="accordion-item">
        <h6 class="accordion-header" id="headingOne">
          <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne" aria-expanded="false" aria-controls="collapseOne">
            <strong>TOP задач:</strong>
          </button>
        </h6>
        <div id="collapseOne" class="accordion-collapse collapse" aria-labelledby="headingOne" data-bs-parent="#accordionExample">
            <ol class="list-group list-group-numbered">
              <li class="list-group-item" v-for="top in exercisesRating" :key="top.rating">
                <router-link :to="{name: 'exercise', params: {slug: top.slug}}" class="rate_link">
                {{top.title.length<15 ? top.title : (top.title.substring(0,15)+"...")}}
                </router-link> | <strong>{{top.rating}}</strong></li>
            </ol>
        </div>
      </div>
      <div class="accordion-item">
        <h6 class="accordion-header" id="headingTwo">
          <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
            <strong>TOP юзеров: </strong>
          </button>
        </h6>
        <div id="collapseTwo" class="accordion-collapse collapse" aria-labelledby="headingTwo" data-bs-parent="#accordionExample">
          <ol class="list-group list-group-numbered">
            <li class="list-group-item" v-for="top in usersRating" :key="top.rating">
              {{top.username.length<15 ? top.username : (top.username.substring(0,15)+"...")}} | <strong>{{top.rating}}</strong>
            </li>
          </ol>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {axios} from "@/common/api.service";

export default {
  name: "SidebarRightComponent",
  data() {
    return {
      exercisesRating: null,
      usersRating: null
    }
  },
  methods: {
    async getExerciseRatingData() {
      const endpoint = '/api/v1/top_exercises/'
      try {
        const response = await axios.get(endpoint)
        this.exercisesRating = response.data
      } catch (error) {
        this.exercisesRating = null
      }
    },
    async getUsersRatingData() {
      const endpoint = '/api/v1/top_users/'
      try {
        const response = await axios.get(endpoint)
        this.usersRating = response.data
      } catch (error) {
        this.usersRating = null
      }
    },
  },
  created() {
    this.getExerciseRatingData()
    this.getUsersRatingData()
  }
}
</script>

<style>
.bd-rightbar {
  position: fixed;
  z-index: 1000;
  margin-top: 0.5rem;
  border-radius: 5px;
  width: calc(100% - 250px - 69%);
  right: 275px;
  margin-right: -250px;
  overflow-y: auto;
  overflow-x: hidden;
  -webkit-transition: all 0.5s ease;
  -moz-transition: all 0.5s ease;
  -o-transition: all 0.5s ease;
  transition: all 0.5s ease;
  opacity: 90%;
}

.rate_link{
  font-size: 14px;
  text-decoration: none;
  color: #343a40;

}
</style>