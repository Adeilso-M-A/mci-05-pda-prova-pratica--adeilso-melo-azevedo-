"""Configuração global do pytest para o projeto Chamados."""

import os

os.environ.setdefault("POSTGRES_DB", "chamados")
os.environ.setdefault("POSTGRES_USER", "postgres_user")
os.environ.setdefault("POSTGRES_PASSWORD", "postgres_pass")
os.environ.setdefault("POSTGRES_HOST", "localhost")
os.environ.setdefault("POSTGRES_PORT", "5432")
os.environ.setdefault("SECRET_KEY", "chave-secreta-apenas-para-testes")
os.environ.setdefault("DEBUG", "True")
os.environ.setdefault("ALLOWED_HOSTS", "localhost,127.0.0.1")
