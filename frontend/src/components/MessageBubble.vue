<template>
  <div :class="['message-bubble', messageTypeClass]">
    <div class="message-content">
      <div class="message-text" v-html="formattedText"></div>
      <div class="message-time">{{ formattedTime }}</div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

// Определение пропсов
const props = defineProps({
  message: {
    type: Object,
    required: true
  },
  isLast: {
    type: Boolean,
    default: false
  }
});

// Вычисляемые свойства
const messageTypeClass = computed(() => {
  return `message-${props.message.type}`;
});

// Форматирование текста сообщения (обработка переносов строк)
const formattedText = computed(() => {
  return props.message.text.replace(/\n/g, '<br>');
});

// Форматирование времени
const formattedTime = computed(() => {
  const date = new Date(props.message.timestamp);
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
});
</script>

<style scoped>
.message-bubble {
  display: flex;
  margin-bottom: 16px;
  animation: fadeIn 0.3s ease-in-out;
  max-width: 80%;
}

.message-user {
  align-self: flex-end;
  margin-left: auto;
}

.message-ai {
  align-self: flex-start;
  margin-right: auto;
}

.message-content {
  padding: 12px 16px;
  border-radius: 18px;
  position: relative;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
}

.message-user .message-content {
  background-color: var(--color-secondary);
  color: #fff;
  border-bottom-right-radius: 4px;
  margin-left: auto;
}

.message-ai .message-content {
  background-color: #fff;
  color: var(--color-text);
  border-bottom-left-radius: 4px;
  border-left: 4px solid var(--color-primary);
}

.message-text {
  line-height: 1.5;
  word-wrap: break-word;
}

.message-time {
  font-size: 0.75rem;
  opacity: 0.7;
  margin-top: 5px;
  text-align: right;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
