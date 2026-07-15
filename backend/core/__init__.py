"""
TeamFlow EPMS — Core Module.

Provides shared base classes, utilities, and infrastructure used across
all TeamFlow Django apps:

- BaseModel / TimeStampedModel (abstract model bases)
- Custom exceptions + Ninja exception handlers
- Permission decorators for RBAC
- Pagination schemas
- Shared Pydantic schemas
- BaseService (service-layer pattern)
- NinjaAPI instance (master API)
"""
