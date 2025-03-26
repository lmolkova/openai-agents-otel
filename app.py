import logging

import requests
from opentelemetry import trace
from agents import trace as agents_trace
from agents import Agent, Runner

from fastapi import FastAPI

app = FastAPI()

tracer = trace.get_tracer(__name__)

agent = Agent(name="Assistant", instructions="You are a helpful assistant")
@app.get("/")
async def hello_world():

    with tracer.start_as_current_span("otel-span") as otel_span:
        otel_span.set_attribute("hello", "from otel span")

        result = await Runner.run(agent, "Write a haiku about recursion in programming.")
        logging.warning(f"Result: {result}")

    # this is a general-purpose API intended for end-users, but OTel provides them
    # allowing to correlate spans (with spans and logs).
    with agents_trace("openai-span"):
        requests.get("https://example.com")

    return result.final_output


