from opentelemetry import trace

from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider

resource = Resource.create({

    "service.name": "cea-investimentos",
    "service.version": "6.0",
    "liceu.layer": "financial-runtime"

})

trace.set_tracer_provider(
    TracerProvider(resource=resource)
)

tracer = trace.get_tracer("cea-investimentos")
