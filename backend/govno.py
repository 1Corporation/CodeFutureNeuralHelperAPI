import ollama


def main():

    with open("promt.txt", "r") as file:

        response = ollama.chat(model="llama3", messages=[
        {"role": "system",
         "message": "Далее я скину тебе запись вебинара в текстовом виде. Твоя задача вырезать из него все форматирование, таймкоды и прочее, а так же вырезать весь \"шум\" из вебинара, и оставить только полезные материалы."
        },
        {"role": "user",
         "message": file.read()
            }

    ])
        print(response["message"]["content"])



if __name__ == "__main__":
    main()
