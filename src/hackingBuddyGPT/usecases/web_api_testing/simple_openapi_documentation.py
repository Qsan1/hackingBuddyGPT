from dataclasses import dataclass, field
from typing import List, Any, Union, Dict

import pydantic_core
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionMessage
from rich.panel import Panel

from hackingBuddyGPT.capabilities import Capability
from hackingBuddyGPT.capabilities.http_request import HTTPRequest
from hackingBuddyGPT.capabilities.record_note import RecordNote
from hackingBuddyGPT.usecases.common_patterns import RoundBasedUseCase
from hackingBuddyGPT.usecases.web_api_testing.utils.documentation_handler import DocumentationHandler
from hackingBuddyGPT.usecases.web_api_testing.utils.llm_handler import LLMHandler
from hackingBuddyGPT.usecases.web_api_testing.prompt_engineer import PromptEngineer, PromptStrategy
from hackingBuddyGPT.usecases.web_api_testing.utils.response_handler import ResponseHandler
from hackingBuddyGPT.utils import tool_message
from hackingBuddyGPT.utils.configurable import parameter
from hackingBuddyGPT.utils.openai.openai_lib import OpenAILib
from hackingBuddyGPT.usecases.base import use_case
Prompt = List[Union[ChatCompletionMessage, ChatCompletionMessageParam]]
Context = Any

@use_case("simple_web_api_documentation", "Minimal implementation of a web api documentation use case")
@dataclass
class SimpleWebAPIDocumentation(RoundBasedUseCase):
    llm: OpenAILib
    host: str = parameter(desc="The host to test", default="https://jsonplaceholder.typicode.com")
    _prompt_history: Prompt = field(default_factory=list)
    _context: Context = field(default_factory=lambda: {"notes": list()})
    _capabilities: Dict[str, Capability] = field(default_factory=dict)
    _all_http_methods_found: bool = False

    # Description for expected HTTP methods
    http_method_description: str = parameter(
        desc="Pattern description for expected HTTP methods in the API response",
        default="A string that represents an HTTP method (e.g., 'GET', 'POST', etc.)."
    )

    # Template for HTTP methods in API requests
    http_method_template: str = parameter(
        desc="Template to format HTTP methods in API requests, with {method} replaced by actual HTTP method names.",
        default="{method}"
    )

    # List of expected HTTP methods
    http_methods: str = parameter(
        desc="Expected HTTP methods in the API, as a comma-separated list.",
        default="GET,POST,PUT,PATCH,DELETE"
    )

    def init(self):
        super().init()
        self._setup_capabilities()
        self.llm_handler = LLMHandler(self.llm, self._capabilities)
        self.response_handler = ResponseHandler(self.llm_handler)
        self._setup_initial_prompt()
        self.documentation_handler = DocumentationHandler(self.llm_handler, self.response_handler)

    def _setup_capabilities(self):
        notes = self._context["notes"]
        self._capabilities = {
            "http_request": HTTPRequest(self.host),
            "record_note": RecordNote(notes)
        }

    def _setup_initial_prompt(self):
        initial_prompt = {
            "role": "system",
            "content": f"You're tasked with documenting the REST APIs of a website hosted at {self.host}. "
                       f"Start with an empty OpenAPI specification.\n"
                       f"Maintain meticulousness in documenting your observations as you traverse the APIs."
        }
        self._prompt_history.append(initial_prompt)
        self.prompt_engineer = PromptEngineer(strategy=PromptStrategy.CHAIN_OF_THOUGHT, llm_handler=self.llm_handler,
                                              history=self._prompt_history, schemas={},
                                              response_handler=self.response_handler)


    def all_http_methods_found(self):
        self.console.print(Panel("All HTTP methods found! Congratulations!", title="system"))
        self._all_http_methods_found = True

    def perform_round(self, turn: int):
        prompt = self.prompt_engineer.generate_prompt(doc=True)
        response, completion = self.llm_handler.call_llm(prompt)
        self._handle_response(completion, response)

    def _handle_response(self, completion, response):
        message = completion.choices[0].message
        tool_call_id = message.tool_calls[0].id
        command = pydantic_core.to_json(response).decode()
        self.console.print(Panel(command, title="assistant"))
        self._prompt_history.append(message)

        with self.console.status("[bold green]Executing that command..."):
            result = response.execute()
            self.console.print(Panel(result[:30], title="tool"))
            result_str = self.response_handler.parse_http_status_line(result)
            self._prompt_history.append(tool_message(result_str, tool_call_id))
            invalid_flags = ["recorded","Not a valid HTTP method", "404" ,"Client Error: Not Found"]
            print(f'result_str:{result_str}')
            if not result_str in invalid_flags  or any(item in result_str for item in invalid_flags):
                self.documentation_handler.update_openapi_spec(response, result)
                self.documentation_handler.write_openapi_to_yaml()
                self.prompt_engineer.schemas = self.documentation_handler.schemas
        return self._all_http_methods_found



    def has_no_numbers(self, path):
        return not any(char.isdigit() for char in path)

