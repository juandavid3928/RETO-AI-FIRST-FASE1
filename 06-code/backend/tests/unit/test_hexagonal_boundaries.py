import ast
from pathlib import Path


FORBIDDEN_ROOTS = {"fastapi", "psycopg", "pydantic", "pwdlib", "argon2", "app.infrastructure"}


def test_domain_and_application_do_not_import_frameworks_or_infrastructure() -> None:
    roots = [Path("app/domain"), Path("app/application")]
    violations: list[str] = []
    for root in roots:
        for source in root.rglob("*.py"):
            tree = ast.parse(source.read_text())
            imports = [node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
            for imported in imports:
                names = (
                    [alias.name for alias in imported.names]
                    if isinstance(imported, ast.Import)
                    else [imported.module or ""]
                )
                for name in names:
                    if any(name == forbidden or name.startswith(f"{forbidden}.") for forbidden in FORBIDDEN_ROOTS):
                        violations.append(f"{source}: {name}")
    assert violations == []
