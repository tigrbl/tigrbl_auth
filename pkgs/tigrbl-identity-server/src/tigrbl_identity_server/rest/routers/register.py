from __future__ import annotations

from pathlib import Path

from tigrbl_auth.api.rest.schemas import DynamicClientRegistrationOut
from tigrbl_auth.framework import Depends, HTTPException, TigrblRouter, status
from tigrbl_auth.ops.register import delete_registered_client, get_registered_client, register_client, update_registered_client
from tigrbl_auth.tables import get_db

api = TigrblRouter()
router = api


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def _sync_client_registration(command: str, registration) -> None:
    from tigrbl_auth.services._operator_store import OperationContext
    from tigrbl_auth.services.operator_service import create_resource, delete_resource, update_resource

    if isinstance(registration, dict):
        payload = dict(registration)
    elif hasattr(registration, 'model_dump'):
        payload = registration.model_dump(mode='json')
    else:
        payload = dict(getattr(registration, '__dict__', {}))
    client_id = str(payload.get('client_id') or payload.get('id'))
    if not client_id:
        return
    context = OperationContext(repo_root=_repo_root(), command=command, resource='client', actor='rest')
    patch = {
        'client_id': client_id,
        'tenant_id': payload.get('tenant_id'),
        'metadata': payload,
        'contacts': payload.get('contacts') or [],
        'software_id': payload.get('software_id'),
        'software_version': payload.get('software_version'),
        'registration_access_token_hash': payload.get('registration_access_token_hash'),
        'registration_client_uri': payload.get('registration_client_uri'),
    }
    if command.endswith('.delete'):
        try:
            delete_resource(context, record_id=client_id, if_missing='skip')
        except Exception:
            pass
        return
    existing_command = update_resource if command.endswith('.update') else create_resource
    try:
        existing_command(context, record_id=client_id, patch=patch, if_missing='create' if command.endswith('.update') else 'error', if_exists='update' if command.endswith('.create') else 'error')
    except TypeError:
        # update/create have distinct signatures
        if command.endswith('.update'):
            update_resource(context, record_id=client_id, patch=patch, if_missing='create')
        else:
            create_resource(context, record_id=client_id, patch=patch, if_exists='update')


@api.route('/register', methods=['POST'], response_model=DynamicClientRegistrationOut)
async def register(request, db=Depends(get_db)):
    result = await register_client(request=request, db=db)
    _sync_client_registration('client.registration.create', result)
    return result


@api.route('/client/register', methods=['POST'], response_model=DynamicClientRegistrationOut)
async def register_legacy(request, db=Depends(get_db)):
    raise HTTPException(status.HTTP_400_BAD_REQUEST, 'legacy client registration path unsupported; use /register')


@api.route('/register/{client_id}', methods=['GET'], response_model=DynamicClientRegistrationOut)
async def register_get(request, client_id: str, db=Depends(get_db)):
    return await get_registered_client(request=request, db=db, client_id=client_id)


@api.route('/register/{client_id}', methods=['PUT'], response_model=DynamicClientRegistrationOut)
async def register_put(request, client_id: str, db=Depends(get_db)):
    result = await update_registered_client(request=request, db=db, client_id=client_id)
    _sync_client_registration('client.registration.update', result)
    return result


@api.route('/register/{client_id}', methods=['DELETE'])
async def register_delete(request, client_id: str, db=Depends(get_db)):
    result = await delete_registered_client(request=request, db=db, client_id=client_id)
    _sync_client_registration('client.registration.delete', {'client_id': client_id})
    return result


@api.route('/client/{client_id}', methods=['GET'], response_model=DynamicClientRegistrationOut)
async def register_get_legacy(request, client_id: str, db=Depends(get_db)):
    return await register_get(request=request, client_id=client_id, db=db)


@api.route('/client/{client_id}', methods=['PUT'], response_model=DynamicClientRegistrationOut)
async def register_put_legacy(request, client_id: str, db=Depends(get_db)):
    return await register_put(request=request, client_id=client_id, db=db)


@api.route('/client/{client_id}', methods=['PATCH'], response_model=DynamicClientRegistrationOut)
async def register_patch_legacy(request, client_id: str, db=Depends(get_db)):
    return await register_put(request=request, client_id=client_id, db=db)


@api.route('/client/{client_id}', methods=['DELETE'])
async def register_delete_legacy(request, client_id: str, db=Depends(get_db)):
    return await register_delete(request=request, client_id=client_id, db=db)
