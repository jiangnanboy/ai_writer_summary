from .types import (
    ArticlePlan, 
    ArticleSection
)
from pydantic_ai import Agent

from textwrap import dedent

class PlannerAgent:
    """
    基于主题和字数统计创建文章规划的代理
    """
    agent: Agent
    
    system_prompt: str = dedent("""\
    你是一个文章策划者。你的任务是根据提供的主题和字数创建一个详细的文章规划。
    
    总是提供你的规划和回应背后的理由。
    """)
    
    def __init__(self, model):
        self.agent = Agent(
            model=model,
            system_prompt=self.system_prompt,
            result_type=ArticlePlan,
            retries=3,
        )
    
    def plan(self, topic: str, word_count: int):
        prompt = dedent(f"""\
        基于以下主题和字数创建一个详细的文章规划：
        
        主题: {topic}
        字数: {word_count}
        
        文章应该遵循一个标准的结构，包括引言、章节正文部分和结论。
        
        对于每个章节，指定应该涵盖的主题和项目，并提供一个大致的字数。
        所有章节的字数之和（包括引言和结论）应该大致等于总字数。
        
        确保文章的流程合乎逻辑，并吸引技术/教育/政府/企业等读者。
        """)
        
        result = self.agent.run_sync(prompt)
        
        return result.data


class ContentWriterAgent:
    """
    根据规划以Markdown格式编写文章内容的代理。
    """
    
    agent: Agent
    
    system_prompt: str = dedent("""\
    你是一个文章内容作者。您的任务是根据提供的文章规划以Markdown格式创建引人入胜、信息丰富且结构良好的内容。
    总是提供你的内容和回应背后的理由。
    
    遵循以下准则：
    1. 文章以清晰、简洁、有意义的方式写作。
    2. 使用适当的专业术语，同时保持目标受众的可访问性。
    3. 如果需要，则加入图片或图表的建议，它们会加强理解。
    4. 在需要的地方加入理论或者引用方法的资料论证。
    5. 如果需要进一步丰富文章，在合适的地方可以加入案例分析。
    6. 确保内容符合规划中指定的字数。
    7. 使内容吸引人，信息丰富，对读者有价值。
    8. 在Markdown中直接格式化你的输出：
       - 主标题使用 #
       - 章节标题使用 ##
       - 子章节使用 ###
       - 使用带有适当语言标签的Markdown块
       - 将图片占位符格式化为：![图片描述](image-placeholder.jpg "图片: 描述")
       - 使用 **粗体**、*斜体**、列表、引用和其他适当的Markdown格式
    9. 确保整个章节的格式一致。
    """)
    
    def __init__(self, model):
        self.agent = Agent(
            model=model,
            system_prompt=self.system_prompt,
            result_type=ArticleSection,
            retries=3,
        )
    
    def write_introduction(self, plan: ArticlePlan):
        prompt = dedent(f"""\
        根据以下规划，用Markdown格式为一篇文章写一个引言：
        ```json
        {plan.model_dump_json(indent=2)}
        ```
        
        引言中的内容应该满足以下要求：
        1. 用一个吸引人的开头来吸引读者
        2. 为主题提供上下文和背景
        3. 陈述文章的目的或论点
        4. 简要概述读者将了解的内容
        5. 大约是{plan.outline.introduction_word_count}个单词
        
        使用 ## 作为引言标题。
        
        对于任何图片，请以以下格式包含占位符：![图片描述](image-placeholder.jpg "图片: 描述")
        """)
        
        result = self.agent.run_sync(prompt)
        result.data.section_type = "introduction"
        return result.data
    
    def write_section(self, plan: ArticlePlan, section_index: int):
        if section_index >= len(plan.outline.sections):
            raise ValueError(f"章节索引 {section_index} 超出范围。")
        
        section = plan.outline.sections[section_index]
        
        prompt = dedent(f"""\
        用Markdown格式为一篇文章的一个章节写内容，规划如下：
        ```json
        {plan.model_dump_json(indent=2)}
        ```
        
        我们目前正在进行以下章节的工作：
        ```json
        {section.model_dump_json(indent=2)}
        ```
        
        章节中的内容应该满足以下要求：
        1. 从上一节的平稳过渡开始
        2. 涵盖章节规划中列出的所有项目
        3. 如果需要，使用适当的子标题（### 表示子章节）
        4. 包括例子、解释和见解
        5. 大约为{section.word_count}字

        使用 ## 作为主章节标题。
        
        对于任何图片，请以以下格式包含占位符：![图片描述](image-placeholder.jpg "图片: 描述")

        对于任何图示或图表，提供应该可视化的内容的详细描述。
        """)
        
        result = self.agent.run_sync(prompt)
        result.data.section_type = "body"
        return result.data
    
    def write_conclusion(self, plan: ArticlePlan):
        prompt = dedent(f"""\
        用Markdown格式为一篇文章写一个结论，规划如下
        ```json
        {plan.model_dump_json(indent=2)}
        ```
        
        结论中的内容应该反映或满足以下要求：
        1. 总结本文中涉及的要点
        2. 强化主要信息或论点
        3. 提供最后的想法、暗示或行动号召
        4. 让读者有所思考
        5. 大约为{plan.outline.conclusion_word_count}字
        
        使用 ## 作为结论标题。
        
        对于任何图片，请以以下格式包含占位符：![图片描述](image-placeholder.jpg "图片: 描述")
        """)
        
        result = self.agent.run_sync(prompt)
        result.data.section_type = "conclusion"
        return result.data

