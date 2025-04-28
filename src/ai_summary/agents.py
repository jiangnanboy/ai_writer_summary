from .types import (
    ArticlePlan, 
    ArticleSection
)
from pydantic_ai import Agent

from textwrap import dedent

class PlannerAgent:
    """
    基于文章内容创建提纲和内容
    """
    agent: Agent
    
    system_prompt: str = dedent("""\
    你是一个文章分析总结专家。你的任务是根据提供的文章内容创建一个详细的文章PPT总结规划。
    
    总是提供你的规划和回应背后的理由。
    """)
    
    def __init__(self, model):
        self.agent = Agent(
            model=model,
            system_prompt=self.system_prompt,
            result_type=ArticlePlan,
            retries=3,
        )
    
    def plan(self, content: str):
        prompt = dedent(f"""\
        基于以下文章内容创建一个详细的文章PPT总结规划：
        
        内容: {content}
        
        文章应该遵循一个标准的PPT结构，包括文章内容中的主要观点。
                
        确保文章的总结流程合乎逻辑，并可用于PPT内容创作。
        """)
        
        result = self.agent.run_sync(prompt)
        
        return result.data


class SummaryAgent:
    """
    根据规划以Markdown格式总结文章内容的代理。
    """
    
    agent: Agent
    
    system_prompt: str = dedent("""\
    你是一个文章内容分析总结专家。现在需要根据提供的文章内容对文章进行总结，输出的总结可用于PPT。您的任务是根据提供的文章内容规划以Markdown格式创建引人入胜、信息丰富且结构良好的文章总结内容。
    总是提供你的内容和回应背后的理由。
    
    遵循以下准则：
    1. 文章以清晰、简洁、有意义的方式总结。
    2. 使用适当的专业术语，同时保持目标受众的可访问性。
    3. 如果需要，则加入图片或图表的建议，它们会加强理解。
    4. 在需要的地方加入理论或者引用方法的资料论证。
    5. 如果需要进一步丰富总结，在合适的地方可以加入案例分析。
    6. 使内容吸引人，信息丰富，对读者有价值。
    7. 在Markdown中直接格式化你的输出：
       - 主标题使用 #
       - 章节标题使用 ##
       - 子章节使用 ###
       - 使用带有适当语言标签的Markdown块
       - 将图片占位符格式化为：![图片描述](image-placeholder.jpg "图片: 描述")
       - 使用 **粗体**、*斜体**、列表、引用和其他适当的Markdown格式
    9. 确保整个总结的格式一致，且分层表达，适用于PPT的展示。
    """)
    
    def __init__(self, model):
        self.agent = Agent(
            model=model,
            system_prompt=self.system_prompt,
            result_type=ArticleSection,
            retries=3,
        )

    def write_section(self, plan: ArticlePlan, section_index: int):
        if section_index >= len(plan.outline.sections):
            raise ValueError(f"章节索引 {section_index} 超出范围。")

        section = plan.outline.sections[section_index]

        prompt = dedent(f"""\
        用Markdown格式为一篇文章的一个章节写主要观点，规划如下：
        ```json
        {plan.model_dump_json(indent=2)}
        ```
        
        我们目前正在进行以下章节观点的工作：
        ```json
        {section.model_dump_json(indent=2)}
        ```
        
        章节中的观点应该满足以下要求：
        1. 从上一节的平稳过渡开始
        2. 涵盖章节观点规划中列出的所有项目
        3. 如果需要，使用适当的子标题（### 表示子章节）
        4. 包括例子、解释和见解

        使用 ## 作为主章节观点标题。
        
        对于任何图片，请以以下格式包含占位符：![图片描述](image-placeholder.jpg "图片: 描述")

        对于任何图示或图表，提供应该可视化的内容的详细描述。
        """)

        result = self.agent.run_sync(prompt)
        result.data.section_type = "body"
        return result.data

    def write_conclusion(self, plan: ArticlePlan):
        prompt = dedent(f"""\
        用Markdown格式为一篇文章内容写一个结论，规划如下
        ```json
        {plan.model_dump_json(indent=2)}
        ```
        
        结论中的内容应该反映或满足以下要求：
        1. 总结本文中涉及的要点
        2. 强化主要信息或论点
        3. 提供最后的想法、暗示或行动号召
        4. 让读者有所思考
        
        使用 ## 作为结论标题。
        
        对于任何图片，请以以下格式包含占位符：![图片描述](image-placeholder.jpg "图片: 描述")
        """)

        result = self.agent.run_sync(prompt)
        result.data.section_type = "conclusion"
        return result.data

