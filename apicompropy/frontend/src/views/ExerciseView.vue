<template>
      <div class="container mt-3">
        <div v-if="exercise">
          <div class="meta-data">
            <p class="card-subtitle mb-2 text-muted">Решений: {{ exercise.solutions_count }}</p>
            <h6 class="card-subtitle mb-2 text-muted">{{ renderTime(exercise.time_create)}}</h6>
          </div>
          <div class="exercise-header">
            <div>
              <div>
                <span :class="'fa fa-star ' + ((exercise.rating > 0) ? 'checked': '')"></span>
                <span :class="'fa fa-star ' + ((exercise.rating > 1) ? 'checked': '')"></span>
                <span :class="'fa fa-star ' + ((exercise.rating > 2) ? 'checked': '')"></span>
                <span :class="'fa fa-star ' + ((exercise.rating > 3) ? 'checked': '')"></span>
                <span :class="'fa fa-star ' + ((exercise.rating > 4) ? 'checked': '')"></span>
              </div>
              <h2 class="card-title"><strong>{{ exercise.title }}</strong></h2>
              <h6 class="card-subtitle mb-2 text-muted">{{ exercise.author_username }}</h6>
              <div class="tag-list">
              <div class="tags">
                 <a href="#" class="card-link" v-for="tag in exercise.tags" :key="tag.pk">{{ tag }}</a>
              </div>
            </div>
            </div>
          </div>

          <div class="description">
            <div class="description-main">
              <h3><strong>Описание</strong></h3>
              <p>{{exercise.description_main}}</p>
            </div>
            <hr/>
            <div class="description-inputs">
              <h3><strong>Входные данные</strong></h3>
              <p>{{exercise.description_inputs}}</p>
            </div>
            <hr/>
            <div class="description-outputs">
              <h3><strong>Выходные данные</strong></h3>
              <p>{{exercise.description_outputs}}</p>
            </div>
            <hr/>
            <div class="example">
              <h3><strong>Пример</strong></h3>
              <table class="table table-bordered">
                <thead>
                  <tr>
                    <th>INPUT.txt</th>
                    <th>OUTPUT.txt</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <th scope="col">{{exercise.example_inputs}}</th>
                    <th scope="col">{{exercise.example_outputs}}</th>
                  </tr>
                </tbody>
              </table>
            </div>
            <hr/>
          </div>
          <div class="container mt-3">
            <div class="comments">
              <h3>Комментарии</h3>
              <p v-show="comments.length === 0">Комментариев пока нет!</p>
              <div v-for="comment in comments" :key="comment.time_create">
                <div class="card shadow py-2 my-2 bg-white rounded">
                  <div class="card-body">
                    <div class="d-flex justify-content-between">
                      <div>
                        <h5 class="card-title"><strong>{{ comment.author_name }}</strong></h5>
                      </div>
                      <div>
                        {{ renderTime(comment.time_create)}}
                      </div>
                    </div>
                    <hr class="my-1"/>
                    <div class="d-flex">
                      <div>
                        <p class="card-subtitle mt-2 text-muted">{{ comment.content }} </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-else>
          <h4>404 - Задача не найдена</h4>
        </div>
      </div>
</template>

<script>
import {axios} from "@/common/api.service";
import {getTime} from "@/common/timeHandler";

export default {
  name: "ExerciseView",
  props: {
    slug: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      exercise: {},
      comments: [],
      name: "ExerciseView"
    }
  },
  methods: {
    setPageTitle(title) {
      document.title = title
    },
    async getExerciseData() {
      const endpoint = `/api/v1/exercises/${this.slug}/`
      try {
        const response = await axios.get(endpoint)
        this.exercise = response.data
        this.setPageTitle(this.exercise.title)
      } catch (error) {
        this.setPageTitle('404 - Задача не найдена')
        this.exercise = null
      }
    },
    async getCommentsData() {
      const endpoint = `/api/v1/comments/?task=${this.slug}`
      try {
        const response = await axios.get(endpoint)
        this.comments = response.data.results
      } catch (error) {
        this.comments = null
      }
    },
    renderTime(time) {
      return getTime(time)
    }
  },
  created() {
    this.$emit('changePage', this.name)
    this.getExerciseData()
    this.getCommentsData()
  }
}
</script>

<style>
.exercise-header{
  text-align: center;
}
.meta-data{
  justify-content: space-between;
  display: flex;
}
</style>