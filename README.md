# Chat Agent Sample with LangChain

This is a simple ReAct chatbot that uses the LangChain API to generate responses to user input.

## Project Setup

### Prerequisites

Make sure you have Python installed. You can download it from [python.org](https://www.python.org/).

### Create and Activate Virtual Environment

1. **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    ```

2. **Activate the virtual environment**:
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```

3. **Deactivate Virtual Environment**:
    
    When you're done using the chatbot, you can deactivate the virtual environment:
    - On Windows:
        ```bash
        venv\Scripts\deactivate
        ```

    - On macOS and Linux:
        ```bash
        deactivate
        ```

### Install Dependencies
```bash
pip3 install -r requirements.txt
```

## Run the Chatbot
```bash
python3 main.py
```