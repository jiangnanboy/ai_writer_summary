import os
from dotenv import load_dotenv
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel

load_dotenv()

deepseek_api = os.environ['DEEPSEEK_API']
deepseek_url = os.environ['DEEPSEEK_URL']
deepseek_model = os.environ['DEEPSEEK_MODEL']

deepseek_provider = OpenAIProvider(
    base_url=deepseek_url,
    api_key=deepseek_api
)

deepseek_model = OpenAIModel(
    deepseek_model,
    provider=deepseek_provider
)
