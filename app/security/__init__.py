"""Package security (offline).

Expose une classe `User` minimale afin que `from app.security import User`
fonctionne sans base de données ni ORM.
"""

from dataclasses import dataclass


@dataclass
class User:
	username: str
	password: str
	role: str = "user"

	@property
	def is_authenticated(self) -> bool:  # pragma: no cover
		return True

	@property
	def is_active(self) -> bool:  # pragma: no cover
		return True

	@property
	def is_anonymous(self) -> bool:  # pragma: no cover
		return False

	def get_id(self) -> str:  # pragma: no cover
		return self.username
