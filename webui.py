import gradio as gr
import requests
import json
import re

# Server's URL
api_url_base = "http://server.abitcons.com:8089"

def generate_query(question):
    # Generating the full URL with the question parameter
    url = f"{api_url_base}/SAP/GenerateQuery?question={requests.utils.quote(question)}"
    # Making a POST request and expecting JSON response
    response = requests.post(url, headers={"accept": "application/json"})
    return format_response(response.json())

def generate_summary(question):
    url = f"{api_url_base}/SAP/SAPQuerySummary?question={requests.utils.quote(question)}"
    response = requests.post(url, headers={"accept": "application/json"})
    return format_response(response.json())

def format_response(data):
    if isinstance(data, dict):
        summary = data.get("Summary", "")
        # Convert markdown bold to HTML bold
        formatted_summary = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', summary)
        # Optional: Extend here for more sophisticated markdown conversions
        
        return '<div style="white-space: pre-wrap;">' + formatted_summary + '</div>'
    else:
        # Fallback to raw JSON if the expected data structure isn't present
        return '<div style="white-space: pre-wrap;">' + json.dumps(data, indent=2) + '</div>'

def create_gradio_interface():
    with gr.Blocks() as demo:
        gr.Markdown("##  SAP Navigator")
        with gr.Tab("Generate Query"):
            gr.Markdown("#### Enter your question for query generation:")
            question_input1 = gr.Textbox(lines=3, placeholder="Enter your question here...")
            output1 = gr.HTML(label="Query Result")
            generate_query_btn = gr.Button("Generate Query")
            generate_query_btn.click(generate_query, inputs=question_input1, outputs=output1)
        
        with gr.Tab("Generate Summary"):
            gr.Markdown("#### Enter your question for summary:")
            question_input2 = gr.Textbox(lines=3, placeholder="Enter your question here...")
            output2 = gr.HTML(label="Summary Result")
            generate_summary_btn = gr.Button("Generate Summary")
            generate_summary_btn.click(generate_summary, inputs=question_input2, outputs=output2)
    
    demo.launch()

if __name__ == "__main__":
    create_gradio_interface()