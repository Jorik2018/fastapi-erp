import inspect
from typing import (
    Any,
    Callable,
    ClassVar,
    List,
    Type,
    TypeVar,
    Union,
    get_origin,
    get_type_hints,
)

from fastapi import APIRouter, Depends
from starlette.routing import Route, WebSocketRoute


T = TypeVar("T")

CBV_CLASS_KEY = "__cbv_class__"


def is_classvar(annotation: Any) -> bool:
    return annotation is ClassVar or get_origin(annotation) is ClassVar


def cbv(router: APIRouter) -> Callable[[Type[T]], Type[T]]:
    """
    This function returns a decorator that converts the decorated
    into a class-based view for the provided router.
    """

    def decorator(cls: Type[T]) -> Type[T]:
        # this is a fix
        router.prefix = ''
        return _cbv(router, cls)

    return decorator


def _cbv(router: APIRouter, cls: Type[T]) -> Type[T]:
    """
    Replaces any methods of the provided class `cls` that are endpoints
    of routes in `router` with updated function calls that will properly
    inject an instance of `cls`.
    """

    _init_cbv(cls)

    cbv_router = APIRouter()

    function_members = inspect.getmembers(cls, inspect.isfunction)
    functions_set = set(func for _, func in function_members)

    cbv_routes = [
        route
        for route in router.routes
        if isinstance(route, (Route, WebSocketRoute))
        and route.endpoint in functions_set
    ]

    for route in cbv_routes:
        router.routes.remove(route)

        _update_cbv_route_endpoint_signature(
            cls,
            route
        )

        cbv_router.routes.append(route)

    router.include_router(cbv_router)

    return cls


def _init_cbv(cls: Type[Any]) -> None:
    """
    Modifies the class so FastAPI can inject class-level dependencies.
    """

    if getattr(cls, CBV_CLASS_KEY, False):
        return

    old_init: Callable[..., Any] = cls.__init__

    old_signature = inspect.signature(old_init)

    old_parameters = list(
        old_signature.parameters.values()
    )[1:]

    new_parameters = [
        x
        for x in old_parameters
        if x.kind not in (
            inspect.Parameter.VAR_POSITIONAL,
            inspect.Parameter.VAR_KEYWORD,
        )
    ]

    dependency_names: List[str] = []

    for name, hint in get_type_hints(cls).items():

        if is_classvar(hint):
            continue

        parameter_kwargs = {
            "default": getattr(
                cls,
                name,
                Ellipsis
            )
        }

        dependency_names.append(name)

        new_parameters.append(
            inspect.Parameter(
                name=name,
                kind=inspect.Parameter.KEYWORD_ONLY,
                annotation=hint,
                **parameter_kwargs
            )
        )

    new_signature = old_signature.replace(
        parameters=new_parameters
    )

    def new_init(
        self: Any,
        *args: Any,
        **kwargs: Any
    ) -> None:

        for dep_name in dependency_names:
            dep_value = kwargs.pop(dep_name)
            setattr(
                self,
                dep_name,
                dep_value
            )

        old_init(
            self,
            *args,
            **kwargs
        )

    setattr(
        cls,
        "__signature__",
        new_signature
    )

    setattr(
        cls,
        "__init__",
        new_init
    )

    setattr(
        cls,
        CBV_CLASS_KEY,
        True
    )


def _update_cbv_route_endpoint_signature(
    cls: Type[Any],
    route: Union[Route, WebSocketRoute]
) -> None:
    """
    Fixes the endpoint signature so FastAPI performs dependency
    injection properly.
    """

    old_endpoint = route.endpoint

    old_signature = inspect.signature(
        old_endpoint
    )

    old_parameters: List[inspect.Parameter] = list(
        old_signature.parameters.values()
    )

    old_first_parameter = old_parameters[0]

    new_first_parameter = old_first_parameter.replace(
        default=Depends(cls)
    )

    new_parameters = [
        new_first_parameter
    ] + [
        parameter.replace(
            kind=inspect.Parameter.KEYWORD_ONLY
        )
        for parameter in old_parameters[1:]
    ]

    new_signature = old_signature.replace(
        parameters=new_parameters
    )

    setattr(
        route.endpoint,
        "__signature__",
        new_signature
    )