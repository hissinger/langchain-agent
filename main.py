import os
import readline
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_community.tools.tavily_search.tool import TavilySearchResults
from langchain.tools.render import render_text_description
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import ReActSingleInputOutputParser


# OpenAI API Key
os.environ["OPENAI_API_KEY"] = "your_openai_api_key"

# Tavily API key
os.environ["TAVILY_API_KEY"] = "your_tavily_api_key"


def custom_input(prompt):
    readline.set_pre_input_hook(lambda: readline.insert_text(""))
    readline.set_startup_hook(lambda: readline.insert_text(""))
    try:
        return input(prompt)
    finally:
        readline.set_pre_input_hook(None)
        readline.set_startup_hook(None)


def main():
    # message history to store chat messages
    memory = ConversationBufferMemory(memory_key="chat_history")

    # for search tool, we are using TavilySearchResults
    tools = [TavilySearchResults(max_results=5)]

    # prompt for the react agent
    prompt = hub.pull("hwchase17/react-chat")
    prompt = prompt.partial(
        tools=render_text_description(tools),
        tool_names=", ".join([t.name for t in tools]),
    )

    # create the model
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    llm_with_stop = llm.bind(stop=["\nObservation"])

    # using LCEL
    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_log_to_str(x["intermediate_steps"]),
            "chat_history": lambda x: x["chat_history"],
        }
        | prompt
        | llm_with_stop
        | ReActSingleInputOutputParser()
    )
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
    )

    while True:
        user_input = custom_input("You: ")
        if user_input.lower() == "exit":
            print("Assistant: Goodbye!")
            break

        try:
            response = agent_executor.invoke({"input": user_input})
            print("Assistant: " + response["output"])

        except Exception as e:
            print("Assistant: I'm sorry, I don't know how to respond to that.")
            print(e)


if __name__ == "__main__":
    main()
