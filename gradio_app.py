import gradio as gr
import os
from tools import analyze_with_gigachat, analyze_with_openai

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
        result_box = gr.Textbox(label="Результат", lines=10)

        def preview_uploaded(file):
            return file.name if file else None

        file_upload.change(fn=preview_uploaded, inputs=file_upload, outputs=image_preview)

        def analyze(lang, model, uploaded_file):
            if not model:
                return "Не выбрана модель. Пожалуйста, выберите модель (GigaChat или GPT-4V)."

            if not uploaded_file:
                return "Не выбрано изображение. Пожалуйста, загрузите фото."

            image_path = uploaded_file.name

            if not os.path.exists(image_path):
                return "Указанный файл не существует. Повторите загрузку."

            try:
                if model == "GigaChat-2-Max":
                    return analyze_with_gigachat(image_path, lang)
                elif model == "GPT-4o":
                    return analyze_with_openai(image_path, lang)
                else:
                    return f"Неизвестная модель: {model}"

            except Exception as e:
                return f"Ошибка анализа: {e}"

        analyze_button.click(
            fn=analyze,
            inputs=[language_selector, model_selector, file_upload],
            outputs=result_box
        )

    return demo

demo = gradio_interface()
demo.launch()