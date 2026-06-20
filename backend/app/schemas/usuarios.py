from pydantic import BaseModel, EmailStr


class SecretariaBase(BaseModel):
    nome: str
    sigla: str
    ativa: bool = True


class SecretariaCreate(SecretariaBase):
    pass


class SecretariaUpdate(BaseModel):
    nome: str | None = None
    sigla: str | None = None
    ativa: bool | None = None


class SecretariaResponse(SecretariaBase):
    id: int

    model_config = {"from_attributes": True}


# ── Usuário ────────────────────────────────────────────────────────────────────

class UsuarioBase(BaseModel):
    username: str
    email: str
    first_name: str = ""
    last_name: str = ""
    perfil: str = "OPERADOR"
    secretaria_id: int | None = None
    telefone: str = ""


class UsuarioCreate(UsuarioBase):
    password: str


class UsuarioUpdate(BaseModel):
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    perfil: str | None = None
    secretaria_id: int | None = None
    telefone: str | None = None
    ativo: bool | None = None


class UsuarioChangePassword(BaseModel):
    current_password: str
    new_password: str


class UsuarioResponse(UsuarioBase):
    id: int
    ativo: bool
    is_superuser: bool
    foto: str | None = None
    secretaria: SecretariaResponse | None = None

    model_config = {"from_attributes": True}


class UsuarioMe(UsuarioResponse):
    """Dados do usuário logado (inclui perfil completo)."""
    pass
