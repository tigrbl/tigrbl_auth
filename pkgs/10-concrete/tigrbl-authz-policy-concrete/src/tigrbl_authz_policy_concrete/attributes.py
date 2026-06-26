"""Mapping-backed attribute resolver and selector implementations."""

from __future__ import annotations

from typing import Any, Mapping

from tigrbl_identity_contracts.policy import AttributeDesignator, AttributeSelector, PolicyRequest


class MappingAttributeResolver:
    def resolve(self, designator: AttributeDesignator, request: PolicyRequest, /) -> Any:
        if designator.attribute_id in request.attributes:
            return request.attributes[designator.attribute_id]
        if designator.required:
            raise KeyError(designator.attribute_id)
        return None


class MappingAttributeSelector:
    def select(self, selector: AttributeSelector, values: Mapping[str, Any], /) -> Any:
        current: Any = values
        for part in selector.path:
            if isinstance(current, Mapping) and part in current:
                current = current[part]
                continue
            if selector.required:
                raise KeyError(".".join(selector.path))
            return None
        return current


__all__ = ["MappingAttributeResolver", "MappingAttributeSelector"]
