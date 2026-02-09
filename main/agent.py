from langgraph.graph import StateGraph , START , END
from .schemas import AgentState
from .tools import PlanningTools , SynthesisTools , EvaluationTools , CitationTools
from langgraph.prebuilt import ToolNode , tools_condition
class Agent:
    
    def __init__(self , llm , tools):
        self.llm = llm
        self.tools = tools
    
    def llm_invoke(self , state):
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

        graph.add_conditional_edges("llm" , tools_condition,
            {
                "tools":"tools",
                END:END
            }
        )
        return graph.compile()
