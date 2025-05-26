import gradio as gr
import os
from tools import analyze_with_gigachat, analyze_with_openai, find_repair_services, has_damage

def gradio_interface():
    with gr.Blocks() as demo:
        gr.Markdown("## Детектор повреждений автомобиля по фото")

        with gr.Row():
            language_selector = gr.Radio(["Русский язык", "English language"], label="Выбор языка", value="Русский язык")
            model_selector = gr.Radio(["GigaChat-2-Max", "GPT-4o"], label="Выбор модели", value="GigaChat-2-Max")

        with gr.Row():
            with gr.Column():
                file_upload = gr.File(label="Загрузите изображение", file_types=["image"])
            image_preview = gr.Image(label="Предпросмотр изображения", type="filepath")

        analyze_button = gr.Button("Определить повреждения")
        result_box = gr.Textbox(label="Описание повреждений", lines=10)

        city_input = gr.Textbox(label="Город", placeholder="Введите город для поиска автосервисов", visible=False)
        search_button = gr.Button("Найти автосервис", visible=False)
        status = gr.Textbox(label="Статус", interactive=False)
        service_output = gr.Markdown(label="Найденные автосервисы", visible=False)

        def preview_uploaded(file):
            return file.name if file else None

        file_upload.change(fn=preview_uploaded, inputs=file_upload, outputs=image_preview)

        def analyze(lang, model, uploaded_file):
            if not model:
                return "Не выбрана модель. Пожалуйста, выберите модель (GigaChat или GPT-4V).", gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)

            if not uploaded_file:
                return "Не выбрано изображение. Пожалуйста, загрузите фото.", gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)

            image_path = uploaded_file.name

            if not os.path.exists(image_path):
                return "Указанный файл не существует. Повторите загрузку.", gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)

            try:
                if model == "GigaChat-2-Max":
                    result = analyze_with_gigachat(image_path, lang)
                elif model == "GPT-4o":
                    result = analyze_with_openai(image_path, lang)
                else:
                    return f"Неизвестная модель: {model}", gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)

                # Если найдены повреждения, показать поля
                if has_damage(result):
                    return result, gr.update(visible=True), gr.update(visible=True), gr.update(visible=True)

                else:
                    return result, gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)

            except Exception as e:
                return f"Ошибка анализа: {e}"

        analyze_button.click(
            fn=analyze,
            inputs=[language_selector, model_selector, file_upload],
            outputs=[result_box, city_input, search_button, service_output]
        )

        search_button.click(
            fn=find_repair_services,
            inputs=[model_selector, city_input],
            outputs=service_output
        )

    return demo

demo = gradio_interface()
demo.launch()