<template>
  <div class="chat-container">
    <header class="chat-header">
      <h1>Помощник от Кода Будущего от 1С</h1>
      <p>Перепроверяйте ответы от нейросети, помощник существует исключительно для справки. Если останутся вопросы,
        перейдите в <a href="https://t.me/party_notificaton_codefuture_bot">чат-бот</a> с живым человеком</p>
    </header>

    <div class="chat-messages" ref="messagesContainer">
      <div v-if="messages.length === 0" class="chat-empty-state">
        <div class="empty-icon">🤖</div>
        <p>Начните диалог с нейросетью</p>
      </div>

      <transition-group name="message-fade">
        <message-bubble
            v-for="(message, index) in messages"
            :key="index"
            :message="message"
            :isLast="index === messages.length - 1"
        />
      </transition-group>

      <div v-if="isLoading" class="loading-indicator">
        <div class="dot-pulse"></div>
      </div>
    </div>

    <div class="chat-input-container">
      <textarea
          v-model="userInput"
          class="chat-input"
          placeholder="Введите сообщение..."
          @keydown.enter.prevent="sendMessage"
          :disabled="isLoading"
          ref="inputField"
      ></textarea>
      <button
          class="send-button btn btn-primary"
          @click="sendMessage"
          :disabled="isLoading || !userInput.trim()"
      >
        <span class="send-icon">➤</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import {ref, onMounted, watch, nextTick} from 'vue';
import MessageBubble from '../components/MessageBubble.vue';
import {getChatHistory, sendMessageToAI} from '../services/apiService';
import {useWebSockets} from "../services/websockets.js";

// Состояние чата
const messages = ref([]);
const userInput = ref('');
const isLoading = ref(false);
const messagesContainer = ref(null);
const inputField = ref(null);


// Получить query params из запроса
const getQueryParams = () => {
  const search = window.location.search;
  return Object.fromEntries(new URLSearchParams(search));
};

// Достаю параметры из запроса
const queryParams = getQueryParams();
const student_id = queryParams.student_id;
const course = queryParams.course;
const timetable = queryParams.timetable;
const full_name = queryParams.full_name;

// Метод для создания сообщения от пользователя
const createUserMessage = (text) => {
  return {
    id: Date.now(),
    text,
    type: 'user',
    timestamp: new Date().toISOString()
  };
};

// Метод для создания сообщения от нейросети
const createAIMessage = (text) => {
  return {
    id: Date.now(),
    text,
    type: 'ai',
    timestamp: new Date().toISOString()
  };
};


// Вызовется в websocket.js, после того как на websocket придет ответ
const onAnswerReceive = (text) => {
  const message = createAIMessage(text);
  messages.value.push(message);
  isLoading.value = false;
  scrollToBottom()
}

// Метод для отправки сообщения
const sendMessage = async () => {

  const text = userInput.value.trim();
  if (!text || isLoading.value) return;

  // Добавляем сообщение пользователя
  const userMessage = createUserMessage(text);
  messages.value.push(userMessage);
  userInput.value = '';

  // Прокручиваем чат вниз
  await scrollToBottom();

  // Устанавливаем состояние загрузки
  isLoading.value = true;

  try {
    // Отправляем запрос к API нейросети
    await sendMessageToAI(text, student_id);

    useWebSockets(student_id, onAnswerReceive);
  } catch (error) {
    console.error('Ошибка при получении ответа:', error);
    isLoading.value = false;

    // Добавляем сообщение об ошибке
    const errorMessage = createAIMessage('Произошла ошибка при получении ответа. Пожалуйста, попробуйте еще раз.');
    messages.value.push(errorMessage);
    scrollToBottom();
  }
};


// Прокрутка чата вниз
const scrollToBottom = async () => {
  await nextTick();
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};


// Следим за изменениями в сообщениях и прокручиваем вниз
watch(messages, () => {
  scrollToBottom();
});

// При монтировании компонента
onMounted(() => {
  // Фокус на поле ввода
  if (inputField.value) {
    inputField.value.focus();
  }

  const welcomeMessage = createAIMessage('Привет! Я нейросеть. Чем я могу помочь вам сегодня?');
  messages.value.push(welcomeMessage);

  getChatHistory(student_id, full_name, course, timetable).then(chat_history => {

    for (const message of chat_history) {
      console.log(message)
      const role = message.role;
      const text = message.text;

      let message_object

      if (role === 'student') {
        message_object = createUserMessage(text);
      } else {
        message_object = createAIMessage(text);
      }

      messages.value.push(message_object);
    }
    scrollToBottom();
  })
});
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px 0;
}

.chat-header {
  padding: 16px;
  background-color: var(--color-primary);
  border-radius: var(--border-radius) var(--border-radius) 0 0;
  box-shadow: var(--box-shadow);
  text-align: center;
}

.chat-header h1 {
  margin: 0;
  color: var(--color-text);
  font-size: 1.8rem;
}

.chat-header p {
  margin: 5px 0 0;
  color: var(--color-text-light);
  font-size: 1rem;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background-color: var(--color-light);
  border-left: 1px solid rgba(255, 193, 7, 0.2);
  border-right: 1px solid rgba(255, 193, 7, 0.2);
}

.chat-empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  opacity: 0.7;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.loading-indicator {
  display: flex;
  justify-content: center;
  margin: 16px 0;
}

.dot-pulse {
  position: relative;
  width: 10px;
  height: 10px;
  border-radius: 5px;
  background-color: var(--color-secondary);
  animation: dot-pulse 1.5s infinite linear;
}

.dot-pulse::before,
.dot-pulse::after {
  content: '';
  position: absolute;
  display: inline-block;
  top: 0;
  width: 10px;
  height: 10px;
  border-radius: 5px;
  background-color: var(--color-secondary);
}

.dot-pulse::before {
  left: -15px;
  animation: dot-pulse-before 1.5s infinite linear;
}

.dot-pulse::after {
  left: 15px;
  animation: dot-pulse-after 1.5s infinite linear;
}

@keyframes dot-pulse-before {
  0% {
    opacity: 0.4;
  }
  25% {
    opacity: 1;
  }
  50% {
    opacity: 0.4;
  }
  75% {
    opacity: 0.4;
  }
  100% {
    opacity: 0.4;
  }
}

@keyframes dot-pulse {
  0% {
    opacity: 0.4;
  }
  25% {
    opacity: 0.4;
  }
  50% {
    opacity: 1;
  }
  75% {
    opacity: 0.4;
  }
  100% {
    opacity: 0.4;
  }
}

@keyframes dot-pulse-after {
  0% {
    opacity: 0.4;
  }
  25% {
    opacity: 0.4;
  }
  50% {
    opacity: 0.4;
  }
  75% {
    opacity: 1;
  }
  100% {
    opacity: 0.4;
  }
}

.chat-input-container {
  display: flex;
  padding: 16px;
  background-color: var(--color-primary);
  border-radius: 0 0 var(--border-radius) var(--border-radius);
  box-shadow: var(--box-shadow);
}

.chat-input {
  flex: 1;
  padding: 12px 16px;
  border: none;
  border-radius: var(--border-radius-sm);
  resize: none;
  font-size: 1rem;
  line-height: 1.5;
  max-height: 120px;
  overflow-y: auto;
  background-color: var(--color-card);
}

.chat-input:focus {
  outline: none;
  box-shadow: 0 0 0 2px var(--color-secondary);
}

.send-button {
  margin-left: 12px;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--color-secondary);
  color: white;
  transition: all 0.2s ease;
}

.send-button:hover:not(:disabled) {
  background-color: var(--color-accent);
  transform: scale(1.05);
}

.send-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.send-icon {
  font-size: 1.2rem;
}

.message-fade-enter-active,
.message-fade-leave-active {
  transition: all 0.3s ease;
}

.message-fade-enter-from,
.message-fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
</style>
