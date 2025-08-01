<template>
  <div class="btn-panel">
    <a
      v-for="(btn, index) in buttons"
      :key="index"
      :class="[
        'nav-btn',
        index === 0 ? 'left-nav-btn' : '',
        index === buttons.length - 1 ? 'right-nav-btn' : '',
        { active: index === activeIndex }
      ]"
      @click="handleClick(index)"
      @mouseenter="hoveredBtnIndex = index"
      @mouseleave="hoveredBtnIndex = null"
    >
      <div class="content">
        <component 
          :is="btn.icon" 
          class="icon" 
          v-show="hoveredBtnIndex !== index"
        />
        <span class="text" v-show="hoveredBtnIndex === index">
          {{ btn.text }}
        </span>
      </div>
    </a>
  </div>
</template>


<script>
export default {
  name: 'BtnPanel',
  props: {
    buttons: {
      type: Array,
      required: true,
    },
    activeIndex: {
      type: Number,
      default: 0,
    },
    hoveredBtnIndex: {
      type: Number,
      default: null,
    },
  },
  methods: {
    handleClick(index) {
      this.$emit('update:activeIndex', index);
      this.$router.push(this.buttons[index].path);
    }
  }
}
</script>

<style scoped>
.btn-panel {
  width: 600px;
  height: 50px;
  display: flex;
  gap: 2px;
}

.nav-btn {
  text-decoration: none;
  height: 100%;
  width: 110px;
  border: 0;
  background: #F5F5F5;
  color: #333333;
  padding: 0 20px;
  cursor: pointer;
  transition: width 0.8s ease, background-color 0.8s ease, color 0.8s ease;
  outline: none;
  display: flex;
  align-items: center;
  justify-content: center;
  white-space: nowrap;
  overflow: hidden;
}

.left-nav-btn {
  border-radius: 50px 0 0 0;
}

.right-nav-btn {
  border-radius: 0 50px 0 0;
}

.active {
  background: #ffffff;
}

.nav-btn:hover {
  width: 200px;
  background-color: #00B4D8;
  color: #ffffff;
}

.nav-btn p {
  margin: 0;
  user-select: none;
}
</style>
