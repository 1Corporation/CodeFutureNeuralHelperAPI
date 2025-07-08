/**
 * Сервис для взаимодействия с API нейросети
 *
 * Этот файл содержит заглушки методов, которые вы можете реализовать для
 * подключения к вашему серверу нейросети.
 */

// Базовый URL API (замените на свой)
const API_BASE_URL = 'http://localhost:8000/api/v1';

/**
 * Отправка сообщения нейросети и получение ответа
 * @param message текст сообщения
 * @param student_id student_id
 * @returns {Promise<Object>} - Ответ нейросети
 */
export const sendMessageToAI = async (message, student_id) => {
    try {
        // Это пример структуры:
        const response = await fetch(`${API_BASE_URL}/receive_message`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            text: message,
            student_id: student_id,
          }),
        });

        if (!response.ok) {
          throw new Error(`Ошибка API: ${response.status}`);
        }
    } catch (error) {
        console.error('Ошибка при отправке сообщения:', error);
        throw error;
    }
};

/**
 * Получение истории сообщений для указанной беседы
 * @param student_id УНТИ СТУДЕНТА
 * @param full_name ФИО студента
 * @param course название курса на котором обучается студент (element|python)
 * @param timetable расписание ученика TODO:Уточните формат в котором отправляется расписание
 * @returns {Promise<Array>} - История сообщений
 */
export const getChatHistory = async (student_id, full_name, course, timetable) => {
    try {
        // Пример структуры:

        const response = await fetch(
            `${API_BASE_URL}/get_chat_history?student_id=${student_id}&full_name=${full_name}&course=${course}&timetable=${timetable}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

        if (!response.ok) {
            throw new Error(`Ошибка API: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Ошибка при отправке сообщения:', error);
        throw error;
    }
};
