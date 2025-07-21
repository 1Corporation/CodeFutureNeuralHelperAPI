import { ref } from 'vue'
import ChatView from "../views/ChatView.vue";

export function useWebSockets(student_id, onMessageCallback) {
    const socket = ref(null)

    socket.value = new WebSocket(`wss://code-for-future.uc1.tech:8000/websocket/v1/wait_answer/?student_id=${student_id}`);
    socket.value.onmessage = (e) => {
        const response = JSON.parse(e.data);
        if (response.event == "answer") {
            onMessageCallback(response.text)
        }
    }
}
