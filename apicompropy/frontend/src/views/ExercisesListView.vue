<template>
  <div class="mt-2" id="exercises-list">
    <div class="container">
      <h2> Задачи</h2>
      <hr/>
      <div v-for="exercise in exercises" :key="exercise.slug">
        <router-link :to="{name: 'exercise', params: {slug: exercise.slug}}" class="exercise-link">
          <div class="card shadow p-2 mb-4 bg-white rounded">
          <div class="card-body">
            <div class="d-flex justify-content-between">
              <div>
                <div>
                  <span :class="'fa fa-star ' + ((exercise.rating > 0) ? 'checked': '')"></span>
                  <span :class="'fa fa-star ' + ((exercise.rating > 1) ? 'checked': '')"></span>
                  <span :class="'fa fa-star ' + ((exercise.rating > 2) ? 'checked': '')"></span>
                  <span :class="'fa fa-star ' + ((exercise.rating > 3) ? 'checked': '')"></span>
                  <span :class="'fa fa-star ' + ((exercise.rating > 4) ? 'checked': '')"></span>
                </div>
                <h4 class="card-title"><strong>{{ exercise.title }}</strong></h4>
              </div>
              <div>
                {{ renderTime(exercise.time_create)}}
              </div>
            </div>
            <div class="d-flex justify-content-between">
              <div>
                <h6 class="card-subtitle mb-2 text-muted">{{ exercise.author }}</h6>
              </div>
              <div>
                <p class="card-subtitle text-muted">Решений: {{ exercise.solutions_count }}</p>
              </div>
            </div>


            <div class="tag-list">
              <div class="tags">
                 <a href="#" class="card-link" v-for="tag in exercise.tags" :key="tag.pk">{{ tag }}</a>
              </div>
            </div>
          </div>
        </div>
        </router-link>
      </div>
    </div>
    <div class="text-center my-2" role="toolbar" aria-label="Buttons Toolbar">
      <div class="btn-group mr-2" role="group" aria-label="Pages Group">
        <button v-show="previous" @click="getExercises(previous)" class="btn btn-sm btn-outline-success my-1">
          &#8592;
        </button>
        <button v-show="next" @click="getExercises(next)" class="btn btn-sm btn-outline-success my-1">
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
  emits: ['changePage'],
  name: "ExercisesListView",
  data() {
    return {
      exercises: [],
      next: null,
      previous: null,
      name: "ExercisesListView"
    }
  },
  methods: {
    async getExercises(endpoint) {
      try {
        const response = await axios.get(endpoint)
        this.exercises = response.data.results
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
        alert(error.response.statusText)
      }
    },
    renderTime(time) {
      return getTime(time)
    }
  },
  created() {
    this.$emit('changePage', this.name)
    document.title = "ComProPy - Задачи"
    let endpoint = "/api/v1/exercises/headers/"
    this.getExercises(endpoint);

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
</style>