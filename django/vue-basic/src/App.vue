<template>
  <div>{{ rawHtml }}</div>
  <div>{{ rawHtml2 }}</div>
  <h1 v-html="rawHtml2"></h1>

  <h2 v-bind:class="{ active: isAcitve }">클레스 바인딩 테스트 입니다.</h2>
  <h2 :class="{ active: isAcitve }">클레스 바인딩 테스트 입니다.</h2>
  <button @click="change">버튼</button>
</template>

<script>
export default {
  data () {
    
    return {
      rawHtml: "이것은 텍스트입니다.",
      rawHtml2: '<span style="color: red">이것은 빨간색이어야 합니다.</span>',
      isAcitve: false,
    }
  },
  methods: {
    change() {
      this.isAcitve = !this.isAcitve
    }
  },
}
</script>

<style scoped>
h2.active {
  color: green;
}
</style>