from langgraph.graph import StateGraph , START , END
from .schemas import AgentState
from langgraph.prebuilt import ToolNode , tools_condition
from langchain.messages import SystemMessage
class Agent:
    
    def __init__(self , llm , tools , system_prompt):
        self.llm = llm
        self.tools = tools
        self.system_prompt = system_prompt
    
    def llm_invoke(self , state):
        if "messages" not in state:
            state["messages"] = []
        
        existing_systems = [m for m in state.get("messages", []) if isinstance(m , SystemMessage)]
        if not any(m.content == self.system_prompt for m in existing_systems):
            state["messages"].insert(0, SystemMessage(content=self.system_prompt))
        
        messages = state["messages"]
        llm_with_tools = self.llm.bind_tools(self.tools)
        response = llm_with_tools.invoke(messages)

        return {"messages": [response]}

    def build_graph(self):
        graph = StateGraph(AgentState)

        graph.add_node("llm" , self.llm_invoke)
        graph.add_node("tools" , ToolNode(tools=self.tools))

        graph.add_edge(START , "llm")
        graph.add_edge("llm" , END)
        graph.add_edge("tools" , "llm")
        graph.add_conditional_edges("llm" , tools_condition,
            {
                "tools":"tools",
                END:END
            }
        )

        return graph.compile()
