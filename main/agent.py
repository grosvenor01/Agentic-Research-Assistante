from langgraph.graph import StateGraph , START , END
from .schemas import AgentState
from .tools import PlanningTools , SynthesisTools , EvaluationTools , CitationTools
from langgraph.prebuilt import ToolNode , tools_condition
class Agent:
    
    def __init__(self , llm , tools):
        self.plannerLLM = llm
        self.tools = tools
    
    def planner(self , state):
        pass

    def synthesis(self , state):
        pass

    def evaluator(self , state):
        pass

    def citation(self , state):
        pass

    def build_graph(self , state):
        graph = StateGraph(AgentState)
        # LLM Nodes
        graph.add_node("Planner" , self.planner)
        graph.add_node("Synthesis" , self.synthesis)
        graph.add_node("Evaluator" , self.evaluator)
        graph.add_node("Citation" , self.citation)
        
        # Tool Nodes
        graph.add_node("Planning_Tools" , ToolNode(tools=PlanningTools))
        graph.add_node("Synthesis_Tools" , ToolNode(tools=SynthesisTools))
        graph.add_node("Evaluation_Tools" , ToolNode(tools=EvaluationTools))
        graph.add_node("Citation_Tools" , ToolNode(tools=CitationTools))

        # Static Edges 
        graph.add_edge(START , "Planner")
        graph.add_edge("Planner" , "Synthesis")
        graph.add_edge("Synthesis" , "Evaluator")
        graph.add_edge("Evaluator" , "Citation")
        graph.add_edge("Citation" , END)

        # Conditional Edges
        graph.add_conditional_edges("Planner" , "Planning_Tools" , tools_condition(PlanningTools))
        graph.add_conditional_edges("Synthesis" , "Synthesis_Tools" , tools_condition(SynthesisTools))
        graph.add_conditional_edges("Evaluator" , "Evaluation_Tools" , tools_condition(EvaluationTools))
        graph.add_conditional_edges("Citation" , "Citation_Tools" , tools_condition(CitationTools))

        # Tools Response Edges
        graph.add_edge("Planning_Tools" , "Planner")
        graph.add_edge("Synthesis_Tools" , "Synthesis")
        graph.add_edge("Evaluation_Tools" , "Evaluator")
        graph.add_edge("Citation_Tools" , "Citation")

        return graph.compile()
