This is a small demo that uses OTel and OpenIA Agents tracing.

## How to run

- set `OPENAI_API_KEY`
- `docker-compose up`
- go to `http://localhost:8000`, wait for a haiku
- check out traces, logs, and metrics at `http://localhost:18888`

## Notable things

1. Agents instrumentation is provided by `openinference-instrumentation-openai-agents` and magically used by `opentelemetry-distro`.

    Look inside `OpenInferenceTracingProcessor`, you can see they have to do it in a [hacky way](https://github.com/Arize-ai/openinference/blob/c4e225244adc287b9b011972bc980550939e126a/python/instrumentation/openinference-instrumentation-openai-agents/src/openinference/instrumentation/openai_agents/_processor.py#L86).

2. Check out the app code - thanks to OpenInference hard work, the correlation between FastAPI (OTel) and OpenAI spans mostly works
   and we can mix and match OTel and OpenAI instrumentation and get correlated data.

    ```python
    @app.get("/")
    async def hello_world():
        result = await Runner.run(agent, "Write a haiku about recursion in programming.")
    ```

    with OTel, you can write spans of any shape and form, here's a basic example

    ```python
    with tracer.start_as_current_span("otel-span") as span:
        span.set_attribute("hello", "from otel span")
    ```

    but then I can also create spans with OpenAI

    ```python
    from agents import trace as agents_trace
    with agents_trace("openai-span"):
        requests.get("https://example.com") # you hope this HTTP request would become a child of openai-span, but nope, it won't
    ```

3. Check out logging and metrics - OTel covers other telemetry data and correlates it all

## Screenshots

Spans

<img width="1161" alt="image" src="https://github.com/user-attachments/assets/ed32f3f3-de4d-4f17-80e4-0349e9a4350a" />

<img width="1096" alt="image" src="https://github.com/user-attachments/assets/d15e5594-0411-4fc7-9655-84a889f144cc" />

![image](https://github.com/user-attachments/assets/89e41a00-b464-4f1c-982d-6da03deac53b)




