from typing import List, Optional
from pydantic import BaseModel, Field
from textwrap import dedent

class Reasoning(BaseModel):
    """
    推理
    """
    description: str = Field(description="推理原因。")

class OutlineSection(BaseModel):
    """
    大纲章节
    """
    title: str = Field(description="章节标题。")
    items: List[str] = Field(default_factory=list, description="章节中要涵盖的主题和项目的列表。")
    word_count: int = Field(description="章节的大致字数")

class ArticleOutline(BaseModel):
    """
    文章大纲
    """
    title: str = Field(description="文章标题。")
    subtitle: Optional[str] = Field(None, description="文章的副标题。")
    introduction_word_count: int = Field(description="引言的大致字数。")
    conclusion_word_count: int = Field(description="结论的大致字数。")
    sections: List[OutlineSection] = Field(default_factory=list, description="大纲中的章节列表。")

class ArticlePlan(BaseModel):
    """
    文章规划
    """
    reasoning: Reasoning = Field(description="文章规划背后的推理。")
    outline: ArticleOutline = Field(description="文章的大纲。")

class ArticleSection(BaseModel):
    """
    文章章节
    """
    reasoning: Reasoning = Field(description="章节内容背后的推理。")
    title: str = Field(description="章节的标题。")
    markdown_content: str = Field(description="以Markdown格式格式化的章节内容。")
    section_type: str = Field(description=dedent("""\
        章节的类型，可以是以下之一：
        - 引言: 文章的引言部分
        - 正文: 文章的正文部分。
        - 结论: 文章的结论部分。
        """))
    image_descriptions: List[str] = Field(default_factory=list, description="章节中应该包含的图像描述。")

