"""
LangGraph 反思机制
通过 3-7 轮对话提升 ChatBot 生成质量或内容深度
"""
import os
from typing import List, Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict, Annotated
from logger import LOG


class ReflectionState(TypedDict):
    """反思状态"""
    messages: Annotated[List, add_messages]
    iteration: int
    max_iterations: int
    final_output: Optional[str]
    reflection_history: List[str]


class LangGraphReflectionAgent:
    """
    使用 LangGraph 实现的反思机制 Agent
    通过多轮对话提升生成质量
    """
    
    def __init__(self, system_prompt_path: str, api_key: Optional[str] = None, max_iterations: int = 5):
        """
        初始化反思 Agent
        
        Args:
            system_prompt_path: System Prompt 文件路径
            api_key: OpenAI API Key
            max_iterations: 最大迭代次数（3-7 轮）
        """
        # 读取 System Prompt
        with open(system_prompt_path, 'r', encoding='utf-8') as f:
            self.system_prompt = f.read()
        
        # 初始化 LLM
        api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("需要设置 OPENAI_API_KEY 环境变量")
        
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            api_key=api_key
        )
        
        self.max_iterations = max(3, min(7, max_iterations))  # 限制在 3-7 轮之间
        
        # 构建 LangGraph
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """构建 LangGraph 工作流"""
        workflow = StateGraph(ReflectionState)
        
        # 添加节点
        workflow.add_node("generate", self._generate_node)
        workflow.add_node("reflect", self._reflect_node)
        workflow.add_node("improve", self._improve_node)
        
        # 设置入口点
        workflow.set_entry_point("generate")
        
        # 添加条件边
        workflow.add_conditional_edges(
            "generate",
            self._should_reflect,
            {
                "reflect": "reflect",
                "improve": "improve",
                "end": END
            }
        )
        
        workflow.add_conditional_edges(
            "reflect",
            self._should_continue,
            {
                "improve": "improve",
                "end": END
            }
        )
        
        workflow.add_conditional_edges(
            "improve",
            self._should_continue,
            {
                "generate": "generate",
                "end": END
            }
        )
        
        return workflow.compile()
    
    def _generate_node(self, state: ReflectionState) -> ReflectionState:
        """生成节点：生成初始内容"""
        messages = state.get("messages", [])
        iteration = state.get("iteration", 0)
        
        # 构建生成提示
        if iteration == 0:
            # 第一轮：生成初始内容
            prompt = "请将以下内容转换为 ChatPPT 标准输入格式（Markdown）：\n\n" + messages[-1].content
        else:
            # 后续轮次：基于反思改进
            prompt = f"基于以下反思，改进并重新生成 Markdown 内容：\n\n反思：{state.get('reflection_history', [])[-1]}\n\n原始内容：{messages[-1].content}"
        
        # 调用 LLM
        response = self.llm.invoke([
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ])
        
        # 更新状态
        state["messages"].append(AIMessage(content=response.content))
        state["iteration"] = iteration + 1
        state["final_output"] = response.content.strip()
        
        LOG.info(f"第 {iteration + 1} 轮生成完成")
        
        return state
    
    def _reflect_node(self, state: ReflectionState) -> ReflectionState:
        """反思节点：分析生成内容的质量"""
        messages = state.get("messages", [])
        current_output = state.get("final_output", "")
        
        # 反思提示
        reflection_prompt = f"""
请对以下生成的 Markdown 内容进行反思和评估：

生成内容：
{current_output}

请从以下角度进行评估：
1. 内容完整性和准确性
2. 结构清晰度
3. 是否符合 ChatPPT 标准格式
4. 是否有改进空间

请提供具体的改进建议。
"""
        
        reflection = self.llm.invoke([
            SystemMessage(content="你是一个专业的质量评估专家，擅长分析和改进内容质量。"),
            HumanMessage(content=reflection_prompt)
        ])
        
        reflection_text = reflection.content.strip()
        state["reflection_history"] = state.get("reflection_history", []) + [reflection_text]
        
        LOG.info(f"第 {state.get('iteration', 0)} 轮反思完成")
        
        return state
    
    def _improve_node(self, state: ReflectionState) -> ReflectionState:
        """改进节点：基于反思改进内容"""
        # 改进逻辑在 generate 节点中实现
        # 这里主要用于状态更新
        LOG.info("进入改进阶段")
        return state
    
    def _should_reflect(self, state: ReflectionState) -> str:
        """判断是否需要反思"""
        iteration = state.get("iteration", 0)
        max_iterations = state.get("max_iterations", self.max_iterations)
        
        if iteration == 0:
            # 第一轮生成后，总是进行反思
            return "reflect"
        elif iteration < max_iterations:
            # 在最大迭代次数内，继续改进
            return "improve"
        else:
            # 达到最大迭代次数，结束
            return "end"
    
    def _should_continue(self, state: ReflectionState) -> str:
        """判断是否继续迭代"""
        iteration = state.get("iteration", 0)
        max_iterations = state.get("max_iterations", self.max_iterations)
        
        if iteration < max_iterations:
            return "improve" if state.get("reflection_history") else "generate"
        else:
            return "end"
    
    def generate_with_reflection(self, user_input: str) -> str:
        """
        使用反思机制生成内容
        
        Args:
            user_input: 用户输入
            
        Returns:
            最终生成的 Markdown 内容
        """
        # 初始化状态
        initial_state: ReflectionState = {
            "messages": [HumanMessage(content=user_input)],
            "iteration": 0,
            "max_iterations": self.max_iterations,
            "final_output": None,
            "reflection_history": []
        }
        
        # 运行工作流
        final_state = self.graph.invoke(initial_state)
        
        # 返回最终输出
        final_output = final_state.get("final_output", "")
        
        LOG.info(f"反思机制完成，共进行 {final_state.get('iteration', 0)} 轮迭代")
        
        return final_output

